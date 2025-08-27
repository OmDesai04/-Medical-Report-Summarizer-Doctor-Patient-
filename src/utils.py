import random
import numpy as np
import torch

def set_seed(seed: int = 42):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

def format_patient_summary(summary: str) -> str:
    # Simple post-processing to make summary more patient-friendly.
    repl = {
        "cardiomegaly": "slightly enlarged heart",
        "pneumonia": "a lung infection (pneumonia)",
        "atelectasis": "partial collapse of small areas of the lung (atelectasis)",
        "edema": "fluid build-up (edema)",
        "COPD": "chronic lung condition (COPD)"
    }
    out = summary
    for k, v in repl.items():
        out = out.replace(k, v)
        out = out.replace(k.capitalize(), v)
    return out
