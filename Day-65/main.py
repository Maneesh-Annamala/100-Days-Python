from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
import random

"""
A Flask REST API for managing café information.

The application provides endpoints to retrieve,
add, update, and delete café records stored
in a SQLite database using SQLAlchemy.
"""

app = Flask(__name__)

# API key required for protected endpoints
secret_key = "abcd1234"


# ---------------------------- DATABASE CONFIGURATION ---------------------------- #

class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""
    pass


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cafes.db"

db = SQLAlchemy(model_class=Base)
db.init_app(app)


# ---------------------------- DATABASE MODEL ---------------------------- #

class Cafe(db.Model):
    """Represents a café stored in the database."""

    id: Mapped[int] = mapped_column(Integer,primary_key=True)

    name: Mapped[str] = mapped_column(String(250),unique=True,nullable=False)

    map_url: Mapped[str] = mapped_column(String(500),nullable=False)

    img_url: Mapped[str] = mapped_column(String(500),nullable=False)

    location: Mapped[str] = mapped_column(String(250),nullable=False)

    seats: Mapped[str] = mapped_column(String(250),nullable=False)

    has_toilet: Mapped[bool] = mapped_column(Boolean,nullable=False)

    has_wifi: Mapped[bool] = mapped_column(Boolean,nullable=False)

    has_sockets: Mapped[bool] = mapped_column(Boolean,nullable=False)

    can_take_calls: Mapped[bool] = mapped_column(Boolean,nullable=False)

    coffee_price: Mapped[str] = mapped_column(String(250),nullable=True)

    def to_dict(self):
        """
        Converts the café object into
        a dictionary representation.
        """

        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }


# Create database tables
with app.app_context():
    db.create_all()


# ---------------------------- HOME PAGE ---------------------------- #

@app.route("/")
def home():
    """Displays the API home page."""

    return render_template("index.html")


# ---------------------------- RANDOM CAFE ---------------------------- #

@app.route("/random")
def get_random():
    """Returns a random café from the database."""

    data = db.session.execute(
        db.select(Cafe)
    ).scalars().all()

    random_choice = random.choice(data)

    return jsonify(cafe=random_choice.to_dict())


# ---------------------------- ALL CAFES ---------------------------- #

@app.route("/all")
def all_data():
    """Returns all cafés available in the database."""

    data = db.session.execute(
        db.select(Cafe)
    ).scalars().all()

    cafes = {
        cafe.name: cafe.to_dict()
        for cafe in data
    }

    return jsonify(cafe=cafes)


# ---------------------------- SEARCH BY LOCATION ---------------------------- #

@app.route("/search")
def search():
    """Returns cafés that match the requested location."""

    loc = request.args.get("loc")

    data = db.session.execute(
        db.select(Cafe).where(Cafe.location == loc)
    ).scalars().all()

    cafes = {
        cafe.name: cafe.to_dict()
        for cafe in data
    }

    return jsonify(cafe=cafes)


# ---------------------------- ADD NEW CAFE ---------------------------- #

@app.route("/add", methods=["POST"])
def add():
    """Adds a new café to the database."""

    data = Cafe(
        name=request.form.get("name"),
        map_url=request.form.get("map_url"),
        img_url=request.form.get("img_url"),
        location=request.form.get("location"),
        seats=request.form.get("seats"),
        has_toilet=request.form.get("has_toilet") == "True",
        has_wifi=request.form.get("has_wifi") == "True",
        has_sockets=request.form.get("has_sockets") == "True",
        can_take_calls=request.form.get("can_take_calls") == "True",
        coffee_price=request.form.get("coffee_price")
    )

    db.session.add(data)
    db.session.commit()

    return jsonify(
        response={
            "success": "Response submitted successfully."
        }
    )


# ---------------------------- UPDATE COFFEE PRICE ---------------------------- #

@app.route("/change-price/<caf_id>", methods=["PATCH"])
def change_price(caf_id):
    """
    Updates the coffee price of
    the selected café.
    """

    new_price = request.args.get("new_price")

    try:

        data = db.session.execute(
            db.select(Cafe).where(Cafe.id == caf_id)
        ).scalar()

        data.coffee_price = new_price

        db.session.commit()

        return jsonify(
            response={
                "success": "Response updated successfully."
            }
        )

    except AttributeError:

        return jsonify(
            response={
                "Failed": "No café found with the given ID."
            }
        )


# ---------------------------- DELETE CAFE ---------------------------- #

@app.route("/report-closed/<int:caf_id>", methods=["DELETE"])
def delete_cafe(caf_id):
    """
    Deletes a café from the database.

    Requires a valid API key.
    """

    api_key = request.args.get("apikey")

    if api_key != secret_key:

        return jsonify(
            response="You are not authorized to perform this action."
        )

    data = db.session.execute(
        db.select(Cafe).where(Cafe.id == caf_id)
    ).scalar()

    if data is None:

        return jsonify(
            response={
                "Failed": "No café found with the given ID."
            }
        )

    db.session.delete(data)
    db.session.commit()

    return jsonify(
        response={
            "success": "Successfully deleted the café."
        }
    )


# ---------------------------- START APPLICATION ---------------------------- #

if __name__ == "__main__":
    app.run(debug=True)