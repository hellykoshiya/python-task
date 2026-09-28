#How do I connect to the database?"

from sqlalchemy import create_engine #creates a connection between Python and the database.
from sqlalchemy.orm import sessionmaker  #creates database sessions that allow us to read/write data.

DATABASE_URL = "sqlite:///./quickcart.db"   #Tells SQLAlchemy which database to use.

engine = create_engine(       #Creates the database engine/connection configuration.
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(        #Creates database sessions.
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db():       #Creates a session, gives it to your API route, and closes it afterward
    db = SessionLocal()     #create/open a database session

    try:
        yield db       #give it to the API route
    finally:
        db.close()     #close the session when the request is finished