# Changelog

Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Versioning: [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.2.0] - 2026-02-25

### Changed
- Split all multi-class files so each Python class resides in its own file.
- Converted domain/models, domain/enums, domain/value_objects, domain/interfaces, domain/base_classes into packages with per-class modules and __init__.py re-exporters.
- Converted patterns/strategy, factory, observer, singleton, adapter into packages.
- Extracted ORM models from config/database.py into config/db_*.py files.
- Moved API Pydantic schemas to api/schemas/ package.
- Split core/text_embedder.py into text_embedder.py and multimodal_embedder.py.
- All existing import paths preserved via re-exporting modules.

## [2.1.0] - 2026-02-25

### Added
- Split monolithic VectorDatabase into FAISSVectorDB + ChromaVectorDB behind abstract BaseVectorDB.
- SearchEngine accepts injected vector_db, embedding_manager, multimodal_embedder.
- Token blacklisting for logout. Rate limiting via slowapi. Request-ID middleware.
- /api/v1/ready readiness probe. X-Request-ID header on responses.
- 59-test suite covering QueryProcessor, SearchEngine, VectorDB, JWT auth, API endpoints.
- GitHub Actions CI workflow. Dockerfile for containerized deployment.
- Thread-safe DI singletons and token blacklist.

### Changed
- Error handler hides internal details when DEBUG=false.
- APP_VERSION centralized in config/settings.py.
- Replaced deprecated @app.on_event with lifespan context manager.
- Fixed passlib/bcrypt >= 4.1 compatibility.
- Fixed Pydantic user.dict() to user.model_dump().
- System routes use Depends(get_search_engine).

### Fixed
- api/security/__init__.py importing non-existent verify_token.
- Extracted stable_text_hash to core/utils.py to avoid heavy ML imports in tests.

## [2.0.0] - 2026-02-24

### Added
- MVC architecture with FastAPI + Flask dual server.
- JWT authentication with role-based access control.
- Multi-modal search (text, image, hybrid, semantic, natural language).
- CLIP, ResNet, Sentence Transformer embedding models.
- FAISS and ChromaDB vector database backends.
- Domain-driven design with interfaces, value objects, type system.
- Query sanitization against XSS/injection.

## [1.0.0] - Initial release

- Basic RAG system for shoe image search.
