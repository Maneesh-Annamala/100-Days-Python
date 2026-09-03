from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,EmailField,PasswordField,IntegerField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditorField


class RegisterForm(FlaskForm):
    username = StringField("Username",validators=[DataRequired()])
    email = EmailField("E-mail",validators=[DataRequired()])
    password = PasswordField("Password",validators=[DataRequired()])
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    email = EmailField("E-mail",validators=[DataRequired()])
    password = PasswordField("Password",validators=[DataRequired()])
    submit = SubmitField("Login")

class AddProduct(FlaskForm):
    title = StringField("Title",validators=[DataRequired()])
    img_link = StringField("Image URL",validators=[DataRequired(),URL()])
    prod_link = StringField("Product URL",validators=[DataRequired(),URL()])
    description = StringField("Description",validators=[DataRequired()])
    category = StringField("Category",validators=[DataRequired()])
    price = IntegerField("Price",validators=[DataRequired()])
    discount = IntegerField("Discount",validators=[DataRequired()])
    brand = StringField("Brand Name",validators=[DataRequired()])
    submit = SubmitField("Submit")

class ReviewForm(FlaskForm):
    review = CKEditorField("Review")
    submit = SubmitField("Post")
