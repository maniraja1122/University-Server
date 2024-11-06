from pydantic import BaseModel

# Enrollment Schemas

class EnrollmentBase(BaseModel):
    student_id: int
    subject_id: int

class EnrollmentCreate(EnrollmentBase):
    pass

class Enrollment(EnrollmentBase):
    id: int

    class Config:
        orm_mode = True