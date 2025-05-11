import os
import uuid
from flask import Blueprint, render_template, request, jsonify, current_app, abort
from app import db
from app.models import Phrase
from app.services.translation import translate_to_korean
from app.services.audio import generate_audio
from app.utils.validators import validate_phrase
from functools import wraps
import time

main = Blueprint("main", __name__)

# Simple rate limiter
request_history = {}


def rate_limit(limit_per_minute=10):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Get client IP
            ip = request.remote_addr
            current_time = time.time()

            # Initialize or clean up old requests
            if ip not in request_history:
                request_history[ip] = []
            request_history[ip] = [
                t for t in request_history[ip] if current_time - t < 60
            ]

            # Check if rate limit exceeded
            if len(request_history[ip]) >= limit_per_minute:
                current_app.logger.warning(f"Rate limit exceeded for IP: {ip}")
                abort(429)

            # Add current request
            request_history[ip].append(current_time)

            return f(*args, **kwargs)

        return decorated_function

    return decorator


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/library")
def library():
    page = request.args.get("page", 1, type=int)
    per_page = 10
    phrases = Phrase.query.order_by(Phrase.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    return render_template("library.html", phrases=phrases)


@main.route("/api/translate", methods=["POST"])
@rate_limit(limit_per_minute=10)
def api_translate():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        english_text = data.get("text", "").strip()

        # Validate input
        is_valid, error_msg = validate_phrase(english_text)
        if not is_valid:
            return jsonify({"error": error_msg}), 400

        # Translate to Korean
        current_app.logger.info(f"Translating: {english_text}")
        korean_text = translate_to_korean(english_text)

        # Create unique filename with UUID to avoid collisions
        unique_id = str(uuid.uuid4())[:8]
        safe_text = "".join(
            c for c in english_text.lower().replace(" ", "_") if c.isalnum() or c == "_"
        )
        filename = f"{safe_text[:30]}_{unique_id}.mp3"
        filepath = os.path.join(current_app.config["AUDIO_DIR"], filename)

        # Generate audio
        current_app.logger.info(f"Generating audio for: {korean_text}")
        generate_audio(korean_text, filepath)

        # Save to database
        phrase = Phrase(
            english_text=english_text,
            korean_text=korean_text,
            audio_path=f"/static/audio/{filename}",
        )
        db.session.add(phrase)
        db.session.commit()

        return jsonify(phrase.to_dict())

    except ValueError as e:
        current_app.logger.error(f"Validation error: {str(e)}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        current_app.logger.error(f"Translation API error: {str(e)}")
        return jsonify(
            {"error": "An error occurred during translation or audio generation"}
        ), 500


@main.route("/api/phrases", methods=["GET"])
def api_phrases():
    try:
        page = request.args.get("page", 1, type=int)
        per_page = 20

        phrases = Phrase.query.order_by(Phrase.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )

        return jsonify(
            {
                "phrases": [p.to_dict() for p in phrases.items],
                "total": phrases.total,
                "pages": phrases.pages,
                "current_page": page,
            }
        )
    except Exception as e:
        current_app.logger.error(f"Error fetching phrases: {str(e)}")
        return jsonify({"error": "Failed to retrieve phrases"}), 500
