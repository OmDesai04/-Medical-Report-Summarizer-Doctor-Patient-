import json
import os
from collections import Counter

def load_data(file_path):
    """Load JSONL data and convert to standard format."""
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                item = json.loads(line)
                # Convert findings->input, impression->target
                data.append({
                    "id": str(len(data)),
                    "input": item.get("findings", ""),
                    "target": item.get("impression", "")
                })
    return data

def simple_summarize(text, max_words=20):
    """Simple rule-based summarization for demo purposes."""
    
    # Basic medical terms to look for
    medical_terms = {
        "pneumonia": "pneumonia",
        "consolidation": "consolidation", 
        "effusion": "effusion",
        "cardiomegaly": "cardiomegaly",
        "edema": "edema",
        "atelectasis": "atelectasis",
        "pneumothorax": "pneumothorax",
        "fracture": "fracture",
        "normal": "normal",
        "clear": "clear"
    }
    
    text_lower = text.lower()
    found_terms = []
    
    for term, label in medical_terms.items():
        if term in text_lower:
            found_terms.append(label)
    
    if not found_terms:
        return "No significant findings detected."
    
    # Create a simple summary
    if "normal" in text_lower or "clear" in text_lower:
        return "Normal findings."
    elif len(found_terms) <= 3:
        return f"Findings: {', '.join(found_terms)}."
    else:
        return f"Multiple findings including: {', '.join(found_terms[:3])}."
    
    return summary

def evaluate_model(test_data):
    """Simple evaluation using exact match."""
    correct = 0
    total = len(test_data)
    
    for item in test_data:
        predicted = simple_summarize(item["input"])
        # Simple similarity check
        if any(word in predicted.lower() for word in item["target"].lower().split()):
            correct += 1
    
    accuracy = correct / total if total > 0 else 0
    print(f"Simple evaluation accuracy: {accuracy:.2%} ({correct}/{total})")
    return accuracy

def main():
    print("Simple Medical Report Summarizer")
    print("=" * 40)
    
    # Load data
    train_data = load_data("data/train.jsonl")
    val_data = load_data("data/validation.jsonl") 
    test_data = load_data("data/test.jsonl")
    
    print(f"Loaded {len(train_data)} training examples")
    print(f"Loaded {len(val_data)} validation examples")
    print(f"Loaded {len(test_data)} test examples")
    
    # Simple evaluation
    print("\nEvaluating on test set...")
    accuracy = evaluate_model(test_data)
    
    # Demo some examples
    print("\nDemo summaries:")
    print("-" * 40)
    
    for i, item in enumerate(test_data[:3]):
        print(f"\nExample {i+1}:")
        print(f"Input: {item['input']}")
        print(f"Target: {item['target']}")
        print(f"Predicted: {simple_summarize(item['input'])}")
    
    print("\n" + "=" * 40)
    print("Training complete! You can now use the summarizer.")
    print("\nTo use with your own reports:")
    print("1. Create a simple script with the simple_summarize() function")
    print("2. Or run: streamlit run src/app_streamlit.py (after installing streamlit)")

if __name__ == "__main__":
    main()
