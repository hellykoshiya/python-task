from sqlalchemy.orm import Session

from database import engine
from models import Category, Product


# Open database session
with Session(engine) as session:

    # Create 5 categories
    electronics = Category(name="Electronics")
    clothing = Category(name="Clothing")
    books = Category(name="Books")
    groceries = Category(name="Groceries")
    sports = Category(name="Sports")

    # Add categories to session
    session.add_all([
        electronics,
        clothing,
        books,
        groceries,
        sports
    ])

    # Create 20 products
    products = [
        Product(title="Laptop", price=60000, stock=10, category=electronics),
        Product(title="Mobile Phone", price=25000, stock=20, category=electronics),
        Product(title="Headphones", price=2000, stock=30, category=electronics),
        Product(title="Keyboard", price=1500, stock=15, category=electronics),

        Product(title="T-Shirt", price=800, stock=25, category=clothing),
        Product(title="Jeans", price=1500, stock=20, category=clothing),
        Product(title="Jacket", price=2500, stock=10, category=clothing),
        Product(title="Shoes", price=2000, stock=18, category=clothing),

        Product(title="Python Book", price=500, stock=12, category=books),
        Product(title="Java Book", price=600, stock=10, category=books),
        Product(title="SQL Book", price=450, stock=15, category=books),
        Product(title="AI Book", price=700, stock=8, category=books),

        Product(title="Rice", price=600, stock=30, category=groceries),
        Product(title="Wheat", price=500, stock=25, category=groceries),
        Product(title="Milk", price=60, stock=40, category=groceries),
        Product(title="Sugar", price=50, stock=35, category=groceries),

        Product(title="Cricket Bat", price=3000, stock=5, category=sports),
        Product(title="Football", price=1200, stock=10, category=sports),
        Product(title="Tennis Racket", price=2500, stock=7, category=sports),
        Product(title="Basketball", price=1500, stock=9, category=sports),
    ]

    # Add products
    session.add_all(products)

    # Save everything to database
    session.commit()

    print("5 categories and 20 products added successfully!")