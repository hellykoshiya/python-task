#What does my database look like

from sqlalchemy import Column, Integer, Float, String, ForeignKey    #Get tools for creating database columns
from sqlalchemy.orm import declarative_base     #Get the base class for database models

from database import engine     #Get the connection to `quickcart


Base = declarative_base()   #base class for your SQLAlchemy models


class Product(Base):     #Product is a database model    base:class represents a database table.
    __tablename__ = "products"    #Product model represents a database table called products.

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)
    category = Column(String, nullable=False)


class Order(Base):      #Order is a database model
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)


Base.metadata.create_all(bind=engine)   #take all models and create table in database





