from datetime import date
from flask import Flask, abort, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user,login_required
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text,ForeignKey
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from typing import List
from forms import CreatePostForm,Register,Login,CommentForm
from dotenv import load_dotenv
import os

load_dotenv()


app = Flask(__name__)
app.config['SECRET_KEY'] = "8BYkEfBA6O6donzWlSihBXox7C0sKR6b"
ckeditor = CKEditor(app)
Bootstrap5(app)

login_manager = LoginManager(app)



class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blogs.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    author_id : Mapped[int] = mapped_column(ForeignKey("users_data.id"))
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)
    author: Mapped['Users'] = relationship(back_populates="posts")
    comments : Mapped[List["Comment"]] = relationship(back_populates="blog_comments",cascade="all,delete-orphan")
 
class Users(UserMixin,db.Model):
    __tablename__ = "users_data"
    id:Mapped[int] = mapped_column(Integer,primary_key=True)
    name: Mapped[str] = mapped_column(String,nullable=False)
    email : Mapped[str] = mapped_column(String,unique=True,nullable=False)
    password : Mapped[str] = mapped_column(String,nullable=False)
    posts : Mapped[List["BlogPost"]] = relationship(back_populates="author")
    user_comment : Mapped[List["Comment"]] = relationship(back_populates="comment_author")

class Comment(db.Model):
    __tablename__ = "comments"
    id : Mapped[int] = mapped_column(Integer,primary_key=True)
    author_id : Mapped[int] = mapped_column(Integer,ForeignKey("users_data.id"))
    post_id : Mapped[int] = mapped_column(Integer,ForeignKey("blog_posts.id"))
    comment : Mapped[str] = mapped_column(Text)
    comment_author:Mapped["Users"]  = relationship(Users,back_populates="user_comment")
    blog_comments : Mapped["BlogPost"] = relationship(BlogPost,back_populates="comments")

with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(Users,int(user_id))

def admin_only(func):
    @wraps(func)
    def decorater(*args,**kwargs):
        if not current_user.is_authenticated:
            return login_manager.unauthorized()
        if current_user.id != 1:
            return abort(403)
        return func(*args,**kwargs)
    return decorater


@app.route('/register',methods=['GET','POST'])
def register():
    register_form = Register()
    if register_form.validate_on_submit():
        password = generate_password_hash(register_form.password.data,method="pbkdf2:sha256",salt_length=8)
        email = register_form.email.data
        check = db.session.execute(db.select(Users).where(Users.email == email)).scalar()
        if check:
            flash("Already have an account with this mail")
            return redirect(url_for('login'))
        else:
            register_user = Users(name=register_form.name.data,
                                email=register_form.email.data,
                                password=password)
            db.session.add(register_user)
            db.session.commit()
            login_user(register_user)
            return redirect(url_for('get_all_posts'))
    return render_template("register.html",form=register_form)



@app.route('/login',methods=['GET','POST'])
def login():
    login_form = Login()
    if login_form.validate_on_submit():
        email = login_form.email.data
        password = login_form.password.data
        email_check = db.session.execute(db.select(Users).where(Users.email == email)).scalar()
        if email_check:
            if check_password_hash(email_check.password,password):
                login_user(email_check)
                return redirect(url_for('get_all_posts'))
            else:
                flash("Invalid Password")
                return redirect(url_for('login'))
        else:
            flash("Invalid Email")
            return redirect(url_for('login'))

    return render_template("login.html",form=login_form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('get_all_posts'))


@app.route('/')
def get_all_posts():
    result = db.session.execute(db.select(BlogPost))
    posts = result.scalars().all()
    return render_template("index.html", all_posts=posts,authenticate=current_user.is_authenticated,id=current_user.get_id())


@app.route("/post/<int:post_id>",methods=['GET','POST'])
def show_post(post_id):
    requested_post = db.get_or_404(BlogPost, post_id)
    comment = CommentForm()
    if comment.validate_on_submit(): 
        if current_user.is_authenticated:
            new_comment = Comment(
                comment_author = current_user,
                blog_comments = requested_post,
                comment = comment.comment.data
            )
            db.session.add(new_comment)
            db.session.commit()
            return redirect(url_for('show_post',post_id=post_id))
        else:
            flash("You need to login or register first")
            return redirect(url_for('login'))
    return render_template("post.html", post=requested_post,current_user = current_user,comment=comment)



@app.route("/new-post", methods=["GET", "POST"])
@admin_only
def add_new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=current_user,
            date=date.today().strftime("%B %d, %Y")
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form)



@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
@login_required
@admin_only
def edit_post(post_id):
    post = db.session.get(BlogPost, post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        body=post.body
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.author = current_user
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))
    return render_template("make-post.html", form=edit_form, is_edit=True,id=current_user.get_id())



@app.route("/delete/<int:post_id>")
@login_required
@admin_only
def delete_post(post_id):
    post_to_delete = db.get_or_404(BlogPost, post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts'))


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True, port=5002)
