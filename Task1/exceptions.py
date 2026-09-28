class ProductError(Exception):
    """Base class for product-related errors."""


class InvalidPriceError(ProductError):
    def __init__(self, title, price):
        self.title = title
        self.price = price
        super().__init__(f"Invalid price for '{title}': {price!r}")


class ProductOutOfStockError(ProductError):
    def __init__(self, title: str, stock: int):
        self.title = title
        self.stock = stock
        super().__init__(f"'{title}' is out of stock (stock={stock})")
