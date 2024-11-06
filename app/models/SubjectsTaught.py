from db import Base
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

class SubjectsTaught(Base):
    __tablename__ = 'subjects_taught'

    id = Column(Integer, primary_key=True)
    teacher_id = Column(Integer, ForeignKey('teacher.id'))
    subject_id = Column(Integer, ForeignKey('subject.id'))

    # Relationships
    teacher = relationship('Teacher', back_populates='teaching_assignments')
    subject = relationship('Subject', back_populates='teaching_assignments')