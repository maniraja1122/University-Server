from sqlalchemy.orm import Session
from sqlalchemy import or_
import models
import schemas

# Departments CRUD Functions

# Get Department based on ID
def get_department(db: Session, department_id: int):
    return db.query(models.Department).filter(models.Department.id == department_id).first()

# Get Multiple Departments
def get_departments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Department).offset(skip).limit(limit).all()

# Create Department Based on Schema Class
def create_department(db: Session, department: schemas.DepartmentCreate):
    db_department = models.Department(name=department.name, description=department.description)
    db.add(db_department)
    db.commit()
    db.refresh(db_department)
    return db_department

# Update Department Based on Schema Class
def update_department(db: Session, department_id: int, department: schemas.DepartmentCreate):
    db_department = get_department(db, department_id)
    if db_department:
        db_department.name = department.name
        db_department.description = department.description
        db.commit()
        db.refresh(db_department)
    return db_department

# Delete Department Based on ID
def delete_department(db: Session, department_id: int):
    db_department = get_department(db, department_id)
    if db_department:
        db.delete(db_department)
        db.commit()
    return db_department