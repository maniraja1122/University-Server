from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
import csv
import io
from sqlalchemy.orm import Session
from typing import List
import controller
import schemas
import models
from db import get_db

enrollment_router = APIRouter(
    prefix="/enrollments",
    tags=["enrollments"],
    responses={404: {"description": "Not found"}},
)

# Payload Functions
# Create Enrollment Based on Schema POST Request
@enrollment_router.post("/", response_model=schemas.Enrollment)
def create_enrollment(enrollment: schemas.EnrollmentCreate, db: Session = Depends(get_db)):
    db_student = controller.get_student(db, student_id=enrollment.student_id)
    db_subject = controller.get_subject(db, subject_id=enrollment.subject_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    if db_subject is None:
        raise HTTPException(status_code=404, detail="Subject not found")
    return controller.create_enrollment(db=db, enrollment=enrollment)

# Get Multiple Enrollments
@enrollment_router.get("/", response_model=List[schemas.Enrollment])
def read_enrollments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    enrollments = controller.get_enrollments(db, skip=skip, limit=limit)
    return enrollments

# Delete Enrollment based on ID
@enrollment_router.delete("/{enrollment_id}")
def delete_enrollment(enrollment_id: int, db: Session = Depends(get_db)):
    db_enrollment = controller.delete_enrollment(db=db, enrollment_id=enrollment_id)
    if db_enrollment is None:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    return {"detail": "Enrollment deleted"}

# CSV Function
@enrollment_router.post("/upload_csv/", response_model=List[schemas.Enrollment])
async def upload_enrollments_csv(
    file: UploadFile = File(...), db: Session = Depends(get_db)
):
    if file.content_type != 'text/csv':
        raise HTTPException(status_code=400, detail="Invalid file type. Expected CSV.")

    content = await file.read()
    reader = csv.DictReader(io.StringIO(content.decode('utf-8')))

    enrollments = []
    for row in reader:
        try:
            # Find student by name
            student_name = row['student_name']
            db_student = db.query(models.Student).filter(models.Student.name == student_name).first()
            if not db_student:
                raise HTTPException(status_code=400, detail=f"Student '{student_name}' not found.")

            # Find subject by title
            subject_title = row['subject_title']
            db_subject = db.query(models.Subject).filter(models.Subject.title == subject_title).first()
            if not db_subject:
                raise HTTPException(status_code=400, detail=f"Subject '{subject_title}' not found.")

            enrollment_data = schemas.EnrollmentCreate(
                student_id=db_student.id,
                subject_id=db_subject.id
            )
            db_enrollment = controller.create_enrollment(db=db, enrollment=enrollment_data)
            enrollments.append(db_enrollment)
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=400, detail=f"Error processing row {row}: {str(e)}")

    return enrollments