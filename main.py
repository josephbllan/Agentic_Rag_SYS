"""Main entry point -- CLI for the RAG System."""
import sys
import logging
import argparse
import json
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from config.settings import LOGGING_CONFIG

logging.basicConfig(
    level=getattr(logging, LOGGING_CONFIG["level"]),
    format=LOGGING_CONFIG["format"],
    handlers=[logging.FileHandler(LOGGING_CONFIG["file"]), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


def main():
    """Parses CLI arguments and dispatches the requested mode
    (index, search, stats, or serve) for the RAG system.
    """
    parser = argparse.ArgumentParser(description="RAG System for Shoe Image Search")
    parser.add_argument("--mode", choices=["index", "search", "serve", "stats"], default="serve")
    parser.add_argument("--query", type=str)
    parser.add_argument("--search-type", choices=["text", "image", "hybrid", "semantic", "natural"], default="text")
    parser.add_argument("--image-dir", type=str)
    parser.add_argument("--vector-backend", choices=["faiss", "chroma"], default="faiss")
    parser.add_argument("--limit", type=int, default=10)
    args = parser.parse_args()

    try:
        from rag_system import RAGSystem
        rag = RAGSystem(vector_backend=args.vector_backend)

        if args.mode == "index":
            print(json.dumps(rag.index_images(args.image_dir), indent=2))

        elif args.mode == "search":
            if not args.query:
                print("Error: Query is required for search mode")
                return 1
            results = rag.search(args.query, args.search_type, limit=args.limit)
            print(f"Found {len(results)} results:")
            for i, r in enumerate(results[:5]):
                print(f"  {i+1}. {r.get('filename', '?')} (Score: {r.get('similarity_score', 0):.3f})")

        elif args.mode == "stats":
            print(json.dumps(rag.get_stats(), indent=2))

        elif args.mode == "serve":
            print("Starting RAG System...")
            print("Web interface: http://localhost:5000")
            print("REST API:     http://localhost:8000/api/docs")
            import threading

            def start_web():
                """Starts the Flask web interface on localhost port 5000."""
                from web.app import app
                app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)

            def start_api():
                """Starts the FastAPI REST API server on port 8000 via uvicorn."""
                import uvicorn
                from api.main import app as api_app
                uvicorn.run(api_app, host="0.0.0.0", port=8000, log_level="info")

            web_t = threading.Thread(target=start_web, daemon=True)
            api_t = threading.Thread(target=start_api, daemon=True)
            web_t.start()
            api_t.start()
            print("Both servers started. Press Ctrl+C to stop.")
            try:
                web_t.join()
            except KeyboardInterrupt:
                print("\nShutting down...")

    except Exception as e:
        logger.error(f"RAG System failed: {e}")
        print(f"Error: {e}")
        return 1
    return 0


if __name__ == "__main__":
    exit(main())
