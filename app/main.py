from db import engine,Base
from fastapi import FastAPI

# Initialize all MYSQL tables
Base.metadata.create_all(engine)

app = FastAPI()

