import uuid
from typing import Any
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.core.config import settings


class Location(Base):
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    key = Column(Integer, unique=True, index=True, nullable=False)
    kind = Column(Integer, nullable=False)
    country = Column(String)
    label = Column(String, nullable=False)
    additional = Column(String)
