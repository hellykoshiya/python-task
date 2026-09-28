import pytest
import httpx
from httpx import AsyncClient   #AsyncClient is used for asynchronous HTTP requests.
from main import app


# 1. Test creating a product   
@pytest.mark.asyncio          # #tells test below is an asynchronous test
async def test_create_product():     #POST /products

    product = {
        "title": "Laptop",
        "price": 50000,
        "stock": 10
    }

    async with AsyncClient(        #HTTP request to your FastAPI application, and checking whether the API returns the correct response.
        transport=httpx.ASGITransport(app=app),
        base_url="http://test"
    ) as client:

        response = await client.post(    #Send a POST request to /products with the product dictionary as JSON.
            "/products",
            json=product
        )

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "Laptop"
    assert data["price"] == 50000
    assert data["stock"] == 10


# 2. Test non-existing product
@pytest.mark.asyncio
async def test_non_existing_product():     #GET /products/9999

    async with AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://test"
    ) as client:

        response = await client.get("/products/9999")

    assert response.status_code == 404

    assert response.json()["detail"] == "Product not found"


# 3. Test ordering more than available stock
@pytest.mark.asyncio
async def test_order_more_than_available_stock():     #POST /products/1/order?quantity=10

    async with AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://test"
    ) as client:

        response = await client.post(
            "/products/1/order?quantity=10"
        )

    assert response.status_code == 400

    assert response.json()["detail"] == "Not enough stock"