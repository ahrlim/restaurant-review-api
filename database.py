from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./restaurant-review-api.db"

# engine is our connection to the database
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

# create a session (= a transaction with the database), each request has its own session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass

# a dependency function provides sessions to our routes
# use it with context manager
def get_db():
    with SessionLocal() as db:
        yield db

