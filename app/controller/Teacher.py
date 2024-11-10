from sqlalchemy.orm import Session
from sqlalchemy import or_
import models
import schemas

# Teachers CRUD Functions

# Get Teacher based on ID
def get_teacher(db: Session, teacher_id: int):
    return db.query(models.Teacher).filter(models.Teacher.id == teacher_id).first()

# Get Multiple Teachers
def get_teachers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Teacher).offset(skip).limit(limit).all()

# Create Teacher Based on Schema Class
def create_teacher(db: Session, teacher: schemas.TeacherCreate):
    db_teacher = models.Teacher(name=teacher.name, contact=teacher.contact)
    db.add(db_teacher)
    db.commit()
    db.refresh(db_teacher)
    return db_teacher

# Update Teacher Based on Schema Class
def update_teacher(db: Session, teacher_id: int, teacher: schemas.TeacherCreate):
    db_teacher = get_teacher(db, teacher_id)
    if db_teacher:
        db_teacher.name = teacher.name
        db_teacher.contact = teacher.contact
        db.commit()
        db.refresh(db_teacher)
    return db_teacher

# Delete Teacher Based on ID
def delete_teacher(db: Session, teacher_id: int):
    db_teacher = get_teacher(db, teacher_id)
    if db_teacher:
        db.delete(db_teacher)
        db.commit()
    return db_teacher