from flask import Flask
from app.web import web
from app.models import db
import ir

def create_app():
    app = Flask(__name__)
    app.config.from_object("config")
    app.config.from_object('secure')
    db.init_app(app)
    db.create_all(app=app)
    register_buleprint(app)
    return app


def register_buleprint(app):
    app.register_blueprint(web)

