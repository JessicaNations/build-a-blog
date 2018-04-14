from flask import Flask, request, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://build-a-blog:YES@localhost:8889/build-a-blog"
app.config["SQLALCHEMY_ECHO"] = True
db = SQLAlchemy(app)

#create class for blog posts (5000 char limit on content set to approx 1000 words)
class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    content = db.Column(db.String(6000))
   

    def __init__(self, title, content):
        self.title = title
        self.content = content



#APP ROUTES / HANDLERS
#root directory just redirects to main blog page
@app.route("/")
def redirector():
    return redirect("/blog")

@app.route("/blog", methods=["POST", "GET"])
def index():
    #the form should direct to /newpost instead, it would make error handling a lot cleaner         
    if request.method == "POST":
        new_title = request.form["title"]
        new_content = request.form["content"]

        if not new_title or not new_content:
            return render_template("newpost.html",title=new_title, content=new_content, error_message="DON'T BE SO STUPID")

        new_post = Blog(new_title, new_content)
        db.session.add(new_post)
        db.session.commit()
        return redirect("/blog?id="+str(new_post.id))
    
    view_post_id = request.args.get("id")
    if view_post_id:
        view_post = Blog.query.get(int(view_post_id))
    else:
        view_post = ""
    
    posts = Blog.query.order_by(Blog.id.desc()).all()

    return render_template("blog.html", posts=posts, view_post=view_post)

@app.route("/newpost", methods=["GET"])
def add_post():
    return render_template("newpost.html")

#only run when supposed to
if __name__ == "__main__":
    app.run()