from datetime import datetime

from sqlalchemy import String, BigInteger, DateTime
from sqlalchemy.orm import declarative_base, Mapped, mapped_column

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=True)
    full_name: Mapped[str] = mapped_column(String)
    chat_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    phone_number: Mapped[str] = mapped_column(String, unique=True)
    language: Mapped[str] = mapped_column(String, default="en")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
