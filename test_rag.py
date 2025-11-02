# test_rag.py
import shutil
import os
from app.services.rag_service import RAGService

def clear_index():
    """기존 Chroma 인덱스 폴더를 완전히 삭제"""
    index_path = os.path.join("app", "services", "embeddings", "soulstay_index")
    if os.path.exists(index_path):
        shutil.rmtree(index_path)
        print(f"🧹 기존 인덱스 삭제 완료: {index_path}")
    else:
        print("ℹ️ 기존 인덱스가 없습니다. 새로 생성합니다.")

def main():
    print("🧩 SoulStay RAG 테스트 시작...")

    # 0️⃣ 인덱스 초기화
    clear_index()

    # 1️⃣ RAG 서비스 초기화
    rag = RAGService()

    # 2️⃣ 테스트 문서 추가
    docs = [
        "호텔이 정말 깨끗하고 조용했어요.",
        "직원들이 친절해서 기분이 좋았습니다.",
        "방이 너무 더럽고 냄새가 났어요.",
        "체크인 과정이 너무 느렸습니다.",
        "침대가 편안하고 조식이 맛있었어요."
    ]
    result = rag.add_documents(docs)
    print(result)

    # 3️⃣ 검색 테스트
    query = "객실이 너무 더러웠어요"
    print(f"\n🔍 검색 문장: {query}")
    results = rag.search(query, emotion="negative", top_k=2)

    print("\n📘 검색 결과:")
    for i, r in enumerate(results, start=1):
        print(f"{i}. {r['text']}  (emotion={r['emotion']})")

    print("\n✅ 테스트 완료!")

if __name__ == "__main__":
    main()
