# -*- coding: utf-8 -*-
import os
from app.services import rag_service

def test_rag_workflow():
    print("[SoulStay] RAG 기능 테스트 시작\n")

    # 테스트용 피드백 데이터
    feedback_samples = [
        (1, "호텔 객실이 매우 깨끗하고 조용했어요."),
        (2, "직원들이 친절하지 않았고, 체크인 대기시간이 너무 길었어요."),
        (3, "아침 식사가 정말 맛있었어요! 다시 방문하고 싶습니다."),
        (4, "위치는 좋았지만 방 냄새가 조금 났어요."),
        (5, "서비스가 전반적으로 훌륭하고 기분이 좋았습니다.")
    ]

    # DB에 피드백 추가
    print("피드백을 ChromaDB에 저장 중...\n")
    for fid, text in feedback_samples:
        success = rag_service.add_feedback_to_rag(fid, text)
        if success:
            print(f"({fid}) 저장 완료: {text}")
        else:
            print(f"({fid}) 저장 실패: {text}")

    # 유사 피드백 검색 테스트
    print("\n유사 피드백 검색 테스트")
    query = "직원 서비스가 너무 불친절했어요."
    results = rag_service.search_similar_feedback(query_text=query, top_k=3)

    print(f"\n검색 문장: {query}\n")
    if results:
        print("유사 피드백 결과:")
        for i, r in enumerate(results, start=1):
            print(f"{i}. {r['text']}  (유사도 거리: {r['distance']:.3f})")
    else:
        print("유사한 피드백을 찾지 못했습니다.")

    print("\n테스트 완료!")

    # ChromaDB 폴더 확인
    db_path = "app/chroma_db"
    if os.path.exists(db_path):
        print(f"\nChromaDB 폴더 확인됨 → {os.path.abspath(db_path)}")
    else:
        print("\nChromaDB 폴더가 생성되지 않았습니다. 경로를 다시 확인하세요.")


if __name__ == "__main__":
    test_rag_workflow()
