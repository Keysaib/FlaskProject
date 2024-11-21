from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
import re # Import regular expression module for password validation
from .models import User
from . import db

auth = Blueprint("auth", __name__)

@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        password_confirm = request.form.get("password_confirm")

        # Check if email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email is already in use, please choose another one.", category="error")
            return render_template("sign_up.html")

        # Validation logic
        if password != password_confirm:
            flash("Passwords must match.", category="error")
        
        # Check password requirements
        elif len(password) < 8:
            flash("Password must be at least 8 characters long.", category="error")
        
        elif not re.search(r"[A-Za-z]", password):  # Check if the password contains letters
            flash("Password must contain at least one letter.", category="error")
        
        elif not re.search(r"\d", password):  # Check if the password contains digits
            flash("Password must contain at least one number.", category="error")
        
        elif not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):  # Check if password contains special characters
            flash("Password must contain at least one special character.", category="error")
        
        else:
            # If all validations pass, create the new user
            hashed_password = generate_password_hash(password, method="pbkdf2:sha256")
            user = User(email=email, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            flash("Account created!", category="success")
            login_user(user, remember=True)
            return redirect(url_for("auth.sign_in"))
    
    return render_template("sign_up.html")

# Sign In Route
@auth.route("/sign-in", methods=["GET", "POST"])
def sign_in():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            flash("Logged in successfully!", category="success")
            login_user(user, remember=True)
            return redirect(url_for("views.Home"))
        else:
            flash("Invalid credentials, please try again.", category="error")

    return render_template("index.html")

# Forgot Password Route
@auth.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form.get("email")
        user = User.query.filter_by(email=email).first()

        if user:
            flash("Password reset link sent to your email.", category="info")
            # Here you would normally send the reset link via email
        else:
            flash("Email not found, Please make an account.", category="error")
        
    return render_template("forgot_password.html")

# Log out route
@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.sign_in"))
