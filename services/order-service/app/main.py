import requests
from fastapi import FastAPI, HTTPException

app = FastAPI(title="Order Service API", version="1.0.0")

# These are the local addresses of our other two services
USER_SERVICE_URL = "http://localhost:8001"
PRODUCT_SERVICE_URL = "http://localhost:8002"

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "order-service"}

@app.post("/create-order/{user_id}/{product_id}")
def create_order(user_id: int, product_id: int):
    # 1. Ask User Service: Does this user exist?
    user_response = requests.get(f"{USER_SERVICE_URL}/users/{user_id}")
    if user_response.status_code != 200:
        raise HTTPException(status_code=404, detail="User not found")
    
    # 2. Ask Product Service: Does this product exist?
    prod_response = requests.get(f"{PRODUCT_SERVICE_URL}/products/{product_id}")
    if prod_response.status_code != 200:
        raise HTTPException(status_code=404, detail="Product not found")

    user_data = user_response.json()
    product_data = prod_response.json()

    # 3. If both exist, create a combined response (The "Order")
    return {
        "order_id": 999,
        "customer": user_data["username"],
        "item": product_data["name"],
        "price_paid": product_data["price"],
        "status": "Order Placed Successfully"
    }