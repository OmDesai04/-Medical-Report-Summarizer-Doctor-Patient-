#!/usr/bin/env python3
"""
Quick Medical Report Summarizer
Usage: python quick_summarize.py "your medical report text here"
"""

import sys

def simple_summarize(text):
    """Simple rule-based medical summarization."""
    
    text_lower = text.lower()
    
    # Medical conditions to detect
    conditions = {
        "pneumonia": "pneumonia",
        "consolidation": "consolidation", 
        "effusion": "pleural effusion",
        "cardiomegaly": "enlarged heart",
        "edema": "fluid build-up",
        "atelectasis": "lung collapse",
        "pneumothorax": "collapsed lung",
        "fracture": "bone fracture",
        "normal": "normal",
        "clear": "clear",
        "copd": "COPD",
        "hyperinflation": "hyperinflation",
        "diaphragm": "diaphragm changes"
    }
    
    found_conditions = []
    
    for term, label in conditions.items():
        if term in text_lower:
            found_conditions.append(label)
    
    # Generate summary
    if not found_conditions:
        return "No significant findings detected."
    
    if "normal" in text_lower or "clear" in text_lower:
        return "✅ Normal findings - no significant abnormalities detected."
    elif len(found_conditions) <= 3:
        return f"🔍 Findings: {', '.join(found_conditions)}."
    else:
        return f"🔍 Multiple findings including: {', '.join(found_conditions[:3])}."

def patient_friendly_summary(text):
    """Convert technical summary to patient-friendly language."""
    
    summary = simple_summarize(text)
    
    # Make it more patient-friendly
    patient_terms = {
        "pneumonia": "lung infection (pneumonia)",
        "consolidation": "areas of lung tissue that appear solid",
        "pleural effusion": "fluid around the lungs",
        "enlarged heart": "heart appears larger than normal",
        "fluid build-up": "excess fluid in tissues",
        "lung collapse": "partial collapse of small areas of the lung",
        "collapsed lung": "air leak causing lung to collapse",
        "bone fracture": "broken bone",
        "COPD": "chronic lung condition (COPD)",
        "hyperinflation": "over-expanded lungs",
        "diaphragm changes": "changes in the breathing muscle"
    }
    
    for technical, friendly in patient_terms.items():
        summary = summary.replace(technical, friendly)
    
    return summary

def main():
    if len(sys.argv) < 2:
        print("🏥 Quick Medical Report Summarizer")
        print("=" * 50)
        print("Usage: python quick_summarize.py \"your medical report text\"")
        print()
        print("Example:")
        print("python quick_summarize.py \"There is consolidation in the right lower lobe. No pleural effusion. Mild cardiomegaly.\"")
        print()
        print("⚠️  For educational purposes only - always consult your doctor!")
        return
    
    # Get the medical report from command line arguments
    report_text = " ".join(sys.argv[1:])
    
    print("🏥 Medical Report Summary")
    print("=" * 50)
    print(f"📋 Report: {report_text}")
    print()
    
    print("📊 TECHNICAL SUMMARY:")
    print(simple_summarize(report_text))
    print()
    
    print("👥 PATIENT-FRIENDLY SUMMARY:")
    print(patient_friendly_summary(report_text))
    print()
    
    print("=" * 50)
    print("⚠️  For educational purposes only - always consult your doctor!")

if __name__ == "__main__":
    main()
