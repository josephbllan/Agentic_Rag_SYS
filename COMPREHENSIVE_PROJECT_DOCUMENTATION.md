# Multi-Modal Image Search System - Technical Documentation
###### By Joseph Ballan | ballan.joseph@gmail.com

## Overview

RAG system for multi-modal image search. Combines CLIP/ResNet/Sentence Transformers for embeddings, FAISS/ChromaDB for vector storage, FastAPI for REST API, and Flask for web UI.

Stack: Python 3.12+, PyTorch, FastAPI, Flask, SQLAlchemy, Pydantic.

## Architecture

```
Presentation    FastAPI REST API + Flask web UI
Application     Indexing service, base service
Domain          Enums, models, interfaces, value objects, ABCs
Core            Embeddings, search engine, vector DB, query processor
Infrastructure  Design patterns (Factory, Strategy, Observer, Adapter, Singleton)
Configuration   Settings, SQLAlchemy models, env vars
```

Dependency direction: Presentation -> Application -> Domain <- Core. Infrastructure referenced via abstractions.

## Core Components

### Embeddings (core/)
- `ImageEmbedder`: CLIP or ResNet image embeddings
- `TextEmbedder`: Sentence Transformer text embeddings
- `MultiModalEmbedder`: unified multi-model interface
- `EmbeddingManager`: on-disk caching and batch processing

### Search Engine (core/search_engine.py)
- Text, image, hybrid, semantic, and metadata search
- Weighted hybrid scoring with configurable weights
- Query expansion for semantic search
- Analytics logging per query

### Vector Database (core/vector_db.py, faiss_db.py, chroma_db.py)
- Abstract `BaseVectorDB` with FAISS and ChromaDB implementations
- Add, search, delete, stats, rebuild operations
- Post-search metadata filtering

### Query Processor (core/query_processor.py)
- Natural language to structured `QueryIntent`
- Brand/pattern/shape/size/color extraction
- Synonym expansion, query validation

## API Layer (api/)

### Endpoints (v1)
- Auth: login, me, logout (JWT + OAuth2)
- Search: text, image, hybrid (rate-limited, authenticated)
- System: health, status, rebuild (admin-only)
- Export: results as JSON/CSV
- Upload: image upload

### Security
- JWT tokens with configurable expiry
- Token blacklisting for logout
- Role-based access (admin, user)
- Rate limiting (slowapi)
- Request-ID tracing

### MVC
- Controllers: BaseController, SearchController, HealthController
- Schemas: one Pydantic model per file in api/schemas/
- Middleware: logging, error handling, rate limiting, request ID

## Domain Layer (domain/)

- `types.py`: VectorType, type guards, constants
- `enums/`: QueryType, ModelName, VectorBackend, PatternType, BrandType, etc.
- `models/`: ImageMetadata, SearchQuery, SearchResultItem, SearchResponse, etc.
- `value_objects/`: QueryIntent, EmbeddingResult, SearchScore, CacheKey, etc.
- `interfaces/`: 14 Protocols (IEmbeddingModel, IVectorDatabase, ISearchStrategy, etc.)
- `base_classes/`: 7 ABCs (BaseEmbeddingModel, BaseVectorDatabase, BaseSearchStrategy, etc.)

## Design Patterns (patterns/)

| Pattern | Classes | Purpose |
|---------|---------|---------|
| Factory | ModelFactory, VectorDatabaseFactory, SearchStrategyFactory, ServiceFactory, etc. | Centralized creation |
| Strategy | TextSearchStrategy, ImageSearchStrategy, HybridSearchStrategy, etc. | Interchangeable algorithms |
| Observer | EventPublisher, SearchEventObserver, IndexingEventObserver, etc. | Event-driven hooks |
| Adapter | VectorDatabaseAdapter, FAISSAdapter, ChromaDBAdapter | Unified DB interface |
| Singleton | ConfigurationManager, LoggerManager, CacheManager, ConnectionPoolManager | Shared resources |

## Configuration (config/)

- `settings.py`: paths, vector DB config, model config, search config, API config, JWT config
- `database.py`: SQLAlchemy ORM models (ShoeImage, SearchQuery, SearchResult, UserSession, SystemMetrics)
- `.env.example`: environment variable templates

## Testing

59 tests in 6 modules:
- `test_query_processor.py`: query parsing, normalization, filter extraction
- `test_search_engine.py`: hybrid scoring, text/image search
- `test_vector_db.py`: filter application, vector operations
- `test_api_endpoints.py`: all API routes with mocked search engine
- `test_api_auth.py`: JWT creation, user lookup, authentication
- `test_embeddings.py`: stable hashing

All heavy ML modules mocked in tests for fast execution.

## CI/CD

- GitHub Actions: lint + test on Python 3.10/3.11, Docker build on main
- Dockerfile for containerized deployment
