from db import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy

class Teacher(Base):
    __tablename__ = 'teacher'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    contact = Column(String(255))

    # Relationships
    teaching_assignments = relationship('SubjectsTaught', back_populates='teacher')

    # Association Proxy
    subjects = association_proxy('teaching_assignments', 'subject')