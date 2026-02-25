# Multi-Modal Image Search System
###### By Joseph Ballan | ballan.joseph@gmail.com

RAG system for multi-modal image search using CLIP, ResNet, Sentence Transformers, FAISS, and ChromaDB.

## Features

- **Search modes**: text-to-image, image-to-image, hybrid, semantic, metadata
- **Embeddings**: CLIP (ViT-B/32, ViT-L/14), ResNet50/101, Sentence Transformers
- **Vector stores**: FAISS and ChromaDB with unified API
- **REST API**: FastAPI with JWT auth, RBAC, rate limiting, versioned endpoints
- **Web UI**: Flask interface for search, upload, analytics, browsing
- **Patterns**: Factory, Strategy, Observer, Adapter, Singleton

## Architecture

```
Presentation (FastAPI, Flask)
    |
Application (services)
    |
Domain (models, enums, interfaces, value objects)
    |
Core (embeddings, search engine, vector DB, query processor)
    |
Infrastructure (design patterns, adapters)
```

## Setup

```bash
git clone <repository-url>
cd rag
pip install -r requirements.txt
```

Set environment variables (optional):

```bash
export JWT_SECRET_KEY=your-secret
export CUDA_AVAILABLE=true
```

## Usage

### Index images

```bash
python main.py --mode index --image-dir /path/to/images
```

### Start servers

```bash
python main.py --mode serve
```

- Web UI: http://localhost:5000
- API: http://localhost:8000
- Docs: http://localhost:8000/docs

### CLI search

```bash
python main.py --mode search --query "red nike sneakers" --search-type text
python main.py --mode search --query /path/to/image.jpg --search-type image
```

### API examples

```bash
# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -d "username=admin&password=secret"

# Text search (with token)
curl -X POST http://localhost:8000/api/v1/search/text \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"query": "red nike sneakers", "limit": 10}'
```

### Python API

```python
from rag_system import RAGSystem

rag = RAGSystem(vector_backend="faiss")
rag.index_images("/path/to/images")
results = rag.search("red nike sneakers", search_type="text", limit=10)
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | /api/v1/auth/login | Get JWT token |
| GET | /api/v1/auth/me | Current user info |
| POST | /api/v1/auth/logout | Revoke token |
| POST | /api/v1/search/text | Text search |
| POST | /api/v1/search/image | Image search |
| POST | /api/v1/search/hybrid | Hybrid search |
| GET | /api/v1/system/health | Health check |
| GET | /api/v1/system/status | System status |
| POST | /api/v1/system/rebuild | Rebuild index (admin) |
| GET | /api/v1/export/results | Export results |
| POST | /api/v1/upload/upload | Upload image |

Demo credentials: `admin` / `secret` (admin+user roles), `demo` / `secret` (user role).

## Configuration

Key settings in `config/settings.py`:

- **Vector DB**: index type, dimension, distance metric
- **Models**: CLIP model name, device, batch size
- **Search**: max results, similarity threshold, hybrid weights
- **JWT**: secret key, algorithm, token expiry

## Testing

```bash
pip install -r requirements-dev.txt
python -m pytest tests/ -v
```

59 tests covering query processing, search engine, vector DB, JWT auth, and API endpoints.

## Docker

```bash
docker build -t rag-system .
docker run -p 8000:8000 rag-system
```

## License

MIT
