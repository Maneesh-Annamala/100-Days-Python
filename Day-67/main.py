from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

# CREATE DATABASE


class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABSE")
app.config["UPLOAD_FOLDER"] = os.getenv("UPLOAD_FOLDER")
db = SQLAlchemy(model_class=Base)
db.init_app(app)

login_manger = LoginManager()
login_manger.init_app(app)


class User(UserMixin,db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(1000))


with app.app_context():
    db.create_all()

@login_manger.user_loader
def load_user(user_id):
    return db.session.get(User,int(user_id))

@app.route('/')
def home():
    return render_template("index.html",logged_in=current_user.is_authenticated)


@app.route('/register',methods=["GET","POST"])
def register():
    if request.method == 'POST':
        hashed_pass = generate_password_hash(request.form.get("password"),method="pbkdf2:sha256:600000",salt_length=8)
        new_user = User(email=request.form.get("email"),
                    password=hashed_pass,
                    name=request.form.get("name")
                    )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        logged_in = True
        return redirect(url_for("secrets"))
    return render_template("register.html")


@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        result = db.session.execute(db.select(User).where(User.email == email)).scalar()
        if result:
            if check_password_hash(result.password,password):
                login_user(result)
                return redirect(url_for("secrets"))
            else:
                flash("The entered password was wrong")
                return redirect(url_for("login"))
        else:
            flash("Inavlid email please check once")
            
            return redirect(url_for("login"))
    return render_template("login.html")


@app.route('/secrets')
@login_required
def secrets():
    name = current_user.name
    return render_template("secrets.html",name=name)


@app.route('/logout')
def logout():
    
    logout_user()
    return redirect(url_for("home"))


@app.route('/download')
@login_required
def download():
    return send_from_directory(directory=app.config["UPLOAD_FOLDER"],path="cheat_sheet.pdf")


if __name__ == "__main__":
    app.run(debug=True)
