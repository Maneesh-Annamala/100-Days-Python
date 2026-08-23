
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer,String,Boolean,ForeignKey
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column,relationship
from flask_login import UserMixin






class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)


class Tasks(db.Model):
    __tablename__ = "tasks"
    id : Mapped[int] = mapped_column(Integer,primary_key=True)
    title : Mapped[str] = mapped_column(String,nullable=False)
    description : Mapped[str] = mapped_column(String,nullable=False)
    status : Mapped[bool] = mapped_column(Boolean,default=False)
    owner_id : Mapped[int] = mapped_column(Integer,ForeignKey("users.id"))
    user_relation = relationship("Users",back_populates="task_relation")

class Users(UserMixin,db.Model):
    __tablename__ = "users"
    id : Mapped[int] = mapped_column(Integer,primary_key=True)
    name : Mapped[str] = mapped_column(String,nullable=False)
    email : Mapped[str] = mapped_column(String,nullable=False,unique=True)
    password : Mapped[str] = mapped_column(String,nullable=False)
    task_relation = relationship("Tasks",back_populates="user_relation")