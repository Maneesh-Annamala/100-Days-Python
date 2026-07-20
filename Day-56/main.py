from flask import Flask, render_template
from post import Post
import requests


app = Flask(__name__)
blog_response = requests.get("https://api.npoint.io/c790b4d5cab58020d391")
blog_data = blog_response.json()

all_posts =[]
for blog in blog_data:
    post = Post(blog["id"],blog["title"],blog["subtitle"],blog["body"])
    all_posts.append(post)

@app.route('/')
def home():
    
    return render_template("index.html",blogs=blog_data)

@app.route("/post/<index>")
def get_post(index):
    for p in all_posts:
        if p.id == int(index):
            blog_title = p.title
            blog_subtitle = p.subtitle
            blog_body = p.body
            return render_template("post.html",title=blog_title,subtitle=blog_subtitle,body=blog_body)
    
if __name__ == "__main__":
    app.run(debug=True)
