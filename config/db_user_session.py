from sqlalchemy import Column, Integer, String, DateTime, Text
from config.db_base import Base, _utcnow


class UserSession(Base):
    __tablename__ = "user_sessions"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(100), unique=True, index=True)
    user_id = Column(String(100))
    ip_address = Column(String(45))
    user_agent = Column(Text)

    total_searches = Column(Integer, default=0)
    total_clicks = Column(Integer, default=0)
    total_downloads = Column(Integer, default=0)

    created_at = Column(DateTime, default=_utcnow)
    last_activity = Column(DateTime, default=_utcnow)
    ended_at = Column(DateTime)

    def __repr__(self):
        """Returns a string representation of the UserSession instance.
        Displays the session ID and total search count.
        """
        return f"<UserSession(id={self.id}, session_id='{self.session_id}', searches={self.total_searches})>"
