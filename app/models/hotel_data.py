# app/models/hotel_data.py
from sqlalchemy import Column, Integer, String, Float, DateTime
from app.database import Base
from datetime import datetime

class HotelData(Base):
    __tablename__ = "hotel_data"

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String, nullable=False)      # 어떤 파일에서 왔는지
    column_name = Column(String, nullable=False)    # 컬럼명
    value = Column(String, nullable=True)           # 값
    created_at = Column(DateTime, default=datetime.utcnow)
