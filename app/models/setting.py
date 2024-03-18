import uuid
from typing import Any
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.core.config import settings


class Setting(Base):
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    path = Column(String, index=True, nullable=False)
    key = Column(String)
    value = Column(String)
    type = Column(String)
    description = Column(String)
