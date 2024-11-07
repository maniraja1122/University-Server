import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

# This will import the variables from local .env file, if no variables are passed in the environment then as an alternative we can use this.
# load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

def init_db():
    # Initialize all MYSQL tables
    Base.metadata.create_all(engine)

# Function for getting a local session to perform some query/operation on the MYSQL DB, it will be locally injected for the functions in the controller.
# It will also manage closing the database connection for each function.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()