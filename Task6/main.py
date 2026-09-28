from fastapi import FastAPI, HTTPException

app = FastAPI()

products = {
    1: {
        "id": 1,
        "title": "Mobile",
        "price": 20000,
        "stock": 5
    }
}


@app.post("/products", status_code=201)           #creates a POST API endpoin
async def create_product(product: dict):          #define asychronous function that can handle FastApi
    return product


@app.get("/products/{product_id}")
async def get_product(product_id: int):
    if product_id not in products:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return products[product_id]


@app.post("/products/{product_id}/order")      
async def order_product(product_id: int, quantity: int):

    if product_id not in products:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    product = products[product_id]

    if quantity > product["stock"]:
        raise HTTPException(
            status_code=400,
            detail="Not enough stock"
        )

    product["stock"] -= quantity

    return product