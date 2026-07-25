from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField, SelectField
from wtforms.validators import DataRequired
import csv

"""
A Flask web application for managing a list of cafés.

Users can add new cafés with their details such as
location, opening hours, ratings, and socket availability.
The submitted data is stored in a CSV file and displayed
on a separate page.
"""

app = Flask(__name__)

# Secret key used for CSRF protection
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'

# Initialize Bootstrap
Bootstrap5(app)


class CafeForm(FlaskForm):
    """Form used to collect café information."""

    # Café name
    cafe = StringField('Cafe name',validators=[DataRequired()])

    # Google Maps location URL
    location = URLField('Location link',validators=[DataRequired()])

    # Opening time
    opening = StringField('Open time (e.g. 7 AM)',validators=[DataRequired()])

    # Closing time
    closing = StringField('Closing time (e.g. 9 PM)',validators=[DataRequired()])

    # Coffee rating
    coffee_rating = SelectField('Coffee rating',
        choices=[
            "☕️",
            "☕️☕️",
            "☕️☕️☕️",
            "☕️☕️☕️☕️",
            "☕️☕️☕️☕️☕️"
        ],
        validators=[DataRequired()]
    )

    # Wi-Fi rating
    wifi_rating = SelectField('Wi-Fi rating',
        choices=[
            "✘",
            "💪",
            "💪💪",
            "💪💪💪",
            "💪💪💪💪",
            "💪💪💪💪💪"
        ],
        validators=[DataRequired()]
    )

    # Socket availability
    sockets = SelectField('Socket availability',
        choices=[
            "✘",
            "🔌",
            "🔌🔌",
            "🔌🔌🔌",
            "🔌🔌🔌🔌",
            "🔌🔌🔌🔌🔌"
        ],
        validators=[DataRequired()]
    )

    # Submit button
    submit = SubmitField('Submit')


# ---------------------------- HOME PAGE ---------------------------- #

@app.route("/")
def home():
    """Displays the home page."""

    return render_template("index.html")


# ---------------------------- ADD CAFE ---------------------------- #

@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    """
    Displays the café submission form.

    When the form is submitted successfully,
    the café details are appended to the CSV file.
    """

    form = CafeForm()

    if form.validate_on_submit():

        with open(
            'cafe-data.csv',
            mode='a',
            newline='',
            encoding='utf-8'
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                form.cafe.data,
                form.location.data,
                form.opening.data,
                form.closing.data,
                form.coffee_rating.data,
                form.wifi_rating.data,
                form.sockets.data
            ])

        # Redirect back to the form after successful submission
        return redirect(url_for('add_cafe'))

    return render_template('add.html', form=form)


# ---------------------------- VIEW CAFES ---------------------------- #

@app.route('/cafes')
def cafes():
    """Reads all café records from the CSV file and displays them."""

    with open(
        'cafe-data.csv',
        newline='',
        encoding='utf-8'
    ) as csv_file:

        csv_data = csv.reader(csv_file, delimiter=',')

        list_of_rows = []

        for row in csv_data:
            list_of_rows.append(row)

    return render_template(
        'cafes.html',
        cafes=list_of_rows
    )


# ---------------------------- START APPLICATION ---------------------------- #

if __name__ == '__main__':
    app.run(debug=True)
