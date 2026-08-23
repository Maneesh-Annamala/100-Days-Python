from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,EmailField
from wtforms.validators import DataRequired


class NewTaskForm(FlaskForm):
    title = StringField("Title",validators=[DataRequired()])
    description = StringField("Description",validators=[DataRequired()])
    submit = SubmitField("Submit")

# Create a form to register new users
class RegisterForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    submit = SubmitField("Sign Up")


# Create a form to login existing users
class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")
