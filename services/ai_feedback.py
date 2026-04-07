import os
import json
from openai import OpenAI

def generate_feedback(player: dict, drill: dict, coach_notes: str = "") -> dict:
    api_key = os.environ.get("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)
    
    prompt = f"""
You are an expert youth soccer coach giving feedback to a young player after they completed a training drill.

PLAYER PROFILE:
- Name: {player.get('name')}
- Age: {player.get('age')} years old
- Position: {player.get('position')}
- Skill Level: {player.get('skill_level')}
- Dominant Foot: {player.get('dominant_foot')}
- Goals: {', '.join(player.get('goals', []))}

DRILL COMPLETED:
- Drill Name: {drill.get('title')}
- Skill Focus: {drill.get('skill_type')}
- Key Coaching Points: {', '.join(drill.get('coaching_points', []))}
- Duration: {drill.get('duration_minutes')} minutes

COACH NOTES: {coach_notes or 'None provided'}

Respond ONLY with a JSON object:
{{
  "score": <integer from 40 to 95>,
  "strength": "<one specific thing they did well>",
  "correction": "<one clear actionable thing to improve>",
  "next_drill_suggestion": "<name of a logical next drill>",
  "summary": "<2-3 sentence encouraging summary>"
}}
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=500
    )
    raw = response.choices[0].message.content.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw)
