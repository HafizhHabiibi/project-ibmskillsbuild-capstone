from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

# load encironmetn variable
load_dotenv()

# inisiasi ekstension
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # load configurations
    from .config import Config
    app.config.from_object(Config)

    # initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # register blueprint
    from .routes import main
    app.register_blueprint(main)

    return app