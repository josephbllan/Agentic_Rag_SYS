"""Database - re-exports for backward compatibility."""
from sqlalchemy import text
from config.db_base import engine, SessionLocal, Base, _utcnow, get_db, get_db_session
from config.db_shoe_image import ShoeImage
from config.db_search_query import SearchQuery
from config.db_search_result import SearchResult
from config.db_user_session import UserSession
from config.db_system_metrics import SystemMetrics

__all__ = [
    "engine", "SessionLocal", "Base", "get_db", "get_db_session",
    "ShoeImage", "SearchQuery", "SearchResult", "UserSession", "SystemMetrics",
]


def create_tables():
    Base.metadata.create_all(bind=engine)


def drop_tables():
    Base.metadata.drop_all(bind=engine)


def reset_database():
    drop_tables()
    create_tables()


def test_connection():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False


if __name__ == "__main__":
    create_tables()
    print("Database tables created successfully!")
