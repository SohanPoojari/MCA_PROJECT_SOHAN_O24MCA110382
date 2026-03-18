from fastapi import FastAPI

# Initialize the application
app = FastAPI(
    title="User Service API",
    description="Microservice for handling user data",
    version="1.0.0"
)

# Root endpoint for health checks (Crucial for Kubernetes later)
@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "user-service"}

# Mock User Database endpoint
@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {
        "id": user_id,
        "username": f"mca_student_{user_id}",
        "email": f"student{user_id}@university.edu",
        "role": "admin"
    }