from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Order Service API", version="1.0.0")

# --- IN-MEMORY ORDER LEDGER ---
db_orders = []

class OrderCreate(BaseModel):
    user_id: int
    product_id: int
    quantity: int

@app.get("/health")
def health():
    return {"status": "healthy", "service": "order-service"}

# 1. Endpoint to CREATE an order
@app.post("/orders", status_code=201)
def create_order(order: OrderCreate):
    new_order = {
        "id": len(db_orders) + 1,
        "user_id": order.user_id,
        "product_id": order.product_id,
        "quantity": order.quantity,
        "status": "Order Confirmed"
    }
    db_orders.append(new_order)
    return {"message": "Order placed successfully", "order": new_order}

# 2. Endpoint to GET all orders
@app.get("/orders")
def get_orders():
    return db_orders