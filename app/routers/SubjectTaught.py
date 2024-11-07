from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import controller
import schemas
from db import get_db

subjects_taught_router = APIRouter(
    prefix="/subjects_taught",
    tags=["subjects_taught"],
    responses={404: {"description": "Not found"}},
)

@subjects_taught_router.post("/", response_model=schemas.SubjectTaught)
def create_subject_taught(subject_taught: schemas.SubjectTaughtCreate, db: Session = Depends(get_db)):
    db_teacher = controller.get_teacher(db, teacher_id=subject_taught.teacher_id)
    db_subject = controller.get_subject(db, subject_id=subject_taught.subject_id)
    if db_teacher is None:
        raise HTTPException(status_code=404, detail="Teacher not found")
    if db_subject is None:
        raise HTTPException(status_code=404, detail="Subject not found")
    return controller.create_subject_taught(db=db, subject_taught=subject_taught)

@subjects_taught_router.get("/", response_model=List[schemas.SubjectTaught])
def read_subjects_taught(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    subjects_taught = controller.get_subjects_taught(db, skip=skip, limit=limit)
    return subjects_taught

@subjects_taught_router.delete("/{subject_taught_id}")
def delete_subject_taught(subject_taught_id: int, db: Session = Depends(get_db)):
    db_subject_taught = controller.delete_subject_taught(db=db, subject_taught_id=subject_taught_id)
    if db_subject_taught is None:
        raise HTTPException(status_code=404, detail="SubjectTaught not found")
    return {"detail": "SubjectTaught deleted"}