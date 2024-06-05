from flask import Blueprint, render_template, redirect, request, url_for, session
from tinydb import TinyDB, Query
from .sendfeedback import send_email

# Initialize Flask Blueprint
views = Blueprint("views", __name__)

# TinyDB setup
db = TinyDB("posts.json")
posts_table = db.table("posts")

# Password for admin access
password = "keychain14"
error_message = None
success_message = None


@views.route("/documentation")
def documentation():
    return render_template("documentation.html")

@views.route("/")
def blog():
    posts = posts_table.all()
    return render_template("index.html", posts=reversed(posts))

@views.route("/admin", methods=["GET", "POST"])
def admin():
    global error_message, success_message, password

    if "isadmin" not in session:
        session["isadmin"] = False

    error_message = None
    success_message = None
    if request.method == 'POST':
        if "post-submit" in request.form:
            title = request.form.get("post-title")
            post_id = request.form.get("post-id")
            content = request.form.get("post-content")

            Post = Query()
            if not posts_table.contains(Post.id == post_id):
                posts_table.insert({"id": post_id, "title": title, "content": content})
                success_message = "Post added successfully!"
                error_message = None
            else:
                error_message = "ID already in use!"
                success_message = None

        if "delete-post" in request.form:
            post_to_delete = request.form.get("post-id")

            Post = Query()
            if posts_table.contains(Post.id == post_to_delete):
                posts_table.remove(Post.id == post_to_delete)
                success_message = "Post deleted successfully!"
                error_message = None
            else:
                error_message = "Post ID not found!"
                success_message = None


        if "change-password" in request.form:
            new_password = request.form.get("password")

            if len(new_password) > 6:
                password = new_password
                success_message = f"{password} set as the new password successfully!"

            else: 
                error_message = "Error, password is too short!"
                

    if session["isadmin"] != False:
        return render_template("admin.html", posts=posts_table.all(), error_message=error_message, success_message=success_message)
    else:
        return redirect(url_for("views.logout"))





@views.route("/login", methods=["GET", "POST"])
def login():
    if "isadmin" not in session:
        session["isadmin"] = False

    if request.method == "POST":
        attempted_password = request.form.get("password")

        if attempted_password == password:
            session["isadmin"] = True
            return redirect(url_for("views.admin"))

    return render_template("login.html")

feedback_sent = False

@views.route("/feedback", methods=["GET", "POST"])
def feedback():
    global feedback_sent
    feedback_sent = False
    if request.method == 'POST':
        feedback = request.form.get("feedback")
        send_email("SITE USER FEEDBACK", "victoryphili0@gmail.com", feedback)
        send_email("SITE USER FEEDBACK", "rynstheoverlord@gmail.com", feedback)
        feedback_sent = True
    return render_template("feedback.html", feedback_sent=feedback_sent)

@views.route("/logout")
def logout():
    session["isadmin"] = False
    return redirect(url_for("views.login"))