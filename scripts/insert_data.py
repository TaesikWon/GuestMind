# scripts/insert_test_data.py
from app.database import SessionLocal
from app.models.emotion_log import EmotionLog
from app.models.user import User
from datetime import datetime

db = SessionLocal()
user = db.query(User).filter_by(username="test_user").first()

sample_logs = [
    ("조식이 식어서 맛이 없었어요.", "부정", "서비스 불만"),
    ("룸서비스가 빠르고 친절했어요.", "긍정", "응대 만족"),
]

for text, emotion, reason in sample_logs:
    log = EmotionLog(user_id=user.id, text=text, emotion=emotion, reason=reason, created_at=datetime.now())
    db.add(log)

db.commit()
db.close()
