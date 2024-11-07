from sqlalchemy.orm import Session
from sqlalchemy import or_
import models
import schemas

# Enrollments

def get_enrollment(db: Session, enrollment_id: int):
    return db.query(models.Enrolled).filter(models.Enrolled.id == enrollment_id).first()

def get_enrollments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Enrolled).offset(skip).limit(limit).all()

def create_enrollment(db: Session, enrollment: schemas.EnrollmentCreate):
    db_enrollment = models.Enrolled(
        student_id=enrollment.student_id, subject_id=enrollment.subject_id
    )
    db.add(db_enrollment)
    db.commit()
    db.refresh(db_enrollment)
    return db_enrollment

def delete_enrollment(db: Session, enrollment_id: int):
    db_enrollment = get_enrollment(db, enrollment_id)
    if db_enrollment:
        db.delete(db_enrollment)
        db.commit()
    return db_enrollment