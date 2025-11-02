# tests/test_rag.py
import shutil
import os
import sys

# 프로젝트 루트를 sys.path에 추가
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def clear_index():
    """기존 Chroma 인덱스 폴더를 완전히 삭제"""
    index_path = "app/services/embeddings"
    if os.path.exists(index_path):
        shutil.rmtree(index_path)
        print(f"🧹 기존 인덱스 삭제 완료: {index_path}")
    else:
        print("ℹ️ 기존 인덱스가 없습니다. 새로 생성합니다.")

def main():
    print("🧩 SoulStay LangChain RAG 테스트 시작...")

    # 0️⃣ 인덱스 초기화
    clear_index()

    # 1️⃣ LangChain RAG 서비스 초기화
    from app.services.langchain_rag_service import LangChainRAGService
    
    rag = LangChainRAGService()
    
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

    # 4️⃣ 응답 생성 테스트
    print(f"\n💬 응답 생성 테스트:")
    response = rag.generate_response(query, "negative", results)
    print(f"답변: {response}")

    # 5️⃣ 상태 확인
    status = rag.get_rag_status()
    print(f"\n📊 총 저장된 피드백: {status['total_documents']}개")

    print("\n✅ 테스트 완료!")

if __name__ == "__main__":
    main()