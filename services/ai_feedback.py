import os
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def generate_feedback(player, drill, coach_notes="", video_analysis=None):
    
    video_context = ""
    if video_analysis:
        video_context = f"""
VIDEO ANALYSIS RESULTS:
- Technique Score from video: {video_analysis.get('technique_score', 'N/A')}
- What was observed (strength): {video_analysis.get('strength', 'N/A')}
- What needs work: {video_analysis.get('correction', 'N/A')}
- Body position: {video_analysis.get('body_position', 'N/A')}

Use these video observations to make your feedback more specific and accurate.
"""

    prompt = f"""You are an expert youth soccer coach giving feedback to a young player.

PLAYER INFO:
- Name: {player['name']}
- Age: {player['age']}
- Position: {player['position']}
- Skill Level: {player['skill_level']}

DRILL COMPLETED:
- Title: {drill['title']}
- Skill Type: {drill['skill_type']}
- Coaching Points: {', '.join(drill.get('coaching_points', []))}

COACH NOTES: {coach_notes or 'No additional notes'}

{video_context}

Provide coaching feedback in this exact JSON format:
{{
  "score": <number 0-100>,
  "strength": "<one specific thing they did well>",
  "correction": "<one specific actionable improvement>",
  "next_drill_suggestion": "<name of a good next drill to try>",
  "summary": "<encouraging 1-2 sentence summary for a young player>"
}}

Be encouraging, specific, and age-appropriate. If video analysis is provided, reference what you saw.
Return ONLY the JSON, no other text."""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300
    )

    import json
    text = response.choices[0].message.content.strip()
    text = text.replace("```json", "").replace("```", "").strip()
    result = json.loads(text)
    return result
