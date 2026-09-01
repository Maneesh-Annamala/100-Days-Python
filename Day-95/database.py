from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.orm import relationship,Mapped,mapped_column,DeclarativeBase
from werkzeug.security import generate_password_hash,check_password_hash
from sqlalchemy import Integer,String,Text,ForeignKey
from main import app
from typing import List

class Base(DeclarativeBase):
    pass

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///./e-commerce.db"
db = SQLAlchemy(model_class=Base)
db.init_app(app)

class Users(UserMixin,db.Model):
    __tablename__ = "users"
    id : Mapped[int] = mapped_column(Integer,primary_key=True)
    username : Mapped[str] = mapped_column(String(250))
    email : Mapped[str] = mapped_column(String(250),unique=True)
    password : Mapped[str] = mapped_column(String(300))
    reviews : Mapped[List["Reviews"]] = relationship(back_populates="user")
    cart_rel = Mapped[List["Cart"]] = relationship(back_populates="cart_rel")
    wish_user_rel : Mapped[List["Wishlist"]] = relationship(back_populates="wish_user_rel")

class Products(db.Model):
    __tablename__  = "products"
    id : Mapped[int] = mapped_column(Integer,primary_key=True)
    img_link : Mapped[str] = mapped_column(String(300),nullable=False)
    prod_link : Mapped[str] = mapped_column(String(500),nullable=False)
    description : Mapped[str] = mapped_column(Text,nullable=False)
    category : Mapped[str] = mapped_column(String(250),default="unknown")
    price : Mapped[int] = mapped_column(Integer,nullable=False)
    discount : Mapped[int] = mapped_column(Integer,default=0)
    brand : Mapped[str] = mapped_column(String(250),default="unknown brand")
    reviews : Mapped[List["Reviews"]] = relationship(back_populates="product")
    prod_rel : Mapped[List["Cart"]] = relationship(back_populates="prod_rel")
    wish_prod_rel : Mapped[List["Wishlist"]] = relationship(back_populates="wish_prod_rel")

class Cart(db.Model):
    id : Mapped[int] = mapped_column(Integer,primary_key=True)
    product_id : Mapped[int] = mapped_column(ForeignKey("products.id"),nullable=False)
    user_id : Mapped[int] = mapped_column(ForeignKey("users.id"),nullable=False)
    quantity : Mapped[int] = mapped_column(Integer,default=1)
    cart_rel : Mapped["Users"] = relationship(Users,back_populates="cart_rel")
    prod_rel : Mapped["Products"] = relationship(Products,back_populates="prod_rel")

class Wishlist(db.Model):
    __tablename__ = "wishlist"
    id : Mapped[int] = mapped_column(Integer,primary_key=True)
    product_id : Mapped[int] = mapped_column(ForeignKey("products.id"),nullable=False)
    user_id : Mapped[int] = mapped_column(ForeignKey("users.id"),nullable=False)
    wish_prod_rel : Mapped["Products"] = relationship(Products,back_populates="wish_prod_rel")
    wish_user_rel : Mapped["Users"] = relationship(Users,back_populates="wish_user_rel")
    
class Reviews(db.Model):
    __tablename__  = "reviews"
    id : Mapped[int] = mapped_column(Integer,primary_key=True)
    product_id : Mapped[int] = mapped_column(ForeignKey("products.id"),nullable=False)
    user_id : Mapped[int] = mapped_column(ForeignKey("users.id"),nullable=False)
    review : Mapped[str] = mapped_column(Text)
    user : Mapped["Users"] = relationship(Users,back_populates="reviews")
    product : Mapped["Products"] = relationship(Products,back_populates="reviews")
