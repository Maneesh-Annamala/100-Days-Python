from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,URLField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
from datetime import date
from dotenv import load_dotenv
import os

"""
A Flask Blog application built using SQLAlchemy, WTForms,
Bootstrap, and CKEditor.

This application allows users to create, edit, delete,
and view blog posts stored in a SQLite database.
"""
load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
Bootstrap5(app)

ckeditor = CKEditor()
ckeditor.init_app(app)

# ---------------------------- DATABASE CONFIGURATION ---------------------------- #
class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# ---------------------------- DATABASE MODEL ---------------------------- #
class BlogPost(db.Model):
    """Represents a blog post stored in the database."""
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)

# ---------------------------- BLOG FORM ---------------------------- #
class Form(FlaskForm):
    """Form used to create and edit blog posts."""
    post_title = StringField("post title",validators=[DataRequired()])
    post_subtitle = StringField("post subtitle",validators=[DataRequired()])
    post_author = StringField("Author name",validators=[DataRequired()])
    post_img_url = URLField("image url",validators=[DataRequired()])
    post_body = CKEditorField("Body",validators=[DataRequired()])
    submit = SubmitField("Submit")

with app.app_context():
    # Create database tables
    db.create_all()

# ---------------------------- HOME PAGE ---------------------------- #
@app.route('/')
def get_all_posts():
    """Displays all blog posts."""
    posts = []
    data = db.session.execute(db.select(BlogPost)).scalars().all()
    for i in data:
        posts.append(i)
    return render_template("index.html", all_posts=posts)

# ---------------------------- VIEW BLOG POST ---------------------------- #
@app.route('/singlepost/<post_id>')
def show_post(post_id):
    """Displays a single blog post."""
    data = db.session.execute(db.select(BlogPost).where(BlogPost.id == post_id)).scalar()
    requested_post = data
    return render_template("post.html", post=requested_post)


# ---------------------------- CREATE BLOG POST ---------------------------- #
@app.route("/newpost",methods=['GET','POST'])
def add_new_post():
    """Creates a new blog post."""
    form = Form()
    if form.validate_on_submit():
        data = BlogPost(
            title = form.post_title.data,
            subtitle = form.post_subtitle.data,
            date = date.today(),
            body = form.post_body.data,
            author = form.post_author.data,
            img_url = form.post_img_url.data
        )
        db.session.add(data)
        db.session.commit()
        return redirect(url_for('get_all_posts'))
    return render_template("make-post.html",form=form,heading = "New Post")

# ---------------------------- EDIT BLOG POST ---------------------------- #
@app.route("/edit/<post_id>",methods=['GET','POST'])
def edit_post(post_id):
    """Edits an existing blog post."""
    update = db.session.execute(db.select(BlogPost).where(BlogPost.id == post_id)).scalar()
    form = Form(post_title=update.title,
                post_subtitle=update.subtitle,
                post_author=update.author,
                post_img_url=update.img_url,
                post_body=update.body)
    if form.validate_on_submit():
        update.title = form.post_title.data
        update.subtitle = form.post_subtitle.data
        update.author = form.post_author.data
        update.body = form.post_body.data
        update.img_url = form.post_img_url.data
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html",form=form,heading="Edit Post")

# ---------------------------- DELETE BLOG POST ---------------------------- #
@app.route("/delete-post/<post_id>")
def delete_post(post_id):
    """Deletes a blog post."""
    post = db.session.execute(db.select(BlogPost).where(BlogPost.id == post_id)).scalar()
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for("get_all_posts"))

# ---------------------------- ABOUT PAGE ---------------------------- #
@app.route("/about")
def about():
    """Displays the About page."""
    return render_template("about.html")

# ---------------------------- CONTACT PAGE ---------------------------- #
@app.route("/contact")
def contact():
    """Displays the Contact page."""
    return render_template("contact.html")

# ---------------------------- START APPLICATION ---------------------------- #
if __name__ == "__main__":
    app.run(debug=True, port=5003)
