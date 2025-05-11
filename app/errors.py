from flask import render_template, jsonify, request


def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found_error(error):
        if request.path.startswith("/api/"):
            return jsonify({"error": "Resource not found"}), 404
        return render_template("error.html", error="Page not found"), 404

    @app.errorhandler(500)
    def internal_error(error):
        if request.path.startswith("/api/"):
            return jsonify({"error": "Internal server error"}), 500
        return render_template("error.html", error="An internal error occurred"), 500

    @app.errorhandler(429)
    def too_many_requests(error):
        if request.path.startswith("/api/"):
            return jsonify({"error": "Too many requests"}), 429
        return render_template(
            "error.html", error="Too many requests. Please try again later."
        ), 429

    @app.errorhandler(400)
    def bad_request(error):
        if request.path.startswith("/api/"):
            return jsonify({"error": str(error)}), 400
        return render_template("error.html", error="Bad request"), 400
