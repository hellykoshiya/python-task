from sqlalchemy.orm import Session

from database import engine
from models import Product


def get_product_by_id(product_id):
    with Session(engine) as session:

        product = session.get(Product, product_id)

        return product


def filter_by_price_range(min_price, max_price):
    with Session(engine) as session:

        products = (
            session.query(Product)
            .filter(
                Product.price >= min_price,
                Product.price <= max_price
            )
            .all()
        )

        return products


# Test get_product_by_id()
product = get_product_by_id(21)

if product:
    print("Product found:")
    print("ID:", product.id)
    print("Title:", product.title)
    print("Price:", product.price)
    print("Stock:", product.stock)
else:
    print("Product not found")


# Test filter_by_price_range()
products = filter_by_price_range(1000, 5000)

print("\nProducts between ₹1000 and ₹5000:")

for product in products:
    print(
        product.id,
        product.title,
        product.price,
        product.stock
    )