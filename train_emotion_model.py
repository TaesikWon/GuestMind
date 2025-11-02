# train_emotion_model.py

from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix, classification_report
import matplotlib.pyplot as plt
import seaborn as sns
import torch
import os

# ✅ 1. 모델 및 토크나이저 불러오기
model_name = "monologg/koelectra-base-v3-discriminator"
tokenizer = AutoTokenizer.from_pretrained(model_name)

# ✅ 2. 데이터셋 로드
dataset = load_dataset("csv", data_files={"train": "data/train.csv", "test": "data/test.csv"})

# ✅ 3. 토크나이징
def tokenize(batch):
    return tokenizer(batch["text"], truncation=True, padding="max_length", max_length=128)
dataset = dataset.map(tokenize, batched=True)

# ✅ 4. 라벨 인코딩
labels = {"positive": 0, "negative": 1, "neutral": 2}
def encode_labels(example):
    example["labels"] = labels[example["label"]]
    return example
dataset = dataset.map(encode_labels)

# ✅ 5. 포맷 설정 (PyTorch 텐서로 변환)
dataset.set_format(type="torch", columns=["input_ids", "attention_mask", "labels"])

# ✅ 6. 모델 정의
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=3)

# ✅ 7. 평가 함수 정의
def compute_metrics(pred):
    preds = pred.predictions.argmax(-1)
    labels = pred.label_ids
    acc = accuracy_score(labels, preds)
    f1 = f1_score(labels, preds, average="weighted")
    return {"accuracy": acc, "f1": f1}

# ✅ 8. 학습 설정
training_args = TrainingArguments(
    output_dir="models/emotion_classifier",
    evaluation_strategy="epoch",
    save_strategy="epoch",
    num_train_epochs=3,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,  # 추가
    learning_rate=2e-5,  # 추가
    weight_decay=0.01,  # 추가
    warmup_steps=100,  # 추가
    load_best_model_at_end=True,
    metric_for_best_model="f1",  # 추가
    logging_dir="logs",
    logging_steps=50,  # 100 → 50 (더 자주 로깅)
    save_total_limit=2,  # 추가 (최근 2개 체크포인트만 저장)
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset["train"],
    eval_dataset=dataset["test"],
    tokenizer=tokenizer,
    compute_metrics=compute_metrics,
)

# ✅ 9. 학습 및 저장
print("🚀 모델 학습 시작...")
trainer.train()

# 저장 경로 생성
os.makedirs("models/emotion_classifier", exist_ok=True)
model.save_pretrained("models/emotion_classifier")
tokenizer.save_pretrained("models/emotion_classifier")
print("✅ 모델 학습 및 저장 완료")

# ✅ 10. 테스트 데이터 평가
print("\n📊 테스트 데이터 평가 중...")
predictions = trainer.predict(dataset["test"])
pred_labels = predictions.predictions.argmax(-1)
true_labels = predictions.label_ids

print("\n📈 Classification Report:")
print(classification_report(true_labels, pred_labels, target_names=list(labels.keys())))

# ✅ 11. 혼동행렬 시각화
cm = confusion_matrix(true_labels, pred_labels)
plt.figure(figsize=(8,6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=list(labels.keys()), yticklabels=list(labels.keys()))
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Emotion Classification Confusion Matrix")
plt.tight_layout()

# 저장 경로 생성
os.makedirs("models", exist_ok=True)
plt.savefig("models/confusion_matrix.png", dpi=300, bbox_inches='tight')
print("✅ Confusion Matrix 저장 완료: models/confusion_matrix.png")
plt.show()