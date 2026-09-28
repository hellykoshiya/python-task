import pytest
from product import validate_price    #Go to product.py and get the validate_price() function.


def test_price_cannot_be_negative():   #unit test function
    with pytest.raises(ValueError) :   #expect the code inside this block to produce a ValueErro
        validate_price(-100)           #assign random value for check


from product import place_order


def test_stock_decreases_when_order_is_placed():
    stock = 10
    quantity = 3

    new_stock = place_order(stock, quantity)

    assert new_stock == 7

   