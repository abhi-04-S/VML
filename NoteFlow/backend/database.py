from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# We use SQLite as our database, which stores data in a simple file.
SQLALCHEMY_DATABASE_URL = "sqlite:///./notes.db"

# Create the SQLAlchemy engine that will communicate with SQLite.
# connect_args={"check_same_thread": False} is required for SQLite in FastAPI.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# SessionLocal class will create actual database sessions for our requests.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class that our database models will inherit from.
Base = declarative_base()

# Dependency function to get the database session for each request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
