from sqlalchemy import text

def test_addition():
    assert 2 + 3 == 5   #Check whether this statement is true.


def test_subtraction():
    assert 10 - 4 == 6


def test_multiplication():
    assert 5 * 2 == 10


def test_division():
    assert 10 / 2 == 5

def test_database_is_empty(db):
    result = db.execute(text("SELECT 1"))
    assert result.scalar() == 1

