from pydantic import BaseModel
from typing import List
from datetime import date
from .Subject import Subject

# Student Schemas

class StudentBase(BaseModel):
    name: str
    dob: date

class StudentCreate(StudentBase):
    pass

class Student(StudentBase):
    id: int
    subjects: List[Subject] = []

    class Config:
        orm_mode = True