from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

# Initialize Flask and SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///yourdatabase.db'  # Change to your database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'  # Add a secret key for session management
db = SQLAlchemy(app)  # Initialize the SQLAlchemy instance

# Define the User model
class User(UserMixin, db.Model):  # Inherit from UserMixin to use Flask-Login features
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<User {self.email}>'  # Use email instead of username

    # Flask-Login methods (required)
    def get_id(self):
        return str(self.id)  # Flask-Login needs the user ID as a string
    
    @property
    def is_active(self):
        return True  # Consider all users as active for now

    @property
    def is_authenticated(self):
        return True  # This can be more complex, but for simplicity, we return True

    @property
    def is_anonymous(self):
        return False  # Return False for authenticated users

