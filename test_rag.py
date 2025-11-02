# test_rag.py
import shutil
import os

def clear_index():
    """기존 Chroma 인덱스 폴더를 완전히 삭제"""
    index_path = "app/services/embeddings"
    if os.path.exists(index_path):
        shutil.rmtree(index_path)
        print(f"🧹 기존 인덱스 삭제 완료: {index_path}")
    else:
        print("ℹ️ 기존 인덱스가 없습니다. 새로 생성합니다.")

def main():
    print("🧩 SoulStay RAG 테스트 시작...")

    # 0️⃣ 인덱스 초기화
    clear_index()

    # 1️⃣ RAG 서비스 초기화 (CSV 로드)
    from app.services.rag_service import RAGService
    
    rag = RAGService()
    
    # 2️⃣ CSV 파일에서 피드백 데이터 로드
    csv_path = "data/feedback_samples.csv"
    print(f"\n📂 CSV 파일 로드 중: {csv_path}")
    rag.load_feedback_csv(csv_path)

    # 3️⃣ 검색 테스트
    query = "객실이 너무 더러웠어요"
    print(f"\n🔍 검색 문장: {query}")
    results = rag.search_similar_feedback(query, top_k=3)

    print("\n📘 검색 결과:")
    for i, r in enumerate(results, start=1):
        print(f"{i}. {r['text']} (score={r['score']:.4f})")

    print("\n✅ 테스트 완료!")

if __name__ == "__main__":
    main()