from sqlalchemy.orm import Session
from sqlalchemy import or_
import models
import schemas

# Enrollments CRUD Functions

# Get Enrollment based on ID
def get_enrollment(db: Session, enrollment_id: int):
    return db.query(models.Enrolled).filter(models.Enrolled.id == enrollment_id).first()

# Get Multiple Enrollments
def get_enrollments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Enrolled).offset(skip).limit(limit).all()

# Create Enrollment Based on Schema Class
def create_enrollment(db: Session, enrollment: schemas.EnrollmentCreate):
    db_enrollment = models.Enrolled(
        student_id=enrollment.student_id, subject_id=enrollment.subject_id
    )
    db.add(db_enrollment)
    db.commit()
    db.refresh(db_enrollment)
    return db_enrollment

# Delete Enrollment Based on ID
def delete_enrollment(db: Session, enrollment_id: int):
    db_enrollment = get_enrollment(db, enrollment_id)
    if db_enrollment:
        db.delete(db_enrollment)
        db.commit()
    return db_enrollment