from db import init_db
from fastapi import FastAPI
from routers import *


app = FastAPI(
    title="University API",
    description="An API for managing university data",
    version="1.0.0",
)

init_db()

# Include routers
app.include_router(student_router)
app.include_router(teacher_router)
app.include_router(department_router)
app.include_router(subject_router)
app.include_router(enrollment_router)
app.include_router(subjects_taught_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the University API"}