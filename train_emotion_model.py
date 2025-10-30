#train_emotion_model.py

from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
import torch

model_name = "monologg/koelectra-base-v3-discriminator"  # or klue/bert-base
tokenizer = AutoTokenizer.from_pretrained(model_name)

# ✅ 데이터셋 로드
dataset = load_dataset("csv", data_files={"train": "data/train.csv", "test": "data/test.csv"})

# ✅ 토크나이징
def tokenize(batch):
    return tokenizer(batch["text"], truncation=True, padding="max_length", max_length=128)
dataset = dataset.map(tokenize, batched=True)

# ✅ 라벨 매핑
labels = {"positive": 0, "negative": 1, "neutral": 2}
def encode_labels(example):
    example["labels"] = labels[example["label"]]
    return example
dataset = dataset.map(encode_labels)

# ✅ 모델 정의
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=3)

# ✅ 학습 설정
training_args = TrainingArguments(
    output_dir="models/emotion_classifier",
    evaluation_strategy="epoch",
    num_train_epochs=3,
    per_device_train_batch_size=8,
    save_strategy="epoch",
    load_best_model_at_end=True,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset["train"],
    eval_dataset=dataset["test"],
    tokenizer=tokenizer,
)

trainer.train()
model.save_pretrained("models/emotion_classifier")
tokenizer.save_pretrained("models/emotion_classifier")
print("✅ 모델 학습 및 저장 완료")
