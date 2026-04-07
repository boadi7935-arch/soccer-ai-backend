from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import players, drills, feedback, assignments
from routes.streaks import router as streaks_router
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Soccer AI Development API",
    description="AI-powered youth soccer player development platform",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(players.router, prefix="/players", tags=["Players"])
app.include_router(drills.router, prefix="/drills", tags=["Drills"])
app.include_router(assignments.router, prefix="/assignments", tags=["Assignments"])
app.include_router(feedback.router, prefix="/feedback", tags=["Feedback"])
app.include_router(streaks_router, prefix="/streaks", tags=["Streaks"])

@app.get("/")
def root():
    return {"message": "Soccer AI API is running ✅"}
