from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Hello from Docker!"}

@app.get("/products")
def get_products():
    return [
        {
            "id": 1,
            "title": "Laptop",
            "price": 50000,
            "stock": 10
        },
        {
            "id": 2,
            "title": "Mobile",
            "price": 20000,
            "stock": 5
        }
    ]