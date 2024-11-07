from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
import csv
import io
from sqlalchemy.orm import Session, joinedload
from typing import List
import controller
import schemas
import models
from db import get_db


student_router = APIRouter(
    prefix="/students",
    tags=["students"],
    responses={404: {"description": "Not found"}},
)

# Payload Functions
@student_router.post("/", response_model=schemas.Student)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    return controller.create_student(db=db, student=student)

@student_router.get("/", response_model=List[schemas.Student])
def read_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    students = controller.get_students(db, skip=skip, limit=limit)
    return students

@student_router.get("/{student_id}", response_model=schemas.Student)
def read_student(student_id: int, db: Session = Depends(get_db)):
    db_student = db.query(models.Student).filter(models.Student.id == student_id).options(
        joinedload(models.Student.subjects)
    ).first()
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student

@student_router.put("/{student_id}", response_model=schemas.Student)
def update_student(student_id: int, student: schemas.StudentCreate, db: Session = Depends(get_db)):
    db_student = controller.update_student(db=db, student_id=student_id, student=student)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student

@student_router.delete("/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    db_student = controller.delete_student(db=db, student_id=student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"detail": "Student deleted"}

# CSV Function
@student_router.post("/upload_csv/", response_model=List[schemas.Student])
async def upload_students_csv(
    file: UploadFile = File(...), db: Session = Depends(get_db)
):
    if file.content_type != 'text/csv':
        raise HTTPException(status_code=400, detail="Invalid file type. Expected CSV.")

    content = await file.read()
    reader = csv.DictReader(io.StringIO(content.decode('utf-8')))

    students = []
    for row in reader:
        try:
            student_data = schemas.StudentCreate(
                name=row['name'],
                dob=row['dob']
            )
            db_student = controller.create_student(db=db, student=student_data)
            students.append(db_student)
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=400, detail=f"Error processing row {row}: {str(e)}")

    return students