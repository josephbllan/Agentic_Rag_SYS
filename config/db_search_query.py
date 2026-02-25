from sqlalchemy import Column, Integer, String, Float, DateTime, Text, JSON
from config.db_base import Base, _utcnow


class SearchQuery(Base):
    __tablename__ = "search_queries"

    id = Column(Integer, primary_key=True, index=True)
    query_text = Column(Text)
    query_type = Column(String(50))
    filters = Column(JSON)
    results_count = Column(Integer)
    execution_time = Column(Float)

    session_id = Column(String(100))
    user_id = Column(String(100))
    ip_address = Column(String(45))

    created_at = Column(DateTime, default=_utcnow)

    def __repr__(self):
        return f"<SearchQuery(id={self.id}, query='{self.query_text[:50]}...', type='{self.query_type}')>"
