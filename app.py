from flask import Flask, render_template, request,redirect,url_for,session
import os
from db import db, connect_db
import models
from werkzeug.security import generate_password_hash, check_password_hash

app=Flask(__name__)

app.secret_key=os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"]=connect_db()
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
db.init_app(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/profile")
def profile():
    user_id=session.get("user_id")
    if not user_id:
        return redirect(url_for("register"))

    user = models.User.query.get(user_id)
    if not user:
        session.clear()
        return redirect(url_for("register"))
    
    return render_template("profile.html", user=user) ## user для кода шабонизатора Jinja2 в html
    
    


@app.route("/register",methods=["GET","POST"])
def register():
    if request.method == "POST":
        last_name=request.form.get("last-name")
        first_name=request.form.get("first-name")
        email=request.form.get("email")
        password=request.form.get("password")
        confirm_password=request.form.get("confirm-password")
        
        if password!=confirm_password:
            return "Пароли не совпадают",400
        if len(password)<6:
            return "Пароль должен содержать не мнее 6 символов", 400
        if models.User.query.filter_by(email=email).first():
            return "Пользователь уже существует",400
        hashed_password = generate_password_hash(password)

        user=models.User(
            email = email,
            bank_requisites = "None",
            password_hash = hashed_password,
            first_name = first_name,
            last_name = last_name,
            role = "user"
        )

        db.session.add(user)
        db.session.commit()

        history=models.History(
            user_id=user.id,
            table_name="users",
            doing="insert",
            new_data={
                "email":email,
                "first_name":first_name,
                "last_name":last_name,
            }
        )
        db.session.add(history)
        db.session.commit()
        session["user_id"] = user.id
        return redirect(url_for("profile"))
    return render_template("sgin.html")


@app.route("/login",methods=["GET","POST"])
def login():
    if request.method == "POST":
        
        email=request.form.get("email")
        password=request.form.get("password")
        
        
        user = models.User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password_hash,password):
            session["user_id"] = user.id
            return redirect(url_for("profile"))
        
        else:
            return "неверный email или пароль", 401
    return render_template("login.html")

# @app.route("/<page>.html")
# def html_page(page):
#     return render_template(f"{page}.html")

if __name__=="__main__":
    app.run(debug=True,port=5001)