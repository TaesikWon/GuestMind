# analyze_training_results.py
import os
import json
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def analyze_logs(log_dir="logs"):
    log_file = None
    for root, _, files in os.walk(log_dir):
        for file in files:
            if file.endswith(".json"):
                log_file = os.path.join(root, file)
                break
    if not log_file:
        print("⚠️ 로그 파일을 찾을 수 없습니다.")
        return

    print(f"📄 로그 파일 로드 중: {log_file}")
    logs = []
    with open(log_file, "r", encoding="utf-8") as f:
        for line in f:
            try:
                logs.append(json.loads(line.strip()))
            except:
                continue

    df = pd.DataFrame(logs)
    if "eval_loss" not in df.columns:
        print("⚠️ 평가 기록이 포함된 로그가 없습니다.")
        return

    # ✅ F1, Accuracy 시각화
    plt.figure(figsize=(8, 5))
    sns.lineplot(x=df["epoch"], y=df["eval_f1"], label="F1-score", marker="o")
    sns.lineplot(x=df["epoch"], y=df["eval_accuracy"], label="Accuracy", marker="s")
    plt.title("📈 Model Performance per Epoch")
    plt.xlabel("Epoch")
    plt.ylabel("Score")
    plt.legend()
    plt.tight_layout()
    plt.savefig("models/training_metrics.png", dpi=300, bbox_inches="tight")
    plt.show()
    print("✅ 학습 성능 그래프 저장 완료: models/training_metrics.png")

    best_epoch = df.loc[df["eval_f1"].idxmax(), "epoch"]
    best_f1 = df["eval_f1"].max()
    best_acc = df.loc[df["eval_f1"].idxmax(), "eval_accuracy"]
    print(f"\n🏆 Best Epoch: {best_epoch}")
    print(f"⭐ F1-score: {best_f1:.4f}")
    print(f"⭐ Accuracy: {best_acc:.4f}")

def check_confusion_matrix():
    cm_path = "models/confusion_matrix.png"
    if os.path.exists(cm_path):
        print(f"\n🖼️ 혼동 행렬 이미지 확인 완료: {cm_path}")
    else:
        print("\n⚠️ 혼동 행렬 이미지가 없습니다. 모델 학습을 먼저 실행하세요.")

if __name__ == "__main__":
    print("🔍 감정 분석 모델 학습 결과 자동 분석 리포트")
    analyze_logs("logs")
    check_confusion_matrix()
    print("\n✅ 분석 완료!")
