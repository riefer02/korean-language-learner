import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-key-change-in-production")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", f"sqlite:///{os.path.join(basedir, 'korean_learner.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    AUDIO_DIR = os.path.join(basedir, "app/static/audio")
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB max upload

    # Environment-specific configs
    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False

    @staticmethod
    def init_app(app):
        # Production logging setup
        import logging
        from logging.handlers import RotatingFileHandler

        file_handler = RotatingFileHandler("app.log", maxBytes=10240, backupCount=10)
        file_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"
            )
        )
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info("Korean Language Learner startup")


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
