import os

from flask import Flask
from flask_migrate import Migrate

from config import Config
from app.db import db
from app.routes.product_routes import product_bp
from app import models

migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__)

    app.config.from_object(config_class)

    os.makedirs(app.instance_path, exist_ok=True)

    db.init_app(app)
    migrate.init_app(app, db)
    app.register_blueprint(product_bp)

    @app.route("/")
    def index():
        return {
            "application": "Product Intelligence System",
            "status": "running"
        }

    return app