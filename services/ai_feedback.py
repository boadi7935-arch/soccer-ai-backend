import os
import json
from dotenv import load_dotenv

load_dotenv()

def generate_feedback(player: dict, drill: dict, coach_notes: str = "") -> dict:
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = f"""
You are an expert youth soccer coach giving feedback to a young player.
Player: {player.get('name')}, Age: {player.get('age')}, Level: {player.get('skill_level')}
Drill: {drill.get('title')} - Focus: {drill.get('skill_type')}
Coach Notes: {coach_notes or 'None'}
Respond ONLY with JSON:
{{"score": <40-95>, "strength": "<what they did well>", "correction": "<one thing to fix>", "next_drill_suggestion": "<next drill>", "summary": "<2-3 encouraging sentences>"}}
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
