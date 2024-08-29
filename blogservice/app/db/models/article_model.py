from sqlalchemy import Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base_model import Base, str_uniq


class Article(Base):
    __tablename__ = "articles"

    title: Mapped[str] = mapped_column(index=True, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[str_uniq]
    author_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    author: Mapped["User"] = relationship("User", back_populates="articles")
    comments: Mapped[list["Comment"]] = relationship("Comment", back_populates="article")

    def __str__(self):
        return f"<Article(title={self.title}, content={self.content}, category={self.category}, author={self.author})>"

    def __repr__(self):
        return str(self)
