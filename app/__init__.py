from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize SQLAlchemy
db = SQLAlchemy()


def create_app(config_name="default"):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # Ensure audio directory exists with proper permissions
    try:
        os.makedirs(app.config["AUDIO_DIR"], exist_ok=True)
        # Test write access
        test_file = os.path.join(app.config["AUDIO_DIR"], "test_write.txt")
        with open(test_file, "w") as f:
            f.write("test")
        os.remove(test_file)
    except (IOError, PermissionError) as e:
        app.logger.error(f"Failed to access audio directory: {e}")
        raise

    # Initialize extensions
    db.init_app(app)

    # Import and register blueprints
    from app.routes import main as main_blueprint

    app.register_blueprint(main_blueprint)

    # Register error handlers
    from app.errors import register_error_handlers

    register_error_handlers(app)

    return app
