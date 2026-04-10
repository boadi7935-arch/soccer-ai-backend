from pydantic import BaseModel
from typing import Optional, List
from enum import Enum

class Position(str, Enum):
    goalkeeper = "goalkeeper"
    defender = "defender"
    midfielder = "midfielder"
    winger = "winger"
    forward = "forward"

class SkillLevel(str, Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"

class SkillType(str, Enum):
    dribbling = "dribbling"
    passing = "passing"
    first_touch = "first_touch"
    weak_foot = "weak_foot"
    shooting = "shooting"
    ball_mastery = "ball_mastery"
    agility = "agility"

class DominantFoot(str, Enum):
    left = "left"
    right = "right"

class PlayerCreate(BaseModel):
    name: str
    age: int
    position: Position
    dominant_foot: DominantFoot
    skill_level: SkillLevel
    goals: List[SkillType]
    training_days_per_week: int
    parent_email: Optional[str] = None
    coach_id: Optional[str] = None

class PlayerResponse(PlayerCreate):
    id: str
    created_at: str
    class Config:
        from_attributes = True

class DrillCreate(BaseModel):
    title: str
    skill_type: SkillType
    level: SkillLevel
    duration_minutes: int
    instructions: str
    coaching_points: List[str]
    demo_video_url: Optional[str] = None
    equipment_needed: Optional[List[str]] = []

class DrillResponse(DrillCreate):
    id: str
    class Config:
        from_attributes = True

class AssignmentCreate(BaseModel):
    player_id: str
    drill_id: str
    due_date: Optional[str] = None
    notes: Optional[str] = None

class AssignmentResponse(AssignmentCreate):
    id: str
    status: str
    assigned_date: str
    class Config:
        from_attributes = True

class FeedbackCreate(BaseModel):
    assignment_id: str
    player_id: str
    drill_id: str
    video_url: Optional[str] = None
    coach_notes: Optional[str] = None

class FeedbackResponse(BaseModel):
    id: str
    assignment_id: str
    score: int
    strength: str
    correction: str
    next_drill_suggestion: str
    summary: str
    coach_approved: bool = False
    class Config:
        from_attributes = True

class WeeklyPlanRequest(BaseModel):
    player_id: str
    focus_skills: Optional[List[SkillType]] = None

class PlayerUpdate(BaseModel):
    avatar_type: Optional[str] = None
    avatar_url: Optional[str] = None
    avatar_emoji: Optional[str] = None
    avatar_color: Optional[str] = None
    avatar_label: Optional[str] = None
