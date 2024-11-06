from pydantic import BaseModel

# SubjectsTaught Schemas

class SubjectTaughtBase(BaseModel):
    teacher_id: int
    subject_id: int

class SubjectTaughtCreate(SubjectTaughtBase):
    pass

class SubjectTaught(SubjectTaughtBase):
    id: int

    class Config:
        orm_mode = True