from flask import Flask, render_template, request
import requests
import smtplib
from dotenv import load_dotenv
import os

"""
A Flask blog application that displays blog posts,
allows users to view individual posts, and provides
a contact form that sends messages via email.
"""

# Load environment variables
load_dotenv()

# Fetch blog data from API
posts = requests.get("https://api.npoint.io/c790b4d5cab58020d391").json()

app = Flask(__name__)

# Email credentials
MY_MAIL = os.getenv("MAIL")
MY_PASSWORD = os.getenv("PASSWORD")


# ---------------------------- HOME PAGE ---------------------------- #

@app.route('/')
def get_all_posts():
    """Displays all blog posts on the home page."""
    return render_template("index.html", all_posts=posts)


# ---------------------------- ABOUT PAGE ---------------------------- #

@app.route("/about")
def about():
    """Displays the About page."""
    return render_template("about.html")


# ---------------------------- CONTACT PAGE ---------------------------- #

@app.route("/contact", methods=["GET", "POST"])
def contact():
    """
    Displays the contact page.

    If the user submits the contact form,
    sends the details to the configured email.
    """

    if request.method == "POST":

        # Retrieve submitted form data
        data = request.form

        # Send email containing user details
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(MY_MAIL, MY_PASSWORD)

            connection.sendmail(
                from_addr=MY_MAIL,
                to_addrs=MY_MAIL,
                msg="Subject:Users Data\n\n"
                    f"Name: {data['name']}\n"
                    f"Email: {data['email']}\n"
                    f"Phone Number: {data['phone']}\n"
                    f"Message: {data['message']}"
            )

        return render_template("contact.html", msg_sent=True)

    return render_template("contact.html", msg_sent=False)


# ---------------------------- BLOG POST PAGE ---------------------------- #

@app.route("/post/<int:index>")
def show_post(index):
    """Displays the selected blog post."""

    requested_post = None

    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post

    return render_template("post.html", post=requested_post)


# ---------------------------- START APPLICATION ---------------------------- #

if __name__ == "__main__":
    app.run(debug=True, port=5001)