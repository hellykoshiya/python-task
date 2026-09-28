def validate_price(price):
    if price < 0:
        raise ValueError("Price cannot be negative")

    return price

def place_order(stock, quantity):
    if quantity > stock:
        raise ValueError("Not enough stock")

    return stock - quantity