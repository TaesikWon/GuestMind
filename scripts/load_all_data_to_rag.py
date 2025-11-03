# scripts/load_all_data_to_rag.py
import os, sys, glob, logging, pandas as pd, chardet
from PyPDF2 import PdfReader
from docx import Document  # ✅ DOCX 읽기용

# ✅ SoulStay 루트 경로 인식 (가장 중요)
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.services.rag_service import add_feedback_to_rag, get_rag_status

# ✅ 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
)
logger = logging.getLogger("soulstay.load_all")

# ✅ PDF 텍스트 추출
def extract_pdf_text(path: str) -> str:
    try:
        reader = PdfReader(path)
        text = "\n".join([page.extract_text() or "" for page in reader.pages])
        return text.strip()
    except Exception as e:
        logger.error(f"❌ PDF 읽기 실패 ({path}): {e}")
        return ""

# ✅ DOCX 텍스트 추출
def extract_docx_text(path: str) -> str:
    try:
        doc = Document(path)
        text = "\n".join([p.text for p in doc.paragraphs])
        text = text.strip()
        if not text:
            logger.warning(f"⚠️ DOCX 내용이 비어있음: {path}")
        return text
    except Exception as e:
        logger.error(f"❌ DOCX 읽기 실패 ({path}): {e}")
        return ""

# ✅ PDF + DOCX 로드
def load_docs():
    data_dir = os.path.join("data", "pdfs")
    os.makedirs(data_dir, exist_ok=True)
    files = glob.glob(os.path.join(data_dir, "*.pdf")) + glob.glob(os.path.join(data_dir, "*.docx"))
    if not files:
        logger.warning("⚠️ data/pdfs 폴더에 PDF/DOCX 파일이 없습니다.")
        return 0

    logger.info(f"📂 {len(files)}개의 PDF/DOCX 파일을 찾았습니다.")
    count = 0
    for path in files:
        ext = os.path.splitext(path)[1].lower()
        text = extract_pdf_text(path) if ext == ".pdf" else extract_docx_text(path)
        if not text:
            continue
        base_name = os.path.basename(path)
        add_feedback_to_rag(user_id=0, feedback_text=text)
        logger.info(f"✅ '{base_name}' 등록 완료")
        count += 1
    return count

# ✅ CSV 인코딩 감지
def read_csv_safely(csv_path):
    try:
        return pd.read_csv(csv_path, encoding="utf-8")
    except UnicodeDecodeError:
        try:
            return pd.read_csv(csv_path, encoding="cp949")
        except UnicodeDecodeError:
            with open(csv_path, "rb") as f:
                raw_data = f.read(50000)
                detected = chardet.detect(raw_data)
                enc = detected.get("encoding", "utf-8")
                logger.warning(f"⚠️ 인코딩 감지됨: {enc} ({os.path.basename(csv_path)})")
                return pd.read_csv(csv_path, encoding=enc)

# ✅ CSV 로드
def load_csvs():
    csv_dir = os.path.join("data", "hotel")
    os.makedirs(csv_dir, exist_ok=True)
    csv_files = glob.glob(os.path.join(csv_dir, "*.csv"))
    if not csv_files:
        logger.warning("⚠️ data/hotel 폴더에 CSV 파일이 없습니다.")
        return 0

    logger.info(f"📊 {len(csv_files)}개의 CSV 파일을 찾았습니다.")
    count = 0
    for csv_path in csv_files:
        try:
            df = read_csv_safely(csv_path)
            text = df.to_string(index=False)
            base_name = os.path.basename(csv_path)
            add_feedback_to_rag(user_id=0, feedback_text=text)
            logger.info(f"✅ '{base_name}' 등록 완료")
            count += 1
        except Exception as e:
            logger.error(f"❌ '{csv_path}' 처리 실패: {e}")
    return count

# ✅ 전체 실행
def main():
    logger.info("🚀 RAG 데이터 통합 등록 시작 (PDF + DOCX + CSV)")
    total_docs = load_docs()
    total_csvs = load_csvs()
    status = get_rag_status()
    logger.info(f"📦 총 {total_docs}개 문서(PDF/DOCX), {total_csvs}개 CSV 등록 완료")
    logger.info(f"📊 현재 RAG 문서 총 {status.get('total_documents', '?')}개")
    logger.info("🏁 모든 데이터 등록 완료!")

if __name__ == "__main__":
    main()
