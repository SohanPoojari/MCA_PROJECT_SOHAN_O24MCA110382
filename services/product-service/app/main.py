from fastapi import FastAPI

app = FastAPI(title="Product Service API", version="1.0.0")

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "product-service"}

@app.get("/products/{product_id}")
def get_product(product_id: int):
    # Mock Database
    products = {
        1: {"id": 1, "name": "Cloud Architecture Book", "price": 50.0},
        2: {"id": 2, "name": "Microservices Course", "price": 120.0}
    }
    return products.get(product_id, {"error": "Product not found"})