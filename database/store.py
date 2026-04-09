from datetime import datetime
import uuid

def new_id():
    return str(uuid.uuid4())

def now():
    return datetime.utcnow().isoformat()

players_db: dict = {}
drills_db: dict = {}
assignments_db: dict = {}
feedback_db: dict = {}

SEED_DRILLS = [
    {
        "id": new_id(),
        "title": "Wall Pass Receiving",
        "skill_type": "first_touch",
        "level": "beginner",
        "duration_minutes": 10,
        "instructions": "Stand 3 feet from a wall. Pass the ball firmly against the wall and control your first touch by pushing it into open space. Repeat 20 times each foot.",
        "coaching_points": ["Open your hips when receiving", "Push first touch into space", "Stay on your toes", "Use inside and outside of both feet"],
        "demo_video_url": None,
        "equipment_needed": ["ball", "wall"]
    },
    {
        "id": new_id(),
        "title": "Cone Dribbling Slalom",
        "skill_type": "dribbling",
        "level": "beginner",
        "duration_minutes": 12,
        "instructions": "Set up 6 cones in a straight line, 1 yard apart. Dribble through using inside and outside of your foot. Return and repeat 5 times.",
        "coaching_points": ["Keep ball close to your foot", "Use small touches", "Keep head up between cones", "Accelerate out of last cone"],
        "demo_video_url": None,
        "equipment_needed": ["ball", "6 cones"]
    },
    {
        "id": new_id(),
        "title": "Weak Foot Only Passing",
        "skill_type": "weak_foot",
        "level": "beginner",
        "duration_minutes": 10,
        "instructions": "Using only your weak foot, pass the ball against a wall from 5 yards. Focus on locking your ankle and following through. 3 sets of 15 reps.",
        "coaching_points": ["Lock your ankle firm on contact", "Plant foot points at target", "Follow through toward the wall", "Accuracy before speed"],
        "demo_video_url": None,
        "equipment_needed": ["ball", "wall"]
    },
    {
        "id": new_id(),
        "title": "Inside Foot Passing",
        "skill_type": "passing",
        "level": "beginner",
        "duration_minutes": 15,
        "instructions": "With a partner or wall, pass and receive at 8 yards. Focus on accuracy over pace. Alternate feet every 10 passes. Complete 4 sets.",
        "coaching_points": ["Use inside of your foot", "Follow through to target", "First touch sets up next pass"],
        "demo_video_url": None,
        "equipment_needed": ["ball", "wall"]
    },
    {
        "id": new_id(),
        "title": "Ball Mastery Figure 8",
        "skill_type": "ball_mastery",
        "level": "intermediate",
        "duration_minutes": 10,
        "instructions": "Place two cones 2 feet apart. Dribble in a figure-8 pattern using both feet. 5 minutes each direction.",
        "coaching_points": ["Stay low and balanced", "Use all surfaces of both feet", "Keep ball moving", "Build speed gradually"],
        "demo_video_url": None,
        "equipment_needed": ["ball", "2 cones"]
    },
    {
        "id": new_id(),
        "title": "Shooting Inside Foot Finish",
        "skill_type": "shooting",
        "level": "intermediate",
        "duration_minutes": 15,
        "instructions": "Place ball 12 yards from goal. Take 3 touches to set up then shoot with inside foot. Aim for corners. 5 sets of 4 shots.",
        "coaching_points": ["Non-kicking foot beside ball", "Head down through contact", "Drive through the ball", "Follow through toward target"],
        "demo_video_url": None,
        "equipment_needed": ["ball", "goal"]
    },
    {
        "id": new_id(),
        "title": "Agility Ladder Two Feet",
        "skill_type": "agility",
        "level": "beginner",
        "duration_minutes": 10,
        "instructions": "Run through agility ladder using two-feet-per-box pattern. Then one-foot-per-box. Repeat 4 times each. Rest 30 seconds between sets.",
        "coaching_points": ["Stay on your toes", "Pump your arms", "Keep eyes forward", "Land softly"],
        "demo_video_url": None,
        "equipment_needed": ["agility ladder"]
    },
    {
        "id": new_id(),
        "title": "Outside Foot First Touch",
        "skill_type": "first_touch",
        "level": "intermediate",
        "duration_minutes": 12,
        "instructions": "From a wall pass, receive on outside of foot and redirect into space. 15 reps each foot.",
        "coaching_points": ["Cushion the ball", "Redirect into space", "Stay balanced", "Practice both feet equally"],
        "demo_video_url": None,
        "equipment_needed": ["ball", "wall"]
    },
]

def seed_drills():
    for drill in SEED_DRILLS:
        drills_db[drill["id"]] = drill

seed_drills()

# Import and add extra drills
from database.drill_seeds import EXTRA_DRILLS

def seed_extra_drills():
    for drill in EXTRA_DRILLS:
        drill_with_id = {**drill, "id": new_id()}
        drills_db[drill_with_id["id"]] = drill_with_id

seed_extra_drills()

# Attach YouTube video IDs to drills
from database.video_map import VIDEO_MAP
for drill in drills_db.values():
    if drill["title"] in VIDEO_MAP:
        drill["youtube_id"] = VIDEO_MAP[drill["title"]]
