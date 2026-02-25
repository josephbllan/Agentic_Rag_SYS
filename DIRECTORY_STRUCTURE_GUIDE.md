# Directory Structure Guide
###### By Joseph Ballan | ballan.joseph@gmail.com

## Layers

```
Presentation    api/, web/          HTTP endpoints, middleware, security
Application     services/           Use-case orchestration
Domain          domain/             Models, enums, interfaces, value objects, ABCs
Core            core/               Embeddings, search engine, vector DB, query processor
Infrastructure  patterns/           Factory, Strategy, Observer, Adapter, Singleton
Configuration   config/             Settings, database models, env
```

## Directory Tree

```
api/
  controllers/          MVC controllers (base, health, search)
  middleware/           Logging, error handling, rate limiting, request ID
  routes/v1/           Versioned endpoints (auth, search, system, export, upload)
  schemas/             Pydantic request/response models (1 class per file)
  security/            JWT handler, password handler, token blacklist
config/
  settings.py          All configuration (models, DB, search, API, JWT)
  database.py          Re-exporter for ORM models and session utilities
  db_base.py           SQLAlchemy engine, Base, session factories
  db_*.py              One ORM model per file (ShoeImage, SearchQuery, etc.)
core/
  image_embedder.py    CLIP/ResNet image embeddings
  text_embedder.py     Sentence Transformer text embeddings
  multimodal_embedder.py  Combined image+text embedder
  embedding_manager.py Caching and batch processing
  embeddings.py        Re-exporter for all embedding classes
  query_processor.py   Natural language query parsing
  query_data.py        Query constants, QueryIntent dataclass, helpers
  search_engine.py     Multi-modal search orchestration
  search_analytics.py  Search logging and statistics
  vector_db.py         Re-exporter and factory for vector backends
  vector_db_base.py    Abstract BaseVectorDB + shared filter logic
  faiss_db.py          FAISS backend implementation
  chroma_db.py         ChromaDB backend implementation
  utils.py             Stable text hashing
domain/
  types.py             Type aliases, guards, constants
  enums/               One enum per file (QueryType, BrandType, etc.)
  models/              One Pydantic model per file (ImageMetadata, SearchQuery, etc.)
  value_objects/       One frozen dataclass per file (QueryIntent, SearchScore, etc.)
  interfaces/          One Protocol per file (IEmbeddingModel, IVectorDatabase, etc.)
  base_classes/        One ABC per file (BaseEmbeddingModel, BaseSearchStrategy, etc.)
patterns/
  strategy/            SearchContext + 5 strategy implementations
  factory/             AbstractFactory + 6 concrete factories
  observer/            Observer, Subject, EventPublisher + 4 event observers
  singleton/           SingletonMeta, Singleton + 4 manager singletons
  adapter/             VectorDatabaseAdapter, FAISSAdapter, ChromaDBAdapter
services/
  base_service.py      Service lifecycle scaffold
  indexing_service.py   Image indexing workflow
web/
  app.py               Flask web interface
  api_routes.py        Flask API blueprint
  templates/           HTML templates
tests/
  conftest.py          Shared fixtures and mocks
  test_*.py            59 tests across 6 test modules
main.py                CLI entry point
rag_system.py          RAGSystem class
```

## Key Design Decisions

- **One class per file**: every Python class lives in its own module.
- **Package re-exporters**: original module names (e.g. `domain/models`, `patterns/strategy`) are preserved as packages whose `__init__.py` re-exports all symbols, so existing imports stay valid.
- **Absolute imports**: `core/` and `patterns/` use absolute imports (`from domain.models import X`). `domain/` sub-packages use relative imports (`from ..enums import X`).
- **Dependency direction**: Presentation -> Application -> Domain <- Core. Infrastructure is consumed via Domain abstractions.

## Patterns Reference

| Pattern | Location | Purpose |
|---------|----------|---------|
| Factory | patterns/factory/ | Create models, DBs, strategies, services |
| Strategy | patterns/strategy/ | Interchangeable search algorithms |
| Observer | patterns/observer/ | Event-driven hooks for search, indexing, cache |
| Adapter | patterns/adapter/ | Normalize vector DB access |
| Singleton | patterns/singleton/ | Config, logging, cache, connection pools |
