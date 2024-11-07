from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
import csv
import io
from sqlalchemy.orm import Session
from typing import List
import controller
import schemas
from db import get_db

department_router = APIRouter(
    prefix="/departments",
    tags=["departments"],
    responses={404: {"description": "Not found"}},
)

# Payload Functions
@department_router.post("/", response_model=schemas.Department)
def create_department(department: schemas.DepartmentCreate, db: Session = Depends(get_db)):
    return controller.create_department(db=db, department=department)

@department_router.get("/", response_model=List[schemas.Department])
def read_departments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    departments = controller.get_departments(db, skip=skip, limit=limit)
    return departments

@department_router.get("/{department_id}", response_model=schemas.Department)
def read_department(department_id: int, db: Session = Depends(get_db)):
    db_department = controller.get_department(db, department_id=department_id)
    if db_department is None:
        raise HTTPException(status_code=404, detail="Department not found")
    return db_department

@department_router.put("/{department_id}", response_model=schemas.Department)
def update_department(department_id: int, department: schemas.DepartmentCreate, db: Session = Depends(get_db)):
    db_department = controller.update_department(db=db, department_id=department_id, department=department)
    if db_department is None:
        raise HTTPException(status_code=404, detail="Department not found")
    return db_department

@department_router.delete("/{department_id}")
def delete_department(department_id: int, db: Session = Depends(get_db)):
    db_department = controller.delete_department(db=db, department_id=department_id)
    if db_department is None:
        raise HTTPException(status_code=404, detail="Department not found")
    return {"detail": "Department deleted"}

# CSV Function
@department_router.post("/upload_csv/", response_model=List[schemas.Department])
async def upload_departments_csv(
    file: UploadFile = File(...), db: Session = Depends(get_db)
):
    if file.content_type != 'text/csv':
        raise HTTPException(status_code=400, detail="Invalid file type. Expected CSV.")

    content = await file.read()
    reader = csv.DictReader(io.StringIO(content.decode('utf-8')))

    departments = []
    for row in reader:
        try:
            department_data = schemas.DepartmentCreate(
                name=row['name'],
                description=row.get('description')
            )
            db_department = controller.create_department(db=db, department=department_data)
            departments.append(db_department)
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=400, detail=f"Error processing row {row}: {str(e)}")

    return departments