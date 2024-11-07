from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
import csv
import io
from sqlalchemy.orm import Session
from typing import List
import controller
import schemas
import models
from db import get_db

subjects_taught_router = APIRouter(
    prefix="/subjects_taught",
    tags=["subjects_taught"],
    responses={404: {"description": "Not found"}},
)

# Payload Functions
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

# CSV Function
@subjects_taught_router.post("/upload_csv/", response_model=List[schemas.SubjectTaught])
async def upload_subjects_taught_csv(
    file: UploadFile = File(...), db: Session = Depends(get_db)
):
    if file.content_type != 'text/csv':
        raise HTTPException(status_code=400, detail="Invalid file type. Expected CSV.")

    content = await file.read()
    reader = csv.DictReader(io.StringIO(content.decode('utf-8')))

    subjects_taught = []
    for row in reader:
        try:
            # Find teacher by name
            teacher_name = row['teacher_name']
            db_teacher = db.query(models.Teacher).filter(models.Teacher.name == teacher_name).first()
            if not db_teacher:
                raise HTTPException(status_code=400, detail=f"Teacher '{teacher_name}' not found.")

            # Find subject by title
            subject_title = row['subject_title']
            db_subject = db.query(models.Subject).filter(models.Subject.title == subject_title).first()
            if not db_subject:
                raise HTTPException(status_code=400, detail=f"Subject '{subject_title}' not found.")

            subject_taught_data = schemas.SubjectTaughtCreate(
                teacher_id=db_teacher.id,
                subject_id=db_subject.id
            )
            db_subject_taught = controller.create_subject_taught(db=db, subject_taught=subject_taught_data)
            subjects_taught.append(db_subject_taught)
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=400, detail=f"Error processing row {row}: {str(e)}")

    return subjects_taught