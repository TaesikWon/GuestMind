# scripts/compare_rag_effect.py
import os, requests, json, time, shutil, sys

# ✅ 프로젝트 루트를 경로에 추가 (중요!)
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

API_URL = "http://127.0.0.1:8000/chat"
CHROMA_PATH = "data/chroma"

def ask_api(question):
    try:
        res = requests.post(API_URL, json={"message": question})
        if res.status_code == 200:
            return res.json().get("response", "").strip()
        return f"❌ 요청 실패: {res.status_code}"
    except Exception as e:
        return f"❌ 오류: {e}"

def clear_rag_data():
    """기존 Chroma 데이터 삭제"""
    if os.path.exists(CHROMA_PATH):
        for root, _, files in os.walk(CHROMA_PATH):
            for f in files:
                try:
                    os.remove(os.path.join(root, f))
                except Exception:
                    pass

def main():
    questions = [
        "호텔 고객이 조식에 불만을 남겼을 때 어떻게 응대해야 할까?",
        "룸서비스 이용 패턴을 개선하려면 무엇을 바꿔야 할까?",
        "직원 친절도 향상을 위한 교육 포인트를 알려줘."
    ]

    print("🚀 RAG 효과 비교 테스트 시작\n")

    # 1️⃣ RAG 없는 상태
    print("============================================================")
    print("🧠 1️⃣ RAG 비활성 상태 (문서 없이)")
    print("============================================================")
    clear_rag_data()
    for q in questions:
        print(f"\nQ: {q}")
        print("→", ask_api(q))
        time.sleep(2)

    # 2️⃣ RAG 데이터 로드 후
    print("\n============================================================")
    print("🔍 2️⃣ RAG 활성 상태 (문서+CSV 포함)")
    print("============================================================")
    os.system("python scripts/load_all_data_to_rag.py")

    for q in questions:
        print(f"\nQ: {q}")
        print("→", ask_api(q))
        time.sleep(2)

    print("\n✅ 테스트 완료!")

if __name__ == "__main__":
    main()
