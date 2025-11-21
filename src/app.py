"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from pydantic import EmailStr, ValidationError, BaseModel
import os
from pathlib import Path

# Email validation model
class EmailModel(BaseModel):
    email: EmailStr

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Soccer Team": {
        "description": "Join the school soccer team for training and matches",
        "schedule": "Mondays, Wednesdays, 4:00 PM - 6:00 PM",
        "max_participants": 25,
        "participants": ["lucas@mergington.edu", "mia@mergington.edu"]
    },
    "Basketball Club": {
        "description": "Practice skills, scrimmage, and regional tournaments",
        "schedule": "Tuesdays, Thursdays, 5:00 PM - 7:00 PM",
        "max_participants": 20,
        "participants": ["noah@mergington.edu", "ava@mergington.edu"]
    },
    "Art Club": {
        "description": "Explore drawing, painting, and mixed media projects",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["isabella@mergington.edu", "liam@mergington.edu"]
    },
    "Theater Group": {
        "description": "Acting workshops, rehearsals, and school productions",
        "schedule": "Fridays, 4:00 PM - 6:30 PM",
        "max_participants": 22,
        "participants": ["ava.l@mergington.edu", "ethan@mergington.edu"]
    },
    "Debate Team": {
        "description": "Prepare for regional and national debate competitions",
        "schedule": "Mondays, Thursdays, 3:45 PM - 5:15 PM",
        "max_participants": 16,
        "participants": ["sophia.r@mergington.edu", "mason@mergington.edu"]
    },
    "Science Club": {
        "description": "Hands-on experiments, projects, and science fairs",
        "schedule": "Tuesdays, 4:00 PM - 5:30 PM",
        "max_participants": 20,
        "participants": ["oliver@mergington.edu", "charlotte@mergington.edu"]
    }
}


def validate_email(email: str) -> str:
    """Validate email format using pydantic EmailStr"""
    try:
        # Validate the email
        validated = EmailModel(email=email)
        return str(validated.email)
    except ValidationError:
        raise HTTPException(status_code=400, detail="Invalid email format")


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate email format
    email = validate_email(email)
    
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Validate student is not already signed up
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student already signed up for this activity")
    
    # Validate activity is not full
    if len(activity["participants"]) >= activity["max_participants"]:
        raise HTTPException(status_code=400, detail="Activity is full")
    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/unregister")
def unregister_from_activity(activity_name: str, email: str = Query(...)):
    """Unregister a student from an activity"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")
    activity = activities[activity_name]
    if email not in activity["participants"]:
        raise HTTPException(status_code=404, detail="Participant not found in this activity")
    activity["participants"].remove(email)
    return {"message": f"Unregistered {email} from {activity_name}"}
