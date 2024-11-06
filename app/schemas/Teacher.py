from pydantic import BaseModel
from typing import List
from .Subject import Subject

# Teacher Schemas

class TeacherBase(BaseModel):
    name: str
    contact: str

class TeacherCreate(TeacherBase):
    pass

class Teacher(TeacherBase):
    id: int
    subjects: List[Subject] = []

    class Config:
        orm_mode = True