"""
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship, Mapped
from datetime import datetime

from app.models.base_model import Base


class Complaint(Base):
    __tablename__ = "complaints"

    reason = Column(String)
    article_id = Column(Integer, ForeignKey("articles.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

    article: Mapped["Article"] = relationship("Article", back_populates="complaints")
    user: Mapped["User"] = relationship("User", back_populates="complaints")
 """
