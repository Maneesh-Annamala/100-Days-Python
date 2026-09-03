from flask import Flask,redirect,render_template,abort,flash,url_for,request
from flask_login import login_required,login_user,logout_user,current_user,LoginManager
from werkzeug.security import generate_password_hash,check_password_hash
from functools import wraps
from forms import *
from database import *
from flask_ckeditor import CKEditor
import os
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

ckeditor = CKEditor(app)
db.init_app(app)

login_manager = LoginManager(app)

with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(Users,int(user_id))

def adminonly(func):
    @wraps(func)
    def decorator(*args,**kwargs):
        if not current_user.is_authenticated:
            return current_user.unauthorized()
        if current_user.id != 1:
            return abort(404)
        return func(*args,**kwargs)
    return decorator 

@app.route("/product/add_product",methods=["GET","POST"])
@login_required
@adminonly
def add_product():
    product_form = AddProduct()
    if product_form.validate_on_submit():
        product = Products(
            title = product_form.title.data,
            img_link = product_form.img_link.data,
            prod_link = product_form.prod_link.data,
            description = product_form.description.data,
            category = product_form.category.data,
            price = product_form.price.data,
            discount = product_form.discount.data,
            brand = product_form.brand.data
        )
        db.session.add(product)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("add_product.html",product_form=product_form)


@app.route("/register",methods=["GET","POST"])
def register():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        password = generate_password_hash(register_form.password.data,method="pbkdf2:sha256",salt_length=8)
        email = register_form.email.data
        check = db.session.execute(db.select(Users).where(Users.email == email)).scalar()
        if check:
            flash("Already have an account with this mail")
            return redirect(url_for('login'))
        else:
            register_user = Users(username=register_form.username.data,
                                email=register_form.email.data,
                                password=password)
            db.session.add(register_user)
            db.session.commit()
            login_user(register_user)
            return redirect(url_for('home'))
    return render_template("register.html",form=register_form)

@app.route("/login",methods=["GET","POST"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        email = login_form.email.data
        password = login_form.password.data
        email_check = db.session.execute(db.select(Users).where(Users.email == email)).scalar()
        if email_check:
            if check_password_hash(email_check.password,password):
                login_user(email_check)
                return redirect(url_for("home"))
            else:
                flash("Invalid Password")
                return redirect(url_for('login'))
        else:
            flash("Invalid Email")
            return redirect(url_for('login'))
    return render_template("login.html",form=login_form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route("/")
def home():
    products = db.session.execute(db.select(Products)).scalars().all()
    return render_template("index.html",products=products)

@app.route("/product/<int:prod_id>",methods=["GET","POST"])
def show_product(prod_id):
    product = db.get_or_404(Products,prod_id)
    review = ReviewForm()
    if review.validate_on_submit():
        if current_user.is_authenticated:
            review_data = Reviews(
                product_id = product.id,
                user_id = current_user.get_id(),
                review = review.review.data
            )
            db.session.add(review_data)
            db.session.commit()
            return redirect(url_for("show_product",prod_id=prod_id))
        flash("You need to login or register first")
        return redirect(url_for('login'))
    return render_template("product.html",current_user=current_user,review=review,product=product)

@app.route("/product/search")
def search():
    query = request.args.get("q","").lower()
    requested_products = db.session.execute(db.select(Products).where(Products.title.ilike(f"%{query}%"))).scalars().all()
    return render_template("search.html",products=requested_products)

@app.route("/products/cart_items/<int:prod_id>",methods=["POST"])
@login_required
def add_cart(prod_id):
    quantity = int(request.form["quantity"])
    cart_item = Cart.query.filter_by(product_id=prod_id,user_id=current_user.id).first() 
    if cart_item:
        cart_item.quantity += quantity
    else:        
        cart_item = Cart(
            product_id = prod_id,
            user_id = current_user.get_id(),
            quantity = quantity
        )
        db.session.add(cart_item)
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/product/goto_cart")
def goto_cart():
    cart_products = db.session.execute(db.select(Cart).where(Cart.user_id == current_user.get_id())).scalars().all()
    total = 0
    for item in cart_products:
        total += item.prod_rel.price * item.quantity
    return render_template("cart.html",products=cart_products,total=total)

@app.route("/product/wishlist/<int:prod_id>",methods=["POST"])
@login_required
def add_wishlist(prod_id):
    prod = Wishlist(
        product_id = prod_id,
        user_id = current_user.get_id()
    )
    db.session.add(prod)
    db.session.commit()
    return redirect(url_for("home"))
   
@app.route("/product/wishlist")
def wishlist():
    wishlited_prods = db.session.execute(db.select(Wishlist).where(Wishlist.user_id == current_user.get_id())).scalars().all()
    return render_template("wishlist.html",products=wishlited_prods)

@app.route("/product/checkout", methods=["GET", "POST"])
@login_required
def checkout():
    cart_products = db.session.execute(db.select(Cart).where(Cart.user_id == current_user.id)).scalars().all()
    if not cart_products:
        flash("Your cart is empty.")
        return redirect(url_for("home"))

    total = 0 
    for item in cart_products:
        total += item.prod_rel.price * item.quantity
    if request.method == "POST":
        order = Orders(
            user_id=current_user.id,
            total_amount=total ,
            payment_status="pending"
        )
        db.session.add(order)
        db.session.commit()
        for item in cart_products:
            order_item = OrderItems(
                order_id=order.id,
                product_id=item.product_id,
                quantity=item.quantity,
                price=item.prod_rel.price
            )
            db.session.add(order_item)
        db.session.commit()
        return redirect(url_for("payment", order_id=order.id))
    return render_template(
        "checkout.html",
        products=cart_products,
        total=total
    )

@app.route("/payment/<int:order_id>", methods=["GET", "POST"])
@login_required
def payment(order_id):
    order = db.get_or_404(Orders, order_id)
    if order.user_id != current_user.id:
        abort(403)
    if request.method == "POST":
        order.payment_status = "paid"
        db.session.commit()
        Cart.query.filter_by(user_id=current_user.id).delete()
        db.session.commit()
        return redirect(url_for("order_success",order_id=order.id))
    return render_template("payment.html",order=order)

@app.route("/order-success/<int:order_id>")
@login_required
def order_success(order_id):
    order = db.get_or_404(Orders, order_id)
    if order.user_id != current_user.id:
        abort(403)
    return render_template("order_success.html",order=order)
if __name__ == "__main__":
    app.run(debug=True)
