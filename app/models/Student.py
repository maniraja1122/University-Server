from db import Base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy

class Student(Base):
    __tablename__ = 'student'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    dob = Column(Date)
    # Relationships
    enrollments = relationship('Enrolled', back_populates='student')
    # Association Proxy
    subjects = association_proxy('enrollments', 'subject')