from flask import Flask,render_template,redirect,url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired,Length
from wtforms import StringField,SubmitField,EmailField
import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
MY_MAIL = os.getenv("MY_MAIL")
MY_PASSWORD = os.getenv("MY_PASSWORD")
Bootstrap5(app) 

class ContactForm(FlaskForm):
    Name = StringField("Name",validators=[DataRequired(),Length(min=3)])
    purpose = StringField("Purpose",validators=[DataRequired()])
    mobile = StringField("Mobile",validators=[DataRequired()])
    email = EmailField("E-mail",validators=[DataRequired()])
    submit = SubmitField("submit")


@app.route("/")
def interface():
    return render_template("index.html")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/contact",methods=['GET','POST'])
def contact():
    form_data = ContactForm()
    if form_data.validate_on_submit():
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:

            # Secure the SMTP connection
            connection.starttls()

            # Login to Gmail
            connection.login(
                MY_MAIL,
                MY_PASSWORD
            )
            connection.sendmail(
                from_addr=MY_MAIL,
                to_addrs=MY_MAIL,
                msg = "Subject:Mail from Web\n\n"
                        f"""Name:{form_data.Name.data}\n
                        Purpose : {form_data.purpose.data}\n
                        Mobile :{form_data.mobile.data}\n
                        Email : {form_data.email.data}"""
            )
        return redirect(url_for("home"))
    return render_template("contact.html",form_data=form_data)

if __name__ == "__main__":
    app.run(debug=True)
