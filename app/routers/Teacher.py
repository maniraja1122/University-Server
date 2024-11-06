from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List
from app import controller, schemas, models
from db import get_db

teacher_router = APIRouter(
    prefix="/teachers",
    tags=["teachers"],
    responses={404: {"description": "Not found"}},
)

@teacher_router.post("/", response_model=schemas.Teacher)
def create_teacher(teacher: schemas.TeacherCreate, db: Session = Depends(get_db)):
    return controller.create_teacher(db=db, teacher=teacher)

@teacher_router.get("/", response_model=List[schemas.Teacher])
def read_teachers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    teachers = controller.get_teachers(db, skip=skip, limit=limit)
    return teachers

@teacher_router.get("/{teacher_id}", response_model=schemas.Teacher)
def read_teacher(teacher_id: int, db: Session = Depends(get_db)):
    db_teacher = db.query(models.Teacher).filter(models.Teacher.id == teacher_id).options(
        joinedload(models.Teacher.subjects)
    ).first()
    if db_teacher is None:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return db_teacher

@teacher_router.put("/{teacher_id}", response_model=schemas.Teacher)
def update_teacher(teacher_id: int, teacher: schemas.TeacherCreate, db: Session = Depends(get_db)):
    db_teacher = controller.update_teacher(db=db, teacher_id=teacher_id, teacher=teacher)
    if db_teacher is None:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return db_teacher

@teacher_router.delete("/{teacher_id}")
def delete_teacher(teacher_id: int, db: Session = Depends(get_db)):
    db_teacher = controller.delete_teacher(db=db, teacher_id=teacher_id)
    if db_teacher is None:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return {"detail": "Teacher deleted"}