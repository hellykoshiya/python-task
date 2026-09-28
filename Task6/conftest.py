import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker  #what your Python code uses to communicate with the database.


@pytest.fixture    # tells pytest that db() is a reusable setup function, and pytest can automatically give its result to any test that asks for db.
def db():
    # Temporary in-memory database
    engine = create_engine("sqlite:///:memory:")   #Create the SQLite database only in RAM (memory).

    # Create a database session
    SessionLocal = sessionmaker(bind=engine)    #Create sessions that use this database.
    session = SessionLocal()

    # Give the database session to the test
    yield session

    # Clean up after the test
    session.close()  #session close
    engine.dispose() #close database connection by engine