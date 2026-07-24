from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import DataRequired, Length, Email
from flask_bootstrap import Bootstrap5

"""
A Flask login application using Flask-WTF forms
and Bootstrap styling.

The application validates user input and grants
or denies access based on predefined credentials.
"""

app = Flask(__name__)

# Initialize Bootstrap
bootstrap = Bootstrap5(app)

# Secret key required for CSRF protection
app.config["SECRET_KEY"] = "maneesh"

# Dummy user credentials
username = "maneesh"
mail = "maneesh@gmail.com"
password = "123@12345"


class MyForm(FlaskForm):
    """Defines the login form and its validation rules."""

    # Username field
    name = StringField(
        label="name",
        validators=[
            DataRequired(message="It's a mandatory field")
        ]
    )

    # Email field
    email = EmailField(
        label="email",
        validators=[
            DataRequired(message="It's a mandatory field"),
            Email(message="That's not a valid email")
        ]
    )

    # Password field
    password = PasswordField(
        label="password",
        validators=[
            DataRequired(),
            Length(
                min=8,
                message="Password must contain at least 8 characters"
            )
        ]
    )

    # Submit button
    submit = SubmitField(label="Submit")


# ---------------------------- HOME PAGE ---------------------------- #

@app.route("/")
def home():
    """Displays the home page."""

    return render_template(
        "index.html",
        bootstrap=bootstrap
    )


# ---------------------------- LOGIN PAGE ---------------------------- #

@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Displays the login form.

    If the submitted credentials match the predefined
    user credentials, the success page is shown.
    Otherwise, access is denied.
    """

    form = MyForm()

    if form.validate_on_submit():

        # Validate entered credentials
        if (
            form.name.data == username
            and form.email.data == mail
            and form.password.data == password
        ):
            return render_template("success.html")

        else:
            return render_template("denied.html")

    return render_template(
        "login.html",
        form=form
    )


# ---------------------------- START APPLICATION ---------------------------- #

if __name__ == "__main__":
    app.run(debug=True)