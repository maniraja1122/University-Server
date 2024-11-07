from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
import csv
import io
from sqlalchemy.orm import Session
from typing import List
import controller
import schemas
import models
from db import get_db

subject_router = APIRouter(
    prefix="/subjects",
    tags=["subjects"],
    responses={404: {"description": "Not found"}},
)

@subject_router.post("/", response_model=schemas.Subject)
def create_subject(subject: schemas.SubjectCreate, db: Session = Depends(get_db)):
    db_department = controller.get_department(db=db, department_id=subject.dept_id)
    if db_department is None:
        raise HTTPException(status_code=404, detail="Department not found")
    return controller.create_subject(db=db, subject=subject)

@subject_router.get("/", response_model=List[schemas.Subject])
def read_subjects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    subjects = controller.get_subjects(db, skip=skip, limit=limit)
    return subjects

@subject_router.get("/{subject_id}", response_model=schemas.Subject)
def read_subject(subject_id: int, db: Session = Depends(get_db)):
    db_subject = controller.get_subject(db=db, subject_id=subject_id)
    if db_subject is None:
        raise HTTPException(status_code=404, detail="Subject not found")
    return db_subject

@subject_router.put("/{subject_id}", response_model=schemas.Subject)
def update_subject(subject_id: int, subject: schemas.SubjectCreate, db: Session = Depends(get_db)):
    db_subject = controller.update_subject(db=db, subject_id=subject_id, subject=subject)
    if db_subject is None:
        raise HTTPException(status_code=404, detail="Subject not found")
    return db_subject

@subject_router.delete("/{subject_id}")
def delete_subject(subject_id: int, db: Session = Depends(get_db)):
    db_subject = controller.delete_subject(db=db, subject_id=subject_id)
    if db_subject is None:
        raise HTTPException(status_code=404, detail="Subject not found")
    return {"detail": "Subject deleted"}

@subject_router.post("/upload_csv/", response_model=List[schemas.Subject])
async def upload_subjects_csv(
    file: UploadFile = File(...), db: Session = Depends(get_db)
):
    if file.content_type != 'text/csv':
        raise HTTPException(status_code=400, detail="Invalid file type. Expected CSV.")

    content = await file.read()
    reader = csv.DictReader(io.StringIO(content.decode('utf-8')))

    subjects = []
    for row in reader:
        try:
            # Find or create department by name
            dept_name = row['dept_name']
            db_department = db.query(models.Department).filter(models.Department.name == dept_name).first()
            if not db_department:
                # Create the department if it doesn't exist
                department_data = schemas.DepartmentCreate(name=dept_name)
                db_department = controller.create_department(db, department_data)

            subject_data = schemas.SubjectCreate(
                title=row['title'],
                credithours=int(row['credithours']),
                dept_id=db_department.id
            )
            db_subject = controller.create_subject(db=db, subject=subject_data)
            subjects.append(db_subject)
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=400, detail=f"Error processing row {row}: {str(e)}")

    return subjects