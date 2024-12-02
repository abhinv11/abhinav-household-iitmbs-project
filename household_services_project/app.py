# Starting of app
from flask import Flask
from backend.models import db, User, UserRole

app = None

def setup_app():
    global app  # Ensure `app` is accessible globally
    app = Flask(__name__)
    app.secret_key = 'e8f7c3f8c4b94a9dbf213f9e3c8f32ba'  # Example key

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///household_services.sqlite3"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # Optional, to suppress warnings
    db.init_app(app)  # Connect Flask app to SQLite database (SQLAlchemy)

    # Create tables and add admin user if not exists
    with app.app_context():
        db.create_all()  # Creates the database if it doesn't already exist
        
        # Check if the admin user exists
        admin_user = User.query.filter_by(role=UserRole.ADMIN).first()
        if not admin_user:
            # Create admin user
            admin_user = User(
                id=1,  # Ensure admin ID is always 1
                full_name="Admin",
                email="admin@gmail.com",
                role=UserRole.ADMIN,
                password="admin123",
                is_active=True
            )
            db.session.add(admin_user)
            db.session.commit()
            print("Admin user created with ID 1, role ADMIN, and password 'admin123'.")

    app.app_context().push()  # Allow direct access to other modules
    app.debug = True
    print("Household service app is started.")

# Call the setup
setup_app()

from backend.controllers import *

if __name__ == "__main__":
    app.run()

