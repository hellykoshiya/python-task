import json

with open("products.json", "r") as file:
    products = json.load(file)

print(products)
