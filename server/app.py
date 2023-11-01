from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db' 
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

from routes import user_routes, task_routes, category_routes

if __name__ == "__main__":
    app.run(debug=True)

migrate = Migrate(app, db)