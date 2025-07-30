import os
import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()

# create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# configure the database - using SQLite as required
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///parking_management.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# initialize extensions
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'

@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))

with app.app_context():
    # Import models and routes
    import models
    import routes
    
    # Create all tables
    db.create_all()
    
    # Create admin user automatically if it doesn't exist
    from werkzeug.security import generate_password_hash
    admin = models.User.query.filter_by(username='admin').first()
    if not admin:
        admin_user = models.User(
            username='admin',
            email='admin@parkingmanagement.com',
            password_hash=generate_password_hash('admin123'),
            is_admin=True
        )
        db.session.add(admin_user)
        db.session.commit()
        print("✅ Admin user created automatically!")
        admin = models.User()
        admin.username = 'admin'
        admin.email = 'admin@parking.com'
        admin.password_hash = generate_password_hash('admin123')
        admin.is_admin = True
        db.session.add(admin)
        db.session.commit()
        logging.info("Admin user created with username: admin, password: admin123")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
