import json

with open("products.json", "r") as file:
    products = json.load(file)

for product in products:
    print("ID:", product["id"])
    print("Title:", product["title"])
    print("Price:", product["price"])
    print("Stock:", product["stock"])
    print()