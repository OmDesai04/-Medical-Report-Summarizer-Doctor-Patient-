import json
import os
from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, Seq2SeqTrainer, Seq2SeqTrainingArguments, DataCollatorForSeq2Seq

# Paths to the processed JSONL files
train_file = "data/train.jsonl"
# Prefer validation split if available; fallback to test
val_file = "data/validation.jsonl" if os.path.exists("data/validation.jsonl") else "data/test.jsonl"

# Load dataset
dataset = load_dataset("json", data_files={"train": train_file, "validation": val_file})

# Model and tokenizer
model_name = "google/flan-t5-small"   # You can upgrade to flan-t5-base or bart-large
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Tokenization
def preprocess_function(batch):
    inputs = tokenizer(batch["input"], max_length=512, truncation=True, padding="max_length")
    targets = tokenizer(batch["target"], max_length=128, truncation=True, padding="max_length")
    inputs["labels"] = targets["input_ids"]
    return inputs

tokenized_dataset = dataset.map(preprocess_function, batched=True, remove_columns=dataset["train"].column_names)

# Model
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# Data collator
data_collator = DataCollatorForSeq2Seq(tokenizer, model=model)

# Training arguments
training_args = Seq2SeqTrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    learning_rate=5e-5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    weight_decay=0.01,
    save_total_limit=2,
    num_train_epochs=3,
    predict_with_generate=True,
    logging_dir="./logs",
    logging_steps=50,
)

# Trainer
trainer = Seq2SeqTrainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset["train"],
    eval_dataset=tokenized_dataset["validation"],
    tokenizer=tokenizer,
    data_collator=data_collator,
)

# Train
trainer.train()
