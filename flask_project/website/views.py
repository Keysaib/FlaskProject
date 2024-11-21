from flask import Blueprint, render_template
from flask_login import login_required, current_user

views = Blueprint("views", __name__)

@views.route("/")
@login_required
def Home():
    return render_template("HomePage.html", user=current_user)

@views.route("/admin-dashboard")
@login_required
def admin_dashboard():
    if not current_user.is_admin:  # Check if the user is an admin
        return "Unauthorized", 403  # Or redirect to another page like home
    return render_template("HomePage.html")