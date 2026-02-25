from sqlalchemy import Column, Integer, String, Float, DateTime, Text, JSON
from config.db_base import Base, _utcnow


class ShoeImage(Base):
    __tablename__ = "shoe_images"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), unique=True, index=True)
    original_path = Column(String(500))
    product_url = Column(String(1000))
    product_title = Column(Text)
    image_url = Column(String(1000))

    pattern = Column(String(50), index=True)
    shape = Column(String(50), index=True)
    size = Column(String(50), index=True)
    brand = Column(String(50), index=True)

    color = Column(String(50))
    style = Column(String(100))
    material = Column(String(100))
    price = Column(Float)

    image_width = Column(Integer)
    image_height = Column(Integer)
    file_size = Column(Integer)
    format = Column(String(10))

    clip_embedding = Column(JSON)
    resnet_features = Column(JSON)
    text_embedding = Column(JSON)

    created_at = Column(DateTime, default=_utcnow)
    updated_at = Column(DateTime, default=_utcnow, onupdate=_utcnow)
    indexed_at = Column(DateTime)

    search_count = Column(Integer, default=0)
    last_searched = Column(DateTime)

    def __repr__(self):
        return f"<ShoeImage(id={self.id}, filename='{self.filename}', brand='{self.brand}')>"
