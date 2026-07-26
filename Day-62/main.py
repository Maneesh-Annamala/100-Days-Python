from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Float

"""
A Flask Book Collection application.

Users can add books, update their ratings,
delete books, and view the complete collection.
Book data is stored using SQLite and SQLAlchemy ORM.
"""

app = Flask(__name__)

# ---------------------------- DATABASE CONFIGURATION ---------------------------- #

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///books-collection.db"

db = SQLAlchemy(app)


# ---------------------------- BOOK MODEL ---------------------------- #

class Books(db.Model):
    """Represents a book stored in the database."""

    # Primary key
    id: Mapped[int] = mapped_column(Integer,primary_key=True)

    # Book title
    title: Mapped[str] = mapped_column(String(100),nullable=False,unique=True)

    # Author name
    author: Mapped[str] = mapped_column(String(150),nullable=False)

    # User rating
    rating: Mapped[float] = mapped_column(Float,nullable=False)


# ---------------------------- HOME PAGE ---------------------------- #

@app.route('/')
def home():
    """Displays all books stored in the database."""

    books = db.session.execute(db.select(Books).order_by(Books.id)).scalars().all()
    return render_template("index.html",books=books)


# ---------------------------- ADD BOOK ---------------------------- #

@app.route("/add", methods=['GET', 'POST'])
def add():
    """
    Displays the Add Book page.

    When the form is submitted,
    a new book is saved into the database.
    """

    if request.method == 'POST':

        # Read form data
        book_title = request.form['title']
        author_name = request.form['author']
        book_rating = request.form['rating']

        # Create a new book object
        details = Books(
            title=book_title,
            author=author_name,
            rating=book_rating
        )

        # Save book into database
        db.session.add(details)
        db.session.commit()

        # Refresh page after successful submission
        return redirect(url_for('add'))

    return render_template("add.html")


# ---------------------------- DELETE BOOK ---------------------------- #

@app.route("/delete")
def delete():
    """Deletes the selected book from the database."""

    # Get selected book id
    id = request.args.get("id")

    # Find book
    delete_book = db.session.execute(db.select(Books).where(Books.id == id)).scalar()

    # Delete book
    db.session.delete(delete_book)
    db.session.commit()

    return redirect(url_for('home'))


# ---------------------------- UPDATE BOOK ---------------------------- #

@app.route("/update", methods=['GET', 'POST'])
def update():
    """
    Displays the Update page.

    Allows the user to update
    the selected book's rating.
    """

    # Get selected book id
    id = request.args.get("id")

    # Retrieve book from database
    book = db.session.execute(
        db.select(Books).where(
            Books.id == id
        )
    ).scalar()

    if request.method == 'POST':

        # Update rating
        book.rating = request.form['rating']

        db.session.commit()

        return redirect(url_for('home'))

    return render_template("update.html",book=book)


# ---------------------------- START APPLICATION ---------------------------- #

if __name__ == "__main__":

    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()

    app.run(debug=True)