import cv2
import base64
import os
import requests
from PIL import Image
import io
import tempfile

def extract_frames(video_path, num_frames=4):
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frames = []
    
    if total_frames == 0:
        cap.release()
        return frames

    indices = [int(total_frames * i / num_frames) for i in range(num_frames)]
    
    for idx in indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        ret, frame = cap.read()
        if ret:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(frame_rgb)
            pil_img = pil_img.resize((640, 360))
            buffer = io.BytesIO()
            pil_img.save(buffer, format='JPEG', quality=70)
            b64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            frames.append(b64)
    
    cap.release()
    return frames

def analyze_video_frames(frames, drill_title, coaching_points, skill_type):
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return None

    coaching_str = "\n".join([f"- {p}" for p in coaching_points])

    content = [
        {
            "type": "text",
            "text": f"""You are an expert youth soccer coach analyzing a player's technique video.

The player is doing the drill: {drill_title}
Skill type: {skill_type}

Key coaching points for this drill:
{coaching_str}

I am sending you {len(frames)} frames from their training video. Analyze their technique and provide:

1. TECHNIQUE_SCORE: A score from 0-100 based on their technique
2. STRENGTH: One specific thing they are doing well (1-2 sentences)
3. CORRECTION: One specific thing to improve with actionable advice (1-2 sentences)
4. BODY_POSITION: Brief comment on their body position and posture
5. SUMMARY: An encouraging 1-sentence summary for a young player

Be specific to what you can see in the frames. Be encouraging but honest. Format your response exactly like this:
TECHNIQUE_SCORE: [number]
STRENGTH: [text]
CORRECTION: [text]
BODY_POSITION: [text]
SUMMARY: [text]"""
        }
    ]

    for i, frame in enumerate(frames):
        content.append({
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{frame}",
                "detail": "low"
            }
        })

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gpt-4o",
        "messages": [{"role": "user", "content": content}],
        "max_tokens": 500
    }

    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        json=payload
    )

    if response.status_code != 200:
        return None

    text = response.json()["choices"][0]["message"]["content"]
    
    result = {}
    for line in text.strip().split("\n"):
        if ":" in line:
            key, val = line.split(":", 1)
            result[key.strip()] = val.strip()

    return {
        "technique_score": int(result.get("TECHNIQUE_SCORE", 70)),
        "strength": result.get("STRENGTH", "Good effort on this drill!"),
        "correction": result.get("CORRECTION", "Keep practicing and focus on the coaching points."),
        "body_position": result.get("BODY_POSITION", "Work on staying balanced throughout the drill."),
        "summary": result.get("SUMMARY", "Great work! Keep training hard!")
    }

def analyze_video_from_url(video_url, drill_title, coaching_points, skill_type):
    try:
        response = requests.get(video_url, timeout=30)
        if response.status_code != 200:
            return None
        
        with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as tmp:
            tmp.write(response.content)
            tmp_path = tmp.name

        frames = extract_frames(tmp_path)
        os.unlink(tmp_path)

        if not frames:
            return None

        return analyze_video_frames(frames, drill_title, coaching_points, skill_type)

    except Exception as e:
        print(f"Video analysis error: {e}")
        return None
