from pydantic import BaseModel
from .Department import Department

# Subject Schemas

class SubjectBase(BaseModel):
    title: str
    credithours: int
    dept_id: int

class SubjectCreate(SubjectBase):
    pass

class Subject(SubjectBase):
    id: int
    department: Department

    class Config:
        orm_mode = True