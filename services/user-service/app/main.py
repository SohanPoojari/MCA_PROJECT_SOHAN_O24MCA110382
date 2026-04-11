from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

# Initialize the application
app = FastAPI(
    title="User Service API",
    description="Microservice for handling user data",
    version="1.0.0"
)

# Define the data structure the Frontend is sending
class UserCreate(BaseModel):
    name: str
    email: str

# Root endpoint for health checks (Crucial for Kubernetes)
@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "user-service"}

# --- THE MISSING DOORS ---

# 1. Endpoint to ADD a new user (This fixes the 404 Error!)
# Notice status_code=201, which is exactly what your Streamlit app checks for to show balloons!
@app.post("/users", status_code=201)
def create_user(user: UserCreate):
    # In a real production app, you would insert this into Azure SQL here.
    # For now, we return a success response so the Frontend knows it worked.
    return {"message": f"User {user.name} created successfully", "email": user.email}

# 2. Endpoint to GET all users (This fixes the "Master Registry" tab)
@app.get("/users")
def get_all_users():
    # Mock data to prove the Frontend table works
    return [
        {"id": 1, "name": "Admin", "email": "admin@mca.com"},
        {"id": 2, "name": "Test User", "email": "test@mca.com"}
    ]

# Original Mock User Database endpoint
@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {
        "id": user_id,
        "name": f"mca_student_{user_id}",
        "email": f"student{user_id}@university.edu",
        "role": "admin"
    }