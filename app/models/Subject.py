from db import Base
from sqlalchemy import Column, Integer, String ,ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy

class Subject(Base):
    __tablename__ = 'subject'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    credithours = Column(Integer)
    dept_id = Column(Integer, ForeignKey('department.id'))

    # Relationships
    department = relationship('Department', back_populates='subjects')
    enrollments = relationship('Enrolled', back_populates='subject')
    teaching_assignments = relationship('SubjectsTaught', back_populates='subject')

    # Association Proxies
    students = association_proxy('enrollments', 'student')
    teachers = association_proxy('teaching_assignments', 'teacher')