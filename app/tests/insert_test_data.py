# app/tests/insert_test_data.py
from app.database import SessionLocal
from app.models.emotion_log import EmotionLog
from app.models.user import User

def insert_test_data():
    db = SessionLocal()
    try:
        # (1) 테스트 사용자 생성
        user = db.query(User).filter_by(username="test_user").first()
        if not user:
            user = User(username="test_user", password_hash="hashed_pw")
            db.add(user)
            db.commit()
            db.refresh(user)
            print(f"✅ 테스트 사용자 생성 완료 (id={user.id})")

        # (2) 감정 로그 데이터 추가
        samples = [
            ("호텔 객실이 매우 깨끗하고 조용했어요.", "긍정", "청결함과 조용함"),
            ("직원들이 불친절했어요.", "부정", "서비스 불만"),
            ("위치는 좋지만 방이 좁아요.", "중립", "공간이 아쉬움"),
        ]

        for text, emotion, reason in samples:
            log = EmotionLog(
                user_id=user.id,
                text=text,
                emotion=emotion,
                reason=reason
            )
            db.add(log)

        db.commit()
        print("✅ 테스트 데이터 삽입 완료")

    except Exception as e:
        db.rollback()
        print(f"❌ 오류 발생: {e}")

    finally:
        db.close()

if __name__ == "__main__":
    insert_test_data()

# app/tests/insert_test_data.py
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from app import models  # ✅ 모든 모델 로드
from app.database import SessionLocal
from app.models.emotion_log import EmotionLog
from app.models.user import User
