# src/preprocess.py

import json
import os
from datasets import load_dataset

def load_meqsum_raw():
    dataset = load_dataset(
        "json",
        data_files={
            "train": "https://raw.githubusercontent.com/shwetanlp/CHQ-Summ/master/dataset/meqsum/train.json",
            "validation": "https://raw.githubusercontent.com/shwetanlp/CHQ-Summ/master/dataset/meqsum/validation.json",
            "test": "https://raw.githubusercontent.com/shwetanlp/CHQ-Summ/master/dataset/meqsum/test.json",
        }
    )

    os.makedirs("data", exist_ok=True)

    for split in ["train", "validation", "test"]:
        records = []
        for ex in dataset[split]:
            q = ex.get("CHQ")
            s = ex.get("Summary")
            if q and s:
                records.append({"input": q, "target": s})

        path = f"data/{split}.jsonl"
        with open(path, "w", encoding="utf-8") as f:
            for r in records:
                f.write(json.dumps(r) + "\n")

        print(f"Saved {len(records)} examples to {path}")

if __name__ == "__main__":
    load_meqsum_raw()
