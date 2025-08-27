import json
import os
import shutil

def prepare_sample_data():
    """Prepare the existing sample data for training."""
    
    print("Using existing sample data...")
    
    # Copy sample data to data directory
    os.makedirs("data", exist_ok=True)
    
    sample_files = {
        "train": "sample_data/toy_reports_train.jsonl",
        "validation": "sample_data/toy_reports_val.jsonl", 
        "test": "sample_data/toy_reports_test.jsonl"
    }
    
    for split_name, source_path in sample_files.items():
        if os.path.exists(source_path):
            dest_path = f"data/{split_name}.jsonl"
            shutil.copy2(source_path, dest_path)
            print(f"Copied {source_path} to {dest_path}")
        else:
            print(f"Warning: {source_path} not found")
    
    print("Sample data preparation complete!")
    print("You can now run: python src/train.py")

if __name__ == "__main__":
    prepare_sample_data()
