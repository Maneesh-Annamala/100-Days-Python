from flask import Flask,render_template
import requests
from post import Post


URL = " https://api.npoint.io/d9fe9817b80cb90b4598"

app = Flask(__name__)

response = requests.get(URL)
blogs_data = response.json()

blog_obj = []
for blog in blogs_data:
    n = Post(blog["id"],blog["title"],blog["subtitle"],blog["body"],blog['image_url'])
    blog_obj.append(n)

@app.route("/")
def blogs():
    return render_template("index.html",blogs_data=blogs_data)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/post/<index>")
def get_post(index):
    for p in blog_obj:
        if p.id == int(index):
            title = p.title
            subtitle = p.subtitle
            body = p.body
            link = p.link
            return render_template("post.html",title=title,subtitle=subtitle,body=body,link=link)

if __name__ == "__main__":
    app.run(debug=True)