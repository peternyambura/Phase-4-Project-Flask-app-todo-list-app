# __init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

# Initialize the database and migrate extension but do not assign any app yet.
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://todolist_with_api_user:CxtzMktwZmZGssMuKD1xBw5xA8taU0Ew@dpg-cl5bhrq8vr0c73amvhc0-a.oregon-postgres.render.com/todolist_with_api'
    app.config["DEBUG"] = True

    # Initialize extensions with the app context
    db.init_app(app)
    migrate.init_app(app, db)

    # Initialize the LoginManager with the app context
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # Import models and blueprints here to avoid circular imports
    from .models import User, Note, Category
    from .views import views
    from .auth import auth

    # Register blueprints
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app
