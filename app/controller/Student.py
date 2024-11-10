from sqlalchemy.orm import Session
from sqlalchemy import or_
import models
import schemas

# Students CRUD Functions

# Get Student based on ID
def get_student(db: Session, student_id: int):
    return db.query(models.Student).filter(models.Student.id == student_id).first()

# Get Multiple Students
def get_students(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Student).offset(skip).limit(limit).all()

# Create Student Based on Schema Class
def create_student(db: Session, student: schemas.StudentCreate):
    db_student = models.Student(name=student.name, dob=student.dob)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

# Update Student Based on Schema Class
def update_student(db: Session, student_id: int, student: schemas.StudentCreate):
    db_student = get_student(db, student_id)
    if db_student:
        db_student.name = student.name
        db_student.dob = student.dob
        db.commit()
        db.refresh(db_student)
    return db_student

# Delete Student Based on ID
def delete_student(db: Session, student_id: int):
    db_student = get_student(db, student_id)
    if db_student:
        db.delete(db_student)
        db.commit()
    return db_student