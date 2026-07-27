from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    IntegerField,
    FloatField,
    URLField
)
from wtforms.validators import DataRequired, Length
from dotenv import load_dotenv
import os

"""
A Flask Movie Collection application.

Users can add movies, update ratings and reviews,
delete movies, and view their personal movie collection.
Movie information is stored using SQLite and SQLAlchemy.
"""
load_dotenv()
app = Flask(__name__)

# Secret key used for CSRF protection
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

# Initialize Bootstrap
Bootstrap5(app)

# Configure SQLite database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movie-collections.db"

# Initialize SQLAlchemy
db = SQLAlchemy(app)


# ---------------------------- DATABASE MODEL ---------------------------- #

class Movies(db.Model):
    """Represents a movie stored in the database."""

    # Primary key
    id: Mapped[int] = mapped_column(Integer,primary_key=True)

    # Movie title
    title: Mapped[str] = mapped_column(String(150),nullable=False,unique=True)

    # Release year
    year: Mapped[int] = mapped_column(Integer,nullable=False)

    # Movie description
    description: Mapped[str] = mapped_column(String(500),nullable=False)

    # User rating
    rating: Mapped[float] = mapped_column(Float,nullable=False)

    # Personal ranking
    ranking: Mapped[int] = mapped_column(Integer,nullable=False)

    # User review
    review: Mapped[str] = mapped_column(String(200))

    # Movie poster URL
    img_url: Mapped[str] = mapped_column(String(500),nullable=False)


# ---------------------------- ADD MOVIE FORM ---------------------------- #

class Form(FlaskForm):
    """Form used to add a new movie."""

    movie_title = StringField("Movie name",validators=[DataRequired()])

    movie_year = IntegerField("Released Year",validators=[DataRequired()])

    movie_desc = StringField("Description of The Movie",validators=[DataRequired(),Length(min=50)])

    movie_rating = FloatField("Rating",validators=[DataRequired()])

    movie_ranking = IntegerField("Your Rank",validators=[DataRequired()])

    movie_review = StringField("Review",validators=[DataRequired()])

    movie_img = URLField("Poster URL",validators=[DataRequired()])

    submit = SubmitField("Submit")


# ---------------------------- UPDATE FORM ---------------------------- #

class QuickForm(FlaskForm):
    """Form used to update a movie's rating and review."""

    update_rating = FloatField("Rating",validators=[DataRequired()])

    update_review = StringField("Review",validators=[DataRequired()])

    submit = SubmitField("Update")


# ---------------------------- HOME PAGE ---------------------------- #

@app.route("/")
def home():
    """Displays all movies ordered by ranking."""

    movies = db.session.execute(db.select(Movies).order_by(Movies.ranking)).scalars().all()

    return render_template("index.html",movies=movies)


# ---------------------------- ADD MOVIE ---------------------------- #

@app.route("/add", methods=["GET", "POST"])
def add_movie():
    """
    Displays the Add Movie page.

    When the form is submitted successfully,
    a new movie is stored in the database.
    """

    form_data = Form()

    if form_data.validate_on_submit():

        data = Movies(
            title=form_data.movie_title.data,
            year=form_data.movie_year.data,
            description=form_data.movie_desc.data,
            rating=form_data.movie_rating.data,
            ranking=form_data.movie_ranking.data,
            review=form_data.movie_review.data,
            img_url=form_data.movie_img.data,
        )

        db.session.add(data)
        db.session.commit()

        return redirect(url_for("home"))

    return render_template(
        "add.html",
        form=form_data
    )


# ---------------------------- UPDATE MOVIE ---------------------------- #

@app.route("/update", methods=["GET", "POST"])
def update():
    """
    Updates the selected movie's
    rating and review.
    """

    movie_id = request.args.get("id")

    movie = db.session.execute(
        db.select(Movies).where(Movies.id == movie_id)
    ).scalar()

    form = QuickForm()

    if form.validate_on_submit():

        movie.rating = form.update_rating.data
        movie.review = form.update_review.data

        db.session.commit()

        return redirect(url_for("home"))

    return render_template(
        "edit.html",
        form=form,
        movie=movie
    )


# ---------------------------- DELETE MOVIE ---------------------------- #

@app.route("/delete")
def delete():
    """Deletes the selected movie."""

    movie_id = request.args.get("id")

    movie = db.session.execute(
        db.select(Movies).where(Movies.id == movie_id)
    ).scalar()

    db.session.delete(movie)
    db.session.commit()

    return redirect(url_for("home"))


# ---------------------------- START APPLICATION ---------------------------- #

if __name__ == "__main__":

    # Create database tables if they don't already exist
    with app.app_context():
        db.create_all()

    app.run(debug=True)