from pydantic import BaseModel, Field


class Product(BaseModel):
    id: int
    title: str
    price: float = Field(gt=0)
    stock: int
    categary: str


product = Product(id=1, title="mobile", price=55000, stock=5, categary="Electrition")
print(product)
