from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
    Boolean,
    ForeignKey,
    UniqueConstraint,
    Table,
)
from database import Base
from sqlalchemy.orm import relationship

user_wishlist = Table(
    "user_wishlist",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("product_id", Integer, ForeignKey("products.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"
    __table_args__ = (UniqueConstraint("email", name="uq_user_email"),)

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    age = Column(Integer)
    role = Column(String, nullable=False)
    hobbies = Column(String)
    city = Column(String)
    country = Column(String)
    orders = relationship("Order", back_populates="user")
    profile = relationship("UserProfile", back_populates="user", uselist=False)
    wishlist = relationship(
        "Product", secondary=user_wishlist, back_populates="wishlisted_by"
    )


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    in_stock = Column(Boolean, default=True)
    orders = relationship("Order", back_populates="product")
    wishlisted_by = relationship(
        "User", secondary=user_wishlist, back_populates="wishlist"
    )


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    status = Column(String, nullable=False, default="pending")
    user = relationship("User", back_populates="orders")
    product = relationship("Product", back_populates="orders")


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    hobbies = Column(String)
    city = Column(String)
    country = Column(String)
    user = relationship("User", back_populates="profile")


# for checking related info
print(User.__table__.columns)
print(Product.__table__.columns)
