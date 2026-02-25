"""Flask API routes (JSON endpoints)."""
import os
import uuid
import logging
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename

from core.search_engine import create_search_engine
from core.query_processor import QueryProcessor

logger = logging.getLogger(__name__)

api_bp = Blueprint("api", __name__)

search_engine = create_search_engine()
query_processor = QueryProcessor()


@api_bp.route("/api/search", methods=["POST"])
def api_search():
    """Handles POST requests for text, image, hybrid, or semantic
    searches and returns matching results as JSON.
    """
    try:
        data = request.get_json()
        query = data.get("query", "")
        stype = data.get("type", "text")
        filters = data.get("filters", {})
        limit = data.get("limit", 20)
        if not query:
            return jsonify({"error": "Query is required"}), 400
        fn = {
            "text": lambda: search_engine.text_to_image_search(query, filters, limit),
            "image": lambda: search_engine.image_to_image_search(query, filters, limit),
            "hybrid": lambda: search_engine.hybrid_search(query=query, filters=filters, limit=limit),
            "semantic": lambda: search_engine.semantic_search(query, filters, limit),
        }.get(stype)
        if fn is None:
            return jsonify({"error": "Invalid search type"}), 400
        results = fn()
        return jsonify({"results": results, "total_count": len(results), "query": query, "type": stype})
    except Exception as e:
        logger.error(f"API search failed: {e}")
        return jsonify({"error": str(e)}), 500


@api_bp.route("/api/upload", methods=["POST"])
def api_upload():
    """Accepts a file upload via POST, validates its type,
    saves it to the uploads folder, and returns the file URL.
    """
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file provided"}), 400
        file = request.files["file"]
        if file.filename == "":
            return jsonify({"error": "No file selected"}), 400
        from flask import current_app
        from config.settings import IMAGE_CONFIG
        allowed = {ext.lstrip(".") for ext in IMAGE_CONFIG["supported_formats"]}
        if "." not in file.filename or file.filename.rsplit(".", 1)[1].lower() not in allowed:
            return jsonify({"error": "Invalid file type"}), 400
        filename = f"{uuid.uuid4()}_{secure_filename(file.filename)}"
        filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)
        return jsonify({"filename": filename, "path": filepath, "url": f"/static/uploads/{filename}"})
    except Exception as e:
        logger.error(f"Upload failed: {e}")
        return jsonify({"error": str(e)}), 500


@api_bp.route("/api/similar", methods=["POST"])
def api_similar():
    """Finds and returns images visually similar to the one
    identified by the provided image path.
    """
    try:
        data = request.get_json()
        image_path = data.get("image_path", "")
        if not image_path:
            return jsonify({"error": "Image path is required"}), 400
        results = search_engine.image_to_image_search(image_path, limit=data.get("limit", 10))
        return jsonify({"results": results, "total_count": len(results), "reference_image": image_path})
    except Exception as e:
        logger.error(f"Similar images search failed: {e}")
        return jsonify({"error": str(e)}), 500


@api_bp.route("/api/recommendations", methods=["POST"])
def api_recommendations():
    """Generates product recommendations based on the given
    reference image and returns them as JSON.
    """
    try:
        data = request.get_json()
        image_path = data.get("image_path", "")
        if not image_path:
            return jsonify({"error": "Image path is required"}), 400
        results = search_engine.get_recommendations(image_path, limit=data.get("limit", 10))
        return jsonify({"results": results, "total_count": len(results), "reference_image": image_path})
    except Exception as e:
        logger.error(f"Recommendations failed: {e}")
        return jsonify({"error": str(e)}), 500


@api_bp.route("/api/natural", methods=["POST"])
def api_natural():
    """Processes a natural language query, extracts intent and filters,
    and routes to the appropriate search method.
    """
    try:
        data = request.get_json()
        query = data.get("query", "")
        if not query:
            return jsonify({"error": "Query is required"}), 400
        intent = query_processor.process_query(query)
        terms = " ".join(intent.search_terms)
        if intent.query_type == "text":
            results = search_engine.text_to_image_search(terms, intent.filters, intent.limit)
        elif intent.query_type == "image" and intent.image_path:
            results = search_engine.image_to_image_search(intent.image_path, intent.filters, intent.limit)
        elif intent.query_type == "metadata":
            results = search_engine.metadata_search(intent.filters, intent.limit)
        else:
            results = search_engine.hybrid_search(terms, intent.image_path, intent.filters, intent.limit)
        return jsonify({
            "results": results, "total_count": len(results),
            "intent": {"type": intent.query_type, "search_terms": intent.search_terms,
                       "filters": intent.filters, "image_path": intent.image_path},
            "original_query": query,
        })
    except Exception as e:
        logger.error(f"Natural language search failed: {e}")
        return jsonify({"error": str(e)}), 500


@api_bp.route("/api/stats")
def api_stats():
    """Returns the current search engine statistics as JSON."""
    try:
        return jsonify(search_engine.get_search_stats())
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_bp.route("/api/categories")
def api_categories():
    """Returns the available metadata categories (brands, patterns, etc.) as JSON."""
    from config.settings import METADATA_CATEGORIES
    return jsonify(METADATA_CATEGORIES)
