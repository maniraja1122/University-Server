from sqlalchemy.orm import Session
from sqlalchemy import or_
import models
import schemas

# Subjects CRUD Functions

# Get Subject based on ID
def get_subject(db: Session, subject_id: int):
    return db.query(models.Subject).filter(models.Subject.id == subject_id).first()

# Get Multiple Subjects
def get_subjects(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Subject).offset(skip).limit(limit).all()

# Create Subject Based on Schema Class
def create_subject(db: Session, subject: schemas.SubjectCreate):
    db_subject = models.Subject(
        title=subject.title,
        credithours=subject.credithours,
        dept_id=subject.dept_id,
    )
    db.add(db_subject)
    db.commit()
    db.refresh(db_subject)
    return db_subject

# Update Subject Based on Schema Class
def update_subject(db: Session, subject_id: int, subject: schemas.SubjectCreate):
    db_subject = get_subject(db, subject_id)
    if db_subject:
        db_subject.title = subject.title
        db_subject.credithours = subject.credithours
        db_subject.dept_id = subject.dept_id
        db.commit()
        db.refresh(db_subject)
    return db_subject

# Delete Subject Based on ID
def delete_subject(db: Session, subject_id: int):
    db_subject = get_subject(db, subject_id)
    if db_subject:
        db.delete(db_subject)
        db.commit()
    return db_subject