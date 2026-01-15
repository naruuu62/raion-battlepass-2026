from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# setup the database connection
DATABASE_URL = "postgresql://postgres:09072511@localhost:5432/fluttermusicapp"

# create the database engine and session provide by SQLAlchemy
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
)

# create a database session
db = SessionLocal()