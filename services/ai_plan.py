import os
import json
from openai import OpenAI

def generate_weekly_plan(player: dict, available_drills: list) -> dict:
    api_key = os.environ.get("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)
    
    drill_summary = "\n".join([
        f"- {d['title']} ({d['skill_type']}, {d['level']}, {d['duration_minutes']} min)"
        for d in available_drills
    ])

    prompt = f"""
You are an expert youth soccer development coach creating a weekly training plan.

PLAYER PROFILE:
- Name: {player.get('name')}
- Age: {player.get('age')} years old
- Position: {player.get('position')}
- Skill Level: {player.get('skill_level')}
- Dominant Foot: {player.get('dominant_foot')}
- Goals: {', '.join(player.get('goals', []))}
- Training Days Per Week: {player.get('training_days_per_week')}

AVAILABLE DRILLS:
{drill_summary}

Create a {player.get('training_days_per_week')}-day training plan for this player.
Respond ONLY with a JSON object in this exact format:
{{
  "week_theme": "<overarching focus for this week>",
  "plan": [
    {{
      "day": 1,
      "drill_title": "<drill name from the list above>",
      "skill_focus": "<skill type>",
      "duration_minutes": <number>,
      "daily_tip": "<one motivating tip for that session>"
    }}
  ],
  "weekly_goal": "<one measurable thing the player should achieve this week>",
  "encouragement": "<a personal age-appropriate motivating message>"
}}
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
