import os
from app import create_app, db
from app.models import Phrase

# Determine environment
env = os.environ.get("FLASK_ENV", "development")
app = create_app(env)


@app.shell_context_processor
def make_shell_context():
    return {"db": db, "Phrase": Phrase}


@app.cli.command("init-db")
def init_db():
    """Initialize the database."""
    with app.app_context():
        db.create_all()
        print("Database tables created.")


if __name__ == "__main__":
    with app.app_context():
        # Create database tables if they don't exist
        db.create_all()

    host = os.environ.get("FLASK_HOST", "127.0.0.1")
    port = int(os.environ.get("FLASK_PORT", 5000))
    app.run(host=host, port=port, debug=env == "development")
