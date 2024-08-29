from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base_model import Base


class Comment(Base):
    __tablename__ = "comments"

    content: Mapped[str] = mapped_column(nullable=False)
    article_id: Mapped[int] = mapped_column(ForeignKey('articles.id'), index=True, nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey('users.id'), index=True, nullable=False)

    article: Mapped["Article"] = relationship("Article", back_populates="comments")
    author: Mapped["User"] = relationship("User", back_populates="comments")
