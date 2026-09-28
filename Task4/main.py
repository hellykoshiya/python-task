from fastapi import FastAPI, Depends, HTTPException     
from pydantic import BaseModel, Field    
from sqlalchemy.orm import Session

from database import get_db
from models import Product, Order


app = FastAPI()     #Used to create your FastAPI application


# ==========================================
# Pydantic Models
# ==========================================

class ProductCreate(BaseModel):     #Pydantic request model
    title: str
    price: float = Field(ge=0)
    stock: int = Field(ge=0)
    category: str


class StockUpdate(BaseModel):
    stock: int = Field(ge=0)


class OrderCreate(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)


# ==========================================
# HOME
# ==========================================

@app.get("/")    #creates a GET endpoint
def home():
    return {
        "message": "QuickCart API is running"
    }


# ==========================================
# HEALTH CHECK
# ==========================================

@app.get("/health")     #This is used to check whether your API is running
def health_check():
    return {
        "status": "ok"
    }


# ==========================================
# 1. POST /products
# Add new product
# ==========================================

@app.post("/products")
def create_product(
    product_data: ProductCreate,     #This contains the JSON sent by the user
    db: Session = Depends(get_db)    #get_db():FastAPI, give this function a database
):
    product = Product(
        title=product_data.title,
        price=product_data.price,
        stock=product_data.stock,
        category=product_data.category
    )

    db.add(product)      #Prepare product to be saved
    db.commit()     #saves change to database
    db.refresh(product)   #Get the latest saved data back into the Python object

    return product

#Create → Save → Refresh → Return ✅

# ==========================================
# 2. GET /products/{id}
# Get product by ID
# ==========================================

@app.get("/products/{product_id}")      
def get_product(
    product_id: int,       #id from url
    db: Session = Depends(get_db)    
):
    product = (            #for search
        db.query(Product)
        .filter(Product.id == product_id)
        .first()             #give first matching product
    )

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product


# ==========================================
# 3. PATCH /products/{id}/stock
# Update stock
# ==========================================

@app.patch("/products/{product_id}/stock")
def update_stock(
    product_id: int,
    stock_data: StockUpdate,
    db: Session = Depends(get_db)
):
    product = (
        db.query(Product)
        .filter(Product.id == product_id)
        .first()
    )

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    product.stock = stock_data.stock

    db.commit()
    db.refresh(product)

    return product


# ==========================================
# 4. POST /orders
# Place order
# ==========================================

@app.post("/orders")
def create_order(
    order_data: OrderCreate,
    db: Session = Depends(get_db)
):
    # Find product
    product = (
        db.query(Product)
        .filter(Product.id == order_data.product_id)
        .first()
    )

    # Product does not exist
    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    # Check stock
    if product.stock < order_data.quantity:
        raise HTTPException(
            status_code=400,
            detail="Not enough stock"
        )

    # Decrease stock
    product.stock -= order_data.quantity

    # Create order
    order = Order(
        product_id=order_data.product_id,
        quantity=order_data.quantity
    )

    db.add(order)
    db.commit()
    db.refresh(order)

    return {
        "message": "Order placed successfully",
        "order": order,
        "remaining_stock": product.stock
    }




# FastAPI - Used to create your API application
# Depends - Used for dependencies
# HTTPException - Used when you want to return an error

# Pydantic - used for validating the data coming into your API
# Basemodel - to create request model

# Session - represents a database session.



#                     QUICKCART                                     

# Frontend / Swagger
#         ↓
#      FastAPI
#         ↓
#     Route/API
#         ↓
#     SQLAlchemy
#         ↓
#      SQLite DB



# GET /products/5

# ↓

# FastAPI receives the request

# ↓

# Your get_product() function runs

# ↓

# SQLAlchemy searches the database

# ↓

# Product is found

# ↓

# FastAPI returns JSON