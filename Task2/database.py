from sqlalchemy import create_engine

DATABASE_URL = "sqlite:///products.db"

engine = create_engine(DATABASE_URL)

print("Database connection created!")