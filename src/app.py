
"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Dependency injection for activities
from src.data import activities
from fastapi import Depends

def get_activities_data():
    return activities

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")


# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")

@app.get("/activities")
def get_activities_endpoint(data=Depends(get_activities_data)):
    return data

@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str, data=Depends(get_activities_data)):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in data:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = data[activity_name]

    # Validate student is not already signed up
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student is already signed up")
    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}

@app.delete("/activities/{activity_name}/unregister")
def unregister_from_activity(activity_name: str, email: str, data=Depends(get_activities_data)):
    """Unregister a student from an activity"""
    if activity_name not in data:
        raise HTTPException(status_code=404, detail="Activity not found")
    activity = data[activity_name]
    if email not in activity["participants"]:
        raise HTTPException(status_code=404, detail="Participant not found in this activity")
    activity["participants"].remove(email)
    return {"message": f"Unregistered {email} from {activity_name}"}
