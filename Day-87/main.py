from flask import Flask, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from database import Tasks,Users,db
from forms import NewTaskForm,RegisterForm,LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, LoginManager, current_user, logout_user,login_required


app = Flask(__name__)
# Configure Flask-Login
app.config["SECRET_KEY"] = "ghscgsfdcgdvh62rgef@ds"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///TodoApplication.db"

db.init_app(app)

with app.app_context():
    db.create_all()


login_manager = LoginManager(app)

Bootstrap5(app)

@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(Users, user_id)


@app.route("/register",methods=["GET","POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():

        # Check if user email is already present in the database.
        result = db.session.execute(db.select(Users).where(Users.email == form.email.data))
        user = result.scalar()
        if user:
            # User already exists
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))

        hash_and_salted_password = generate_password_hash(
            form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = Users(
            email=form.email.data,
            name=form.name.data,
            password=hash_and_salted_password,
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("get_tasks"))
    return render_template("register.html", form=form, current_user=current_user)

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        password = form.password.data
        result = db.session.execute(db.select(Users).where(Users.email == form.email.data))
        # Note, email in db is unique so will only have one result.
        user = result.scalar()
        # Email doesn't exist
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login'))
        # Password incorrect
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for("get_tasks"))

    return render_template("login.html", form=form, current_user=current_user)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/tasks")
@login_required
def get_tasks():
    tasks = db.session.execute(db.select(Tasks).where(Tasks.owner_id == current_user.id)).scalars().all()
    return render_template("tasks.html",tasks=tasks)

@app.route("/create_task",methods=["GET","POST"])
@login_required
def create_task():
    task_form = NewTaskForm()
    if task_form.validate_on_submit():
        task = Tasks(
            title = task_form.title.data,
            description = task_form.description.data,
            status = False,
            owner_id = current_user.id
        )
        db.session.add(task)
        db.session.commit()
        return redirect(url_for("get_tasks"))
    return render_template("create_task.html",form=task_form)

@app.route("/delete_task/<int:task_id>",methods=["GET","POST"])
@login_required
def delete_task(task_id):
    task = db.get_or_404(Tasks,task_id)
    if not task.owner_id == current_user.id:
        flash("You are not allowed to delete this")
        return redirect(url_for("get_tasks"))
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("get_tasks"))

@app.route("/edittask/<int:task_id>",methods=["GET","POST"])
@login_required
def edit_task(task_id):
    task = db.get_or_404(Tasks,task_id)
    if not task.owner_id == current_user.id:
        flash("You are not allowed to edit this!")
        return redirect(url_for("get_tasks"))
    task_form = NewTaskForm(obj=task)
    if task_form.validate_on_submit():
        task.title = task_form.title.data
        task.description = task_form.description.data
        db.session.commit()
        return redirect(url_for("get_tasks"))
    return render_template("edit.html",form=task_form)

@app.route("/taskcompleted/<int:task_id>",methods=["GET","POST"])
@login_required
def completed(task_id):
    task = db.get_or_404(Tasks,task_id)
    if not task.owner_id == current_user.id:
        flash("You are not allowed to edit this!")
        return redirect(url_for("get_tasks"))
    task.status = True
    db.session.commit()
    return redirect(url_for("get_tasks"))    

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)


