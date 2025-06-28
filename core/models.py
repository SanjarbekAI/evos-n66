from datetime import datetime

from sqlalchemy import String, BigInteger, DateTime, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=True)
    full_name: Mapped[str] = mapped_column(String)
    chat_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    phone_number: Mapped[str] = mapped_column(String, unique=True)
    language: Mapped[str] = mapped_column(String, default="en")
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class Category(Base):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[dict] = mapped_column(JSONB, unique=True)

    # Optional: if you want to access all products in this category
    products: Mapped[list["Product"]] = relationship(
        "Product", back_populates="category"
    )


class Product(Base):
    __tablename__ = "product"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[dict] = mapped_column(JSONB, unique=True)
    price: Mapped[int] = mapped_column(BigInteger)
    about: Mapped[dict] = mapped_column(JSONB)
    image: Mapped[str] = mapped_column(String)

    category_id: Mapped[int] = mapped_column(
        ForeignKey("category.id")
    )
    category: Mapped["Category"] = relationship(
        "Category", back_populates="products"
    )
