"""Web Interface for RAG System -- Flask application with HTML pages."""
import os
import logging
from flask import Flask, render_template, request, redirect, url_for, send_file, jsonify
from werkzeug.utils import secure_filename
from pathlib import Path

from core.search_engine import create_search_engine
from config.settings import WEB_CONFIG, IMAGE_CONFIG, METADATA_CATEGORIES

logger = logging.getLogger(__name__)

app = Flask(
    __name__,
    template_folder=str(Path(__file__).parent / "templates"),
    static_folder=str(Path(__file__).parent / "static"),
)
app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY", "dev-only-change-in-production")
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024

UPLOAD_FOLDER = Path(__file__).parent / "static" / "uploads"
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
app.config["UPLOAD_FOLDER"] = str(UPLOAD_FOLDER)

search_engine = create_search_engine()

from web.api_routes import api_bp  # noqa: E402
app.register_blueprint(api_bp)


@app.route("/")
def index():
    return render_template("index.html", categories=METADATA_CATEGORIES)


@app.route("/search")
def search():
    query = request.args.get("q", "")
    search_type = request.args.get("type", "text")
    if not query:
        return redirect(url_for("index"))
    if search_type == "text":
        results = search_engine.text_to_image_search(query, limit=20)
    elif search_type == "image":
        results = search_engine.image_to_image_search(query, limit=20)
    else:
        results = search_engine.hybrid_search(query=query, limit=20)
    return render_template("search.html", query=query, search_type=search_type,
                           results=results, categories=METADATA_CATEGORIES)


@app.route("/browse")
def browse():
    try:
        from config.database import get_db_session, ShoeImage
        with get_db_session() as db:
            images = db.query(ShoeImage).limit(100).all()
        return render_template("browse.html", images=images, categories=METADATA_CATEGORIES)
    except Exception as e:
        logger.error(f"Browse failed: {e}")
        return render_template("error.html", error=str(e))


@app.route("/image/<path:filename>")
def serve_image(filename):
    try:
        return send_file(os.path.join(app.config["UPLOAD_FOLDER"], secure_filename(filename)))
    except Exception:
        return jsonify({"error": "Image not found"}), 404


@app.route("/analytics")
def analytics():
    try:
        return render_template("analytics.html", stats=search_engine.get_search_stats())
    except Exception as e:
        return render_template("error.html", error=str(e))


@app.errorhandler(404)
def not_found(error):
    return render_template("error.html", error="Page not found"), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template("error.html", error="Internal server error"), 500


if __name__ == "__main__":
    app.run(host=WEB_CONFIG["host"], port=WEB_CONFIG["port"], debug=WEB_CONFIG["debug"])
