import requests
from fastapi import FastAPI, HTTPException
import os

app = FastAPI(title="Order Service API", version="1.0.0")

# Fetching the Docker Network URLs passed by Docker Compose!
USER_SERVICE_URL = os.getenv("USER_SERVICE_URL", "http://user-service:8001")
PRODUCT_SERVICE_URL = os.getenv("PRODUCT_SERVICE_URL", "http://product-service:8002")

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "order-service"}

@app.post("/create-order/{user_id}/{product_id}")
def create_order(user_id: int, product_id: int):
    user_response = requests.get(f"{USER_SERVICE_URL}/users/{user_id}")
    if user_response.status_code != 200:
        raise HTTPException(status_code=404, detail="User not found")
    
    prod_response = requests.get(f"{PRODUCT_SERVICE_URL}/products/{product_id}")
    if prod_response.status_code != 200:
        raise HTTPException(status_code=404, detail="Product not found")

    return {
        "order_id": 999,
        "customer": user_response.json()["username"], 
        "item": prod_response.json()["name"],         
        "price_paid": prod_response.json()["price"],
        "status": "Order Placed Successfully via Docker Network!"
    }