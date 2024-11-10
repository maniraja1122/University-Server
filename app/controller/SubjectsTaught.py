from sqlalchemy.orm import Session
from sqlalchemy import or_
import models
import schemas

# Subjects Taught CRUD Functions

# Get Subject Taught based on ID
def get_subject_taught(db: Session, subject_taught_id: int):
    return db.query(models.SubjectsTaught).filter(models.SubjectsTaught.id == subject_taught_id).first()

# Get Multiple Subjects Taught
def get_subjects_taught(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.SubjectsTaught).offset(skip).limit(limit).all()

# Create Subject Taught Based on Schema Class
def create_subject_taught(db: Session, subject_taught: schemas.SubjectTaughtCreate):
    db_subject_taught = models.SubjectsTaught(
        teacher_id=subject_taught.teacher_id, subject_id=subject_taught.subject_id
    )
    db.add(db_subject_taught)
    db.commit()
    db.refresh(db_subject_taught)
    return db_subject_taught

# Delete Subject Taught Based on ID
def delete_subject_taught(db: Session, subject_taught_id: int):
    db_subject_taught = get_subject_taught(db, subject_taught_id)
    if db_subject_taught:
        db.delete(db_subject_taught)
        db.commit()
    return db_subject_taught