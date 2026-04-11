from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Product Service API", version="1.0.0")

# --- IN-MEMORY STOCK LEDGER ---
db_products = [
    {"id": 1, "name": "Cloud Instance", "price": 50.0, "stock": 10},
    {"id": 2, "name": "Storage Bucket", "price": 10.0, "stock": 100}
]

class ProductCreate(BaseModel):
    name: str
    price: float
    stock: int

@app.get("/health")
def health():
    return {"status": "healthy", "service": "product-service"}

# 1. Endpoint to ADD a product (Fixes the silent failure)
@app.post("/products", status_code=201)
def add_product(product: ProductCreate):
    new_prod = {
        "id": len(db_products) + 1,
        "name": product.name,
        "price": product.price,
        "stock": product.stock
    }
    db_products.append(new_prod)
    return {"message": "Product added to Inventory", "product": new_prod}

# 2. Endpoint to GET all products (For the Stock Ledger tab)
@app.get("/products")
def get_products():
    return db_products