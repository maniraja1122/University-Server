from db import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

class Department(Base):
    __tablename__ = 'department'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    description = Column(String(1000))

    # Relationships
    subjects = relationship('Subject', back_populates='department')