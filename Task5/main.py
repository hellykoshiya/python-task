from fastapi import FastAPI,Depends,HTTPException
from fastapi.middleware.cors import CORSMiddleware  #Imports FastAPI's CORS middleware.
from pydantic import BaseModel
# from sqlalchemy.orm import Session


app = FastAPI()

# Frontend origins allowed to access the API
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,           #the FastAPI tool that lets you configure which frontend origins can access your API.
    allow_origins=origins,    #Which frontend websites can access your API
    allow_credentials=True,   #represents a user's authenticated session when making a request.
    allow_methods=["*"],      #Which HTTP methods are allowed (GET, POST, etc.)
    allow_headers=["*"],      # request headers are allowed
)


@app.get("/")
def home():
    return {"message": "FastAPI is running"}


# from fastapi.middleware.cors import CORSMiddleware
# FastAPI:package
# Middlewere:sits between the incoming request and your FastAPI route
# Frontend
#    ↓
# Request
#    ↓
# Middleware
#    ↓
# FastAPI route
#    ↓
# Response

# Cors(Cors Origin Resource sharing):controls which websites/frontend applications are allowed to access your backend API.
# CORSMiddleware:"Use FastAPI's built-in middleware for handling CORS.
# Go to fastapi → middleware → cors and bring me CORSMiddleware.
# fastapi
#   │
#   └── middleware
#         │
#         └── cors
#               │
#               └── CORSMiddleware  ← we import this

# Credentials = information used to maintain/prove a user's login/session.



class Product(BaseModel):
    title: str
    price: float
    stock: int
    category: str

products = [
    {
        "id": 1,
        "title": "Laptop",
        "price": 50000,
        "stock": 10,
        "category": "Electronic"
    },
    {
        "id": 2,
        "title": "Mouse",
        "price": 800,
        "stock": 20,
        "category": "Electronic"

    }
]


@app.get("/products")
def get_products():
    return products

@app.post("/products")
def create_product(product: Product):

    # Generate new ID
    new_id = len(products) + 1

    # Create new product
    new_product = {
        "id": new_id,
        "title": product.title,
        "price": product.price,
        "stock": product.stock,
        "category": product.category
    }

    # Add product to list
    products.append(new_product)

    # Send new product back to frontend
    return new_product



@app.post("/orders")
def create_order(product_id: int):

    # Find product

    product = next(
        (
            p
            for p in products
            if p["id"] == product_id
        ),
        None
    )


    # Product doesn't exist

    if product is None:

        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )


    # Product is out of stock

    if product["stock"] <= 0:

        raise HTTPException(
            status_code=400,
            detail="Out of stock"
        )


    # Reduce stock

    product["stock"] -= 1


    # Return result

    return {

        "message":
            "Purchase successful!",

        "product_id":
            product["id"],

        "remaining_stock":
            product["stock"]

    }