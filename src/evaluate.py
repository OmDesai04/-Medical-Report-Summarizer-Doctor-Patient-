import json
import os
from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import evaluate

# Paths
test_file = "data/test.jsonl" if os.path.exists("data/test.jsonl") else "data/validation.jsonl"
model_dir = "./results/checkpoint-best"   # Update if you want last checkpoint

# Load dataset
dataset = load_dataset("json", data_files={"test": test_file})
test_data = dataset["test"]

# Load model & tokenizer
model_name = "google/flan-t5-small"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_dir)

# Metric
rouge = evaluate.load("rouge")

# Generate predictions
def generate_summary(example):
    inputs = tokenizer(example["input"], return_tensors="pt", max_length=512, truncation=True)
    output = model.generate(**inputs, max_length=128)
    decoded = tokenizer.decode(output[0], skip_special_tokens=True)
    return {"prediction": decoded}

predictions = test_data.map(generate_summary)

# Evaluate with ROUGE
results = rouge.compute(
    predictions=predictions["prediction"],
    references=predictions["target"]
)

print("Evaluation Results:")
print(results)
