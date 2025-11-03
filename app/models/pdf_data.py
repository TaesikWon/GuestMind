# app/models/pdf_data.py
from sqlalchemy import Column, Integer, String, Text, DateTime
from app.database import Base
from datetime import datetime

class PDFData(Base):
    __tablename__ = "pdf_data"

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String, nullable=False)
    page_count = Column(Integer, nullable=True)
    text_content = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
