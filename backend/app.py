from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder = "../frontend/templates", static_folder = "../frontend/static")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///csrs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy()
db.init_app(app)

from routes.module_routes import module_routes
app.register_blueprint(module_routes)
