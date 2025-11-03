# scripts/load_pdf_to_db.py
import os, glob
from PyPDF2 import PdfReader
from datetime import datetime
from app.database import SessionLocal
from app.models.pdf_data import PDFData

def extract_pdf_text(path: str) -> tuple[str, int]:
    """PDF 파일에서 텍스트와 페이지 수 추출"""
    try:
        reader = PdfReader(path)
        text = ""
        for page in reader.pages:
            text += (page.extract_text() or "") + "\n"
        return text.strip(), len(reader.pages)
    except Exception as e:
        print(f"❌ PDF 읽기 실패 ({path}): {e}")
        return "", 0

def load_pdfs_to_db():
    db = SessionLocal()
    folder = "data/pdfs"
    os.makedirs(folder, exist_ok=True)

    pdf_files = glob.glob(os.path.join(folder, "*.pdf"))
    if not pdf_files:
        print("⚠️ data/pdfs 폴더에 PDF 파일이 없습니다.")
        return

    for pdf_path in pdf_files:
        file_name = os.path.basename(pdf_path)
        text, page_count = extract_pdf_text(pdf_path)
        if not text:
            print(f"⚠️ {file_name}: 내용이 비어있어 건너뜀")
            continue

        # DB에 저장
        pdf_record = PDFData(
            file_name=file_name,
            page_count=page_count,
            text_content=text,
            created_at=datetime.utcnow()
        )
        db.add(pdf_record)
        db.commit()
        print(f"✅ {file_name} → DB 저장 완료 ({page_count}쪽)")

    db.close()
    print("🏁 모든 PDF 파일 저장 완료")

if __name__ == "__main__":
    load_pdfs_to_db()
