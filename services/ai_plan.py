import os
import json
from dotenv import load_dotenv

load_dotenv()

def generate_weekly_plan(player: dict, available_drills: list) -> dict:
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    drill_summary = "\n".join([f"- {d['title']} ({d['skill_type']}, {d['level']}, {d['duration_minutes']} min)" for d in available_drills])
    prompt = f"""
You are an expert youth soccer coach creating a weekly training plan.
Player: {player.get('name')}, Age: {player.get('age')}, Level: {player.get('skill_level')}
Goals: {', '.join(player.get('goals', []))}
Training Days: {player.get('training_days_per_week')}
Available Drills:
{drill_summary}
Respond ONLY with JSON:
{{"week_theme": "<focus>", "plan": [{{"day": 1, "drill_title": "<title>", "skill_focus": "<skill>", "duration_minutes": <number>, "daily_tip": "<tip>"}}], "weekly_goal": "<goal>", "encouragement": "<message>"}}
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8,
        max_tokens=800
    )
    raw = response.choices[0].message.content.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw)
