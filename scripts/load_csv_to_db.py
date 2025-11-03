# scripts/load_csv_to_db.py
import os, glob, pandas as pd
from app.database import SessionLocal
from app.models.hotel_data import HotelData
from datetime import datetime

def load_csv_to_db():
    db = SessionLocal()
    folder = "data/hotel"

    for file in glob.glob(os.path.join(folder, "*.csv")):
        df = pd.read_csv(file)
        file_name = os.path.basename(file)
        print(f"📂 {file_name} 불러옴 ({len(df)}행)")

        # 행별로 DB에 삽입
        for idx, row in df.iterrows():
            for col in df.columns:
                value = str(row[col]) if not pd.isna(row[col]) else None
                data = HotelData(
                    file_name=file_name,
                    column_name=col,
                    value=value,
                    created_at=datetime.utcnow()
                )
                db.add(data)

        db.commit()
        print(f"✅ {file_name} → DB 저장 완료")

    db.close()
    print("🏁 모든 CSV 파일 저장 완료")

if __name__ == "__main__":
    load_csv_to_db()
