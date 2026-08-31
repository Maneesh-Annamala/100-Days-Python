import requests
from pprint import pprint
from flask_bootstrap import Bootstrap5
from flask import Flask,render_template,redirect,url_for,flash,request



response = requests.get("https://dummyjson.com/products")

products_data = response.json()

app = Flask(__name__)

def prods(category):
    items = []
    for data in products_data.get("products"):
        if data["category"] == category:
            items.append(data)
    return items

@app.route("/")
def home():
    return render_template("index.html",products=products_data["products"])

@app.route("/search")
def search():

    query = request.args.get("q", "").lower()
    items = []
    for product in products_data["products"]:
        if query in product["title"].lower():
            items.append(product)
    if not items:
        flash("No products found.")
    return render_template("search.html",products=items)

@app.route("/product/beauty")
def beauty():
    items = prods("beauty")
    return render_template("products.html",products=items,category="beauty")

@app.route("/products/fragrances")
def fragrances():
    items = prods("fragrances")
    return render_template("products.html",products=items,category="fragrances")

@app.route("/products/furniture")
def furniture():
    items = prods("furniture")
    return render_template("products.html",products=items,category="furniture")

@app.route("/products/groceries")
def groceries():
    items = prods("groceries")
    return render_template("products.html",products=items,category="groceries")

@app.route("/products/<int:prod_id>")
def view_product(prod_id):
    for data in products_data.get("products"):
        if data["id"] == prod_id:
            return render_template("product.html",product=data)

if __name__ == "__main__":
    app.run(debug=True)