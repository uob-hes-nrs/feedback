from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///csrs.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app) #associates SQLAlchemy instance with Flask .

    # Import and register blueprints
    from routes.module_routes import module_routes
    app.register_blueprint(module_routes) #integrates module_routes blueprint into Flask app

    return app #returns configured app

