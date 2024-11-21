from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from website.models import db, User  # Correct import for db and User from website.models
from werkzeug.security import generate_password_hash
from flask_migrate import Migrate

migrate = Migrate()
# Initialize the login manager
login_manager = LoginManager()
login_manager.login_view = "auth.sign_in"  # This tells Flask-Login to redirect to the sign-in route

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "your_secret_key_here"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"

    # Initialize the app with the database and login manager
    db.init_app(app)  # Pass the app to db.init_app, don't reinitialize db
    migrate.init_app(app, db)
    login_manager.init_app(app)

    from .auth import auth  # Import auth blueprint
    from .views import views  # Import views blueprint

    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(views, url_prefix="/")

    return app


# This function tells Flask-Login how to load a user from the database
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))  # Fetch the user by their ID


app = create_app()  # Create the app instance


@app.before_request
def create_admin():
    # Check if an admin exists already to prevent duplicate admin accounts
    admin_user = User.query.filter_by(email="admin@example.com").first()

    if not admin_user:
        # Create an admin user if it doesn't exist
        hashed_password = generate_password_hash("adminpassword", method="sha256")  # Set admin password
        admin = User(username="admin", email="admin@example.com", password=hashed_password, is_admin=True)
        db.session.add(admin)
        db.session.commit()
        print("Admin user created!")


# Make sure you also initialize the database with the app context
with app.app_context():
    db.create_all()  # This will create the tables (including the new `is_admin` field)

