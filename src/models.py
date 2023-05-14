from sqlalchemy import Column, ForeignKey, Float, UUID, String, DateTime, func
from sqlalchemy.orm import relationship
from uuid import uuid4
from .utils.db import Base


class User(Base):
    __tablename__ = "Users"

    _id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(1000), nullable=False)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # One to Many
    payment_methods = relationship(
        "PaymentMethod", backref="user", cascade="all, delete"
    )

    # One to Many
    purchases = relationship("Purchases", backref="user", cascade="all, delete")


class PaymentMethod(Base):
    __tablename__ = "PaymentMethods"

    _id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    payment_token = Column(String(20), nullable=False)

    user_id = Column(UUID, ForeignKey("Users._id", ondelete="CASCADE"), nullable=False)

    # One to Many
    purchases = relationship(
        "Purchases", backref="payment_method", cascade="all, delete"
    )


class Purchases(Base):
    __tablename__ = "Purchases"

    _id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID, ForeignKey("Users._id", ondelete="CASCADE"), nullable=False)
    item_id = Column(UUID, ForeignKey("Items._id", ondelete="CASCADE"), nullable=False)
    payment_method_id = Column(
        UUID, ForeignKey("PaymentMethods._id", ondelete="CASCADE"), nullable=False
    )

    status = Column(String(10), default="PROCESSING_PAYMENT", nullable=False)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    delivered_at = Column(DateTime(timezone=True), nullable=True)

    items = relationship("Item", backref="purchases", cascade="all, delete")


class Item(Base):
    __tablename__ = "Items"

    _id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(100), unique=True, nullable=False)
    price = Column(Float, nullable=False)
    currency = Column(String(10), default="USD", nullable=False)
    image = Column(String(500), nullable=True)
