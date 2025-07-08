from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    # ایمپورت و ثبت بلوپرینت‌ها
    from app.api.webhook import bp as webhook_bp
    app.register_blueprint(webhook_bp)

    return app
