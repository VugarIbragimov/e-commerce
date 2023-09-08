import uuid
import datetime
from enum import Enum
from sqlalchemy import (Column, ForeignKey, Integer,
                        String, Float, Table, DateTime, Boolean)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY


##############################
# BLOCK WITH DATABASE MODELS #
##############################

Base = declarative_base()


class UserRole(str, Enum):
    ROLE_USER = "ROLE_USER"
    ROLE_ADMIN = "ROLE_ADMIN"
    ROLE_SUPERADMIN = "ROLE_SUPERADMIN"


class User(Base):
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(length=50), nullable=False)
    surname = Column(String(length=50), nullable=False)
    email = Column(String, nullable=False, unique=True)
    phone_number = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    hashed_password = Column(String, nullable=False)
    roles = Column(ARRAY(String), default=UserRole.ROLE_USER,
                   nullable=False)

    orders = relationship('Order', back_populates='users')
    address = relationship("Address", back_populates="user", uselist=False)
    favorites = relationship('Favorite', back_populates='user')
    carts = relationship("Cart", back_populates='user')

    @property
    def is_superadmin(self) -> bool:
        return UserRole.ROLE_SUPERADMIN in self.roles

    @property
    def is_admin(self) -> bool:
        return UserRole.ROLE_ADMIN in self.roles

    def enrich_admin_roles_by_admin_role(self):
        if not self.is_admin:
            return {*self.roles, UserRole.ROLE_ADMIN}

    def remove_admin_privileges_from_model(self):
        if self.is_admin:
            return {role for role in self.roles if role != UserRole.ROLE_ADMIN}


product_category = Table(
    'product_category',
    Base.metadata,
    Column('productId', Integer, ForeignKey('products.product_id')),
    Column('categoryId', Integer, ForeignKey('categories.category_id'))
)


class Product(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=50), nullable=False)
    price = Column(Float, nullable=False)
    sale_price = Column(Float)
    size = Column(String(length=5), nullable=False)
    small_description = Column(String, nullable=False)
    characteristic = Column(String, nullable=False)
    product_care = Column(String, nullable=False)

    categories = relationship('Category', secondary=product_category,
                              back_populates='products')
    favorites = relationship("Favorite", back_populates="product")
    cart_items = relationship("CartItem", back_populates="product")
    order_items = relationship("OrderItem", back_populates="product")
    carts = relationship("Cart", back_populates="products_association")


class Category(Base):
    __tablename__ = 'categories'

    category_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    products = relationship('Product', secondary=product_category,
                            back_populates='categories')


class Address(Base):
    __tablename__ = "address"

    address_id = Column(Integer, primary_key=True, index=True)
    country = Column(String(length=50), nullable=False)
    city = Column(String(length=50), nullable=False)
    index = Column(Integer, nullable=False)
    street = Column(String(length=50), nullable=False)
    house = Column(String, nullable=False)
    flat = Column(String, nullable=False)

    user_id = Column(UUID, ForeignKey('users.user_id'))
    user = relationship("User", back_populates="address")
    order = relationship("Order", back_populates="address", uselist=False)


class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True, index=False)

    user_id = Column(UUID, ForeignKey("users.user_id"), nullable=False)
    user = relationship("User", back_populates="favorites")
    product_id = Column(Integer, ForeignKey("products.product_id"))
    product = relationship("Product", back_populates="favorites")


class Cart(Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True, index=False)

    user_id = Column(UUID, ForeignKey("users.user_id"), nullable=False)
    user = relationship("User", back_populates="carts")
    products_association = relationship(
        "Product",
        primaryjoin="Cart.product_id == Product.product_id",
        back_populates="carts"
    )
    product_id = Column(Integer, ForeignKey('products.product_id'))
    cart_items = relationship("CartItem", back_populates="cart")


class CartItem(Base):
    __tablename__ = 'cart_items'

    id = Column(Integer, primary_key=True, index=True)
    cart_id = Column(Integer, ForeignKey('carts.id'))
    product_id = Column(Integer, ForeignKey('products.product_id'))
    quantity = Column(Integer)

    cart = relationship("Cart", back_populates="cart_items")
    product = relationship("Product", back_populates="cart_items")


class Order(Base):
    __tablename__ = "orders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # !!!!!
    # Array поле, поменять потом!!
    # !!!!
    status = Column(String, default="В обработке")
    total_price = Column(Float)
    order_date = Column(DateTime, default=datetime.datetime.utcnow)
    adress_id = Column(Integer, ForeignKey("address.address_id"),
                       nullable=False)
    address = relationship("Address", back_populates="order", uselist=False)

    user_id = Column(UUID, ForeignKey("users.user_id"), nullable=False)
    users = relationship('User', back_populates='orders')


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(UUID, ForeignKey('orders.id'))
    product_id = Column(Integer, ForeignKey('products.product_id'))
    product = relationship("Product", back_populates="order_items")
    quantity = Column(Integer)
