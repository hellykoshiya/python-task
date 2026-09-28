import json

from pydantic import ValidationError

from exceptions import ProductOutOfStockError
from Product import Product

# from exceptions import ProductFileNotFoundError


def load_products(filepath: str) -> list[Product]:
    with open(filepath, "r") as f:
        raw_data = json.load(f)

    valid_products = []

    for item in raw_data:
        try:
            product = Product(**item)  # Pydantic validates types + price > 0

            if product.stock <= 0:
                raise ProductOutOfStockError(product.title, product.stock)
                # raise ProductOutOfStockError(
                #     f"'{product.title}' is out of stock (stock={product.stock})"
                # )

            valid_products.append(product)

        except ValidationError as e:
            print(f"Skipping invalid product {item}: {e}")

        except ProductOutOfStockError as e:
            print(f"Stock issue: {e}")

    return valid_products


if __name__ == "__main__":
    products = load_products("products.json")
    print(f"\nLoaded {len(products)} valid, in-stock products:")
    for p in products:
        print(f" - {p.title}: ₹{p.price} (stock: {p.stock}, category: {p.categary})")
