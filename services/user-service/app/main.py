from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

# Initialize the application
app = FastAPI(
    title="User Service API",
    description="Microservice for handling user data",
    version="1.0.0"
)

# --- IN-MEMORY DATABASE ---
# This list will store users while the pod is running
db_users = [
    {"id": 1, "name": "Admin", "email": "admin@mca.com"},
    {"id": 2, "name": "Test User", "email": "test@mca.com"}
]

# Define the data structure the Frontend is sending
class UserCreate(BaseModel):
    name: str
    email: str

# Health check for Kubernetes
@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "user-service"}

# --- UPDATED ENDPOINTS ---

# 1. Endpoint to ADD a new user (Now saves to the db_users list)
@app.post("/users", status_code=201)
def create_user(user: UserCreate):
    # Create a new user object with a dynamic ID
    new_user = {
        "id": len(db_users) + 1, 
        "name": user.name, 
        "email": user.email
    }
    db_users.append(new_user) # This saves it!
    return {"message": f"User {user.name} synced to Memory", "user": new_user}

# 2. Endpoint to GET all users (Now returns the dynamic list)
@app.get("/users")
def get_all_users():
    return db_users

# 3. Get specific user by ID
@app.get("/users/{user_id}")
def get_user(user_id: int):
    # Search the list for the user
    user = next((u for u in db_users if u["id"] == user_id), None)
    if user:
        return user
    return {"error": "User not found"}