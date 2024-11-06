from db import Base
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

class Enrolled(Base):
    __tablename__ = 'enrolled'

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('student.id'))
    subject_id = Column(Integer, ForeignKey('subject.id'))

    # Relationships
    student = relationship('Student', back_populates='enrollments')
    subject = relationship('Subject', back_populates='enrollments')