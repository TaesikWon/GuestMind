# scripts/load_pdfs_to_rag.py
import os
import glob
import logging
from PyPDF2 import PdfReader

# ✅ FastAPI 앱의 모듈 경로 인식 (SoulStay 프로젝트 루트에서 실행될 때 필요)
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.services.rag_service import add_feedback_to_rag, get_rag_status

# ✅ 로거 설정
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
)
logger = logging.getLogger("soulstay.load_pdfs")


def extract_pdf_text(path: str) -> str:
    """PDF에서 텍스트 추출"""
    try:
        reader = PdfReader(path)
        text = ""
        for page in reader.pages:
            text += (page.extract_text() or "") + "\n"
        text = text.strip()
        if not text:
            logger.warning(f"⚠️ 텍스트가 비어있음: {path}")
        return text
    except Exception as e:
        logger.error(f"❌ PDF 읽기 실패 ({path}): {e}")
        return ""


def load_all_pdfs():
    """data/pdfs/ 폴더 내 모든 PDF를 RAG DB에 자동 등록"""
    pdf_dir = os.path.join("data", "pdfs")
    os.makedirs(pdf_dir, exist_ok=True)

    pdf_files = glob.glob(os.path.join(pdf_dir, "*.pdf"))
    if not pdf_files:
        logger.warning("⚠️ data/pdfs 폴더에 PDF 파일이 없습니다.")
        return

    logger.info(f"📂 {len(pdf_files)}개의 PDF 파일을 찾았습니다.")

    for pdf_path in pdf_files:
        text = extract_pdf_text(pdf_path)
        if not text:
            continue

        # 문서 이름 기반 중복 방지
        base_name = os.path.basename(pdf_path)
        user_id = 0  # 시스템 문서로 등록
        try:
            add_feedback_to_rag(user_id=user_id, feedback_text=text)
            logger.info(f"✅ '{base_name}' 등록 완료")
        except Exception as e:
            logger.error(f"❌ '{base_name}' 등록 실패: {e}")

    # 최종 상태 출력
    status = get_rag_status()
    logger.info(f"📊 현재 RAG 문서 총 {status.get('total_documents', '?')}개")


if __name__ == "__main__":
    logger.info("🚀 PDF → RAG 자동 등록 스크립트 시작")
    load_all_pdfs()
    logger.info("🏁 처리 완료!")
