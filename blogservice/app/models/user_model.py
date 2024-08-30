from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base_model import Base, str_uniq


class User(Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str_uniq]
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    is_admin: Mapped[bool] = mapped_column(default=False, server_default=text("false"), nullable=False)

    articles: Mapped[list["Article"]] = relationship("Article", back_populates="author")
    comments: Mapped[list["Comment"]] = relationship("Comment", back_populates="author")
    """
    complaints: Mapped[list["Complaint"]] = relationship("Complaint", back_populates="user")
    reviews: Mapped[list["Review"]] = relationship("Review", back_populates="user")
 """

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"
