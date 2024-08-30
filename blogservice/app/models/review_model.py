from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, relationship

"""
from app.models.base_model import Base

class Review(Base):
    __tablename__ = "reviews"

    content = Column(Text)
    rating = Column(Integer)
    article_id = Column(Integer, ForeignKey("articles.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

    article: Mapped["Article"] = relationship("Article", back_populates="reviews")
    user: Mapped["User"] = relationship("User", back_populates="reviews")
    """
