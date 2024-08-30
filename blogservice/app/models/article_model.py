from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base_model import Base, str_uniq


class Article(Base):
    __tablename__ = "articles"

    title: Mapped[str] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[str] = mapped_column(nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    author: Mapped["User"] = relationship("User", back_populates="articles")
    comments: Mapped[list["Comment"]] = relationship("Comment", back_populates="article")
    """
    complaints: Mapped[list["Complaint"]] = relationship("Complaint", back_populates="article")
    reviews: Mapped[list["Review"]] = relationship("Review", back_populates="article")
 """

    def __str__(self):
        return f"<Article(title={self.title}, content={self.content}, category={self.category}, author={self.author})>"

    def __repr__(self):
        return str(self)
