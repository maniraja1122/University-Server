from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import controller
import schemas
from db import get_db

enrollment_router = APIRouter(
    prefix="/enrollments",
    tags=["enrollments"],
    responses={404: {"description": "Not found"}},
)

@enrollment_router.post("/", response_model=schemas.Enrollment)
def create_enrollment(enrollment: schemas.EnrollmentCreate, db: Session = Depends(get_db)):
    db_student = controller.get_student(db, student_id=enrollment.student_id)
    db_subject = controller.get_subject(db, subject_id=enrollment.subject_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    if db_subject is None:
        raise HTTPException(status_code=404, detail="Subject not found")
    return controller.create_enrollment(db=db, enrollment=enrollment)

@enrollment_router.get("/", response_model=List[schemas.Enrollment])
def read_enrollments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    enrollments = controller.get_enrollments(db, skip=skip, limit=limit)
    return enrollments

@enrollment_router.delete("/{enrollment_id}")
def delete_enrollment(enrollment_id: int, db: Session = Depends(get_db)):
    db_enrollment = controller.delete_enrollment(db=db, enrollment_id=enrollment_id)
    if db_enrollment is None:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    return {"detail": "Enrollment deleted"}