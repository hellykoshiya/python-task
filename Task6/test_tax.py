from tax import calculate_tax


def test_tax_calculation():
    result = calculate_tax(1000, 18)

    assert result == 180