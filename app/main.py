"""Quote API - a tiny Flask app used to practise CI/CD pipelines."""
import os
import random

from flask import Flask, jsonify

QUOTES = [
    {"text": "Talk is cheap. Show me the code.", "author": "Linus Torvalds"},
    {"text": "Simplicity is prerequisite for reliability.", "author": "Edsger W. Dijkstra"},
    {"text": "First, solve the problem. Then, write the code.", "author": "John Johnson"},
    {"text": "Make it work, make it right, make it fast.", "author": "Kent Beck"},
    {"text": "Automate all the things.", "author": "DevOps proverb"},
    {"text": "If it hurts, do it more often.", "author": "Martin Fowler"},
    {"text": "Any fool can write code that a computer can understand. "
             "Good programmers write code that humans can understand.",
     "author": "Martin Fowler"},
]


def create_app():
    """Application factory (makes the app easy to test)."""
    app = Flask(__name__)

    @app.get("/health")
    def health():
        return jsonify(status="ok"), 200

    @app.get("/quote")
    def quote():
        return jsonify(random.choice(QUOTES)), 200

    @app.get("/version")
    def version():
        # Set by the pipeline, e.g. -e APP_VERSION=<git commit sha>
        return jsonify(version=os.getenv("APP_VERSION", "dev")), 200

    @app.errorhandler(404)
    def not_found(_error):
        return jsonify(error="not found"), 404

    return app


app = create_app()

if __name__ == "__main__":  # local run: python -m app.main
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")))
