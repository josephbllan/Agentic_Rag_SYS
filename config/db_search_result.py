from sqlalchemy import Column, Integer, Float, DateTime
from config.db_base import Base, _utcnow


class SearchResult(Base):
    __tablename__ = "search_results"

    id = Column(Integer, primary_key=True, index=True)
    query_id = Column(Integer, index=True)
    image_id = Column(Integer, index=True)
    similarity_score = Column(Float)
    rank = Column(Integer)

    clicked = Column(Integer, default=0)
    download_count = Column(Integer, default=0)

    created_at = Column(DateTime, default=_utcnow)

    def __repr__(self):
        """Returns a string representation of the SearchResult instance.
        Displays the query ID, image ID, and similarity score.
        """
        return f"<SearchResult(id={self.id}, query_id={self.query_id}, image_id={self.image_id}, score={self.similarity_score})>"
