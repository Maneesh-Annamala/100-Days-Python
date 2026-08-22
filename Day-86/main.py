from flask import Flask, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from wtforms import (
    StringField,
    SubmitField,
    URLField,
    IntegerField,
    BooleanField
)
from wtforms.validators import DataRequired
import random


app = Flask(__name__)

app.config["SECRET_KEY"] = "YOUR_SECRET_KEY"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cafes.db"

Bootstrap5(app)


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
db.init_app(app)


class Cafe(db.Model):
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String(250),
        unique=True,
        nullable=False
    )

    map_url: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )

    img_url: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )

    location: Mapped[str] = mapped_column(
        String(250),
        nullable=False
    )

    seats: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    has_toilet: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False
    )

    has_wifi: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False
    )

    has_sockets: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False
    )

    can_take_calls: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False
    )

    coffee_price: Mapped[str] = mapped_column(String(250),nullable=True)


class CafeForm(FlaskForm):
    name = StringField("Cafe Name",validators=[DataRequired()])

    map_url = URLField("Map Link")
    img_url = URLField("Cafe Image")

    location = StringField(
        "Location",
        validators=[DataRequired()]
    )

    seats = IntegerField(
        "Seats",
        validators=[DataRequired()]
    )

    has_toilet = BooleanField("Has Toilets")
    has_wifi = BooleanField("Has WIFI")
    has_sockets = BooleanField("Has Sockets")
    can_take_calls = BooleanField("Can Take Calls")

    coffee_price = StringField(
        "Price",
        validators=[DataRequired()]
    )

    submit = SubmitField("Submit")


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/random")
def get_random():
    data = db.session.execute(
        db.select(Cafe)
    ).scalars().all()

    if not data:
        flash("Database is empty.")
        return redirect(url_for("add"))

    random_cafe = random.choice(data)

    return render_template(
        "cafes.html",
        random_cafe=random_cafe
    )


@app.route("/all")
def all_data():
    data = db.session.execute(
        db.select(Cafe)
    ).scalars().all()

    return render_template(
        "cafes.html",
        cafe=data
    )


@app.route("/search/<loc>")
def search(loc):
    data = db.session.execute(
        db.select(Cafe).where(Cafe.location == loc)
    ).scalars().all()

    return render_template(
        "cafe_by_loc.html",
        cafe=data
    )


@app.route("/add", methods=["GET", "POST"])
def add():
    cafe_form = CafeForm()

    if cafe_form.validate_on_submit():
        cafe = Cafe(
            name=cafe_form.name.data,
            map_url=cafe_form.map_url.data,
            img_url=cafe_form.img_url.data,
            location=cafe_form.location.data,
            seats=cafe_form.seats.data,
            has_toilet=cafe_form.has_toilet.data,
            has_wifi=cafe_form.has_wifi.data,
            has_sockets=cafe_form.has_sockets.data,
            can_take_calls=cafe_form.can_take_calls.data,
            coffee_price=cafe_form.coffee_price.data
        )

        db.session.add(cafe)
        db.session.commit()

        return redirect(url_for("home"))

    return render_template(
        "add_cafe.html",
        form=cafe_form
    )


@app.route("/edit/<int:caf_id>", methods=["GET", "POST"])
def edit(caf_id):
    cafe = db.get_or_404(Cafe, caf_id)
    cafe_form = CafeForm(obj=cafe)

    if cafe_form.validate_on_submit():
        cafe.name = cafe_form.name.data
        cafe.map_url = cafe_form.map_url.data
        cafe.img_url = cafe_form.img_url.data
        cafe.location = cafe_form.location.data
        cafe.seats = cafe_form.seats.data
        cafe.has_toilet = cafe_form.has_toilet.data
        cafe.has_wifi = cafe_form.has_wifi.data
        cafe.has_sockets = cafe_form.has_sockets.data
        cafe.can_take_calls = cafe_form.can_take_calls.data
        cafe.coffee_price = cafe_form.coffee_price.data

        db.session.commit()

        return redirect(url_for("home"))

    return render_template(
        "add_cafe.html",
        form=cafe_form
    )


@app.route("/report-closed/<int:caf_id>", methods=["POST"])
def delete_cafe(caf_id):
    cafe = db.get_or_404(Cafe, caf_id)

    db.session.delete(cafe)
    db.session.commit()

    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)