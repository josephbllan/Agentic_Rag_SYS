from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from config.db_base import Base, _utcnow


class SystemMetrics(Base):
    __tablename__ = "system_metrics"

    id = Column(Integer, primary_key=True, index=True)
    metric_name = Column(String(100), index=True)
    metric_value = Column(Float)
    metric_unit = Column(String(20))

    context = Column(JSON)

    recorded_at = Column(DateTime, default=_utcnow)

    def __repr__(self):
        """Returns a string representation of the SystemMetrics instance.
        Displays the metric name and its recorded value.
        """
        return f"<SystemMetrics(id={self.id}, name='{self.metric_name}', value={self.metric_value})>"
