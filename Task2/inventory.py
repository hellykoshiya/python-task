from sqlalchemy.orm import Session

from database import engine
from models import Product, Category
from inventory_reader import read_in_batches


def validate_row(row, categories):

    try:
        product_id = int(row["id"])
        title = row["title"].strip()
        price = float(row["price"])
        stock = int(row["stock"])
        category_name = row["category"].strip()

        if not title:
            return None

        if price < 0:
            return None

        if stock < 0:
            return None

        if category_name not in categories:
            return None

        category_id = categories[category_name]

        return Product(
            id=product_id,
            title=title,
            price=price,
            stock=stock,
            category_id=category_id
        )

    except (ValueError, TypeError):
        return None


with Session(engine) as session:

    categories = {}

    for category in session.query(Category).all():
        categories[category.name] = category.id

    total_rows = 0
    valid_rows = 0
    invalid_rows = 0
    duplicate_rows = 0

    for batch in read_in_batches("inventory.csv", batch_size=100):

        products = []

        for row in batch:

            total_rows += 1

            product = validate_row(row, categories)

            if product is None:
                invalid_rows += 1
                continue

            existing_product = session.get(Product, product.id)

            if existing_product:
                duplicate_rows += 1
                continue

            products.append(product)
            valid_rows += 1

        if products:
            session.add_all(products)
            session.commit()

    print("Import completed!")
    print("Total rows:", total_rows)
    print("Valid rows:", valid_rows)
    print("Invalid rows:", invalid_rows)
    print("Duplicate rows skipped:", duplicate_rows)