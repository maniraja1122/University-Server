from db import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

class Department(Base):
    __tablename__ = 'department'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)

    # Relationships
    subjects = relationship('Subject', back_populates='department')