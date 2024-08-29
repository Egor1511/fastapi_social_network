from sqlalchemy import String, Boolean, Integer, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base_model import Base, str_uniq


class User(Base):
    __tablename__ = "users"

    username: Mapped[str_uniq]
    email: Mapped[str_uniq]
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    is_admin: Mapped[bool] = mapped_column(default=False, server_default=text('false'), nullable=False)

    articles: Mapped[list["Article"]] = relationship("Article", back_populates="author")
    comments: Mapped[list["Comment"]] = relationship("Comment", back_populates="author")

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"
