#!/usr/bin/env python3
"""
Enhanced Medical Report Summarizer
Better handling of medical terminology and context
"""

import sys
import re

def enhanced_summarize(text):
    """Enhanced medical summarization with better term recognition and context."""
    
    text_lower = text.lower()
    
    # Enhanced medical conditions with context
    conditions = {
        # Lung findings
        "ground-glass": "ground-glass opacities",
        "opacities": "opacities",
        "consolidation": "consolidation",
        "atelectasis": "atelectasis",
        "pneumonia": "pneumonia",
        "pneumothorax": "pneumothorax",
        "effusion": "pleural effusion",
        "edema": "pulmonary edema",
        "copd": "COPD",
        "hyperinflation": "hyperinflation",
        
        # Heart findings
        "cardiomegaly": "cardiomegaly",
        "atrial": "atrial enlargement",
        "ventricular": "ventricular enlargement",
        "enlargement": "cardiac enlargement",
        
        # Other findings
        "fracture": "fracture",
        "thickening": "septal thickening",
        "interlobular": "interlobular septal thickening",
        "septal": "septal thickening",
        
        # Normal findings
        "normal": "normal",
        "clear": "clear",
        "unremarkable": "unremarkable"
    }
    
    # Negative indicators
    negative_words = ["no", "not", "negative", "absent", "without", "clear", "normal"]
    
    found_conditions = []
    negative_findings = []
    
    # Check for negative findings first
    for word in negative_words:
        if word in text_lower:
            # Look for what's being negated
            pattern = rf"{word}\s+([a-zA-Z]+)"
            matches = re.findall(pattern, text_lower)
            for match in matches:
                if match in conditions:
                    negative_findings.append(f"no {conditions[match]}")
    
    # Check for positive findings
    for term, label in conditions.items():
        if term in text_lower:
            # Make sure it's not a negative finding
            is_negative = False
            for neg_word in negative_words:
                if f"{neg_word} {term}" in text_lower:
                    is_negative = True
                    break
            
            if not is_negative:
                found_conditions.append(label)
    
    # Remove duplicates while preserving order
    seen = set()
    unique_conditions = []
    for condition in found_conditions:
        if condition not in seen:
            seen.add(condition)
            unique_conditions.append(condition)
    
    # Generate summary
    if not unique_conditions and not negative_findings:
        return "No significant findings detected."
    
    summary_parts = []
    
    if unique_conditions:
        if len(unique_conditions) <= 3:
            summary_parts.append(f"🔍 Findings: {', '.join(unique_conditions)}.")
        else:
            summary_parts.append(f"🔍 Multiple findings including: {', '.join(unique_conditions[:3])}.")
    
    if negative_findings:
        summary_parts.append(f"✅ Normal: {', '.join(negative_findings)}.")
    
    if "normal" in text_lower or "clear" in text_lower or "unremarkable" in text_lower:
        summary_parts.append("✅ Overall: Normal findings.")
    
    return " ".join(summary_parts)

def enhanced_patient_summary(text):
    """Enhanced patient-friendly summary with better explanations."""
    
    summary = enhanced_summarize(text)
    
    # Enhanced patient-friendly translations
    patient_terms = {
        "ground-glass opacities": "areas in the lungs that look hazy or cloudy (suggesting inflammation)",
        "consolidation": "areas of lung tissue that appear solid (like in pneumonia)",
        "atelectasis": "partial collapse of small areas of the lung",
        "pneumonia": "lung infection (pneumonia)",
        "pleural effusion": "fluid around the lungs",
        "pulmonary edema": "excess fluid in the lung tissue",
        "COPD": "chronic lung condition (COPD)",
        "hyperinflation": "over-expanded lungs",
        "cardiomegaly": "enlarged heart",
        "atrial enlargement": "enlarged upper heart chamber",
        "ventricular enlargement": "enlarged lower heart chamber",
        "cardiac enlargement": "enlarged heart",
        "fracture": "broken bone",
        "septal thickening": "thickening of the lung tissue walls",
        "interlobular septal thickening": "thickening of the lung tissue walls between lung sections",
        "pneumothorax": "collapsed lung (air leak)",
        "normal": "normal",
        "clear": "clear",
        "unremarkable": "normal"
    }
    
    # Apply translations
    for technical, friendly in patient_terms.items():
        summary = summary.replace(technical, friendly)
    
    return summary

def analyze_report_detailed(text):
    """Detailed analysis of the medical report."""
    
    text_lower = text.lower()
    
    print("🔬 DETAILED ANALYSIS:")
    print("-" * 40)
    
    # Check for specific patterns
    patterns = {
        "Ground-glass opacities": r"ground.?glass|opacities",
        "Interlobular thickening": r"interlobular|septal.?thickening",
        "Pleural effusion": r"pleural.?effusion|effusion",
        "Cardiac findings": r"atrial|ventricular|cardiomegaly|enlargement",
        "Pneumothorax": r"pneumothorax",
        "Negative findings": r"no\s+\w+|negative|absent|without"
    }
    
    for finding, pattern in patterns.items():
        if re.search(pattern, text_lower):
            print(f"✅ {finding}: Detected")
        else:
            print(f"❌ {finding}: Not mentioned")
    
    print()

def main():
    if len(sys.argv) < 2:
        print("🏥 Enhanced Medical Report Summarizer")
        print("=" * 60)
        print("Usage: python enhanced_summarizer.py \"your medical report text\"")
        print()
        print("Example:")
        print("python enhanced_summarizer.py \"Patchy bilateral ground-glass opacities with interlobular septal thickening. Small bilateral pleural effusions. Mild right atrial enlargement. No pneumothorax.\"")
        print()
        print("⚠️  For educational purposes only - always consult your doctor!")
        return
    
    # Get the medical report from command line arguments
    report_text = " ".join(sys.argv[1:])
    
    print("🏥 Enhanced Medical Report Analysis")
    print("=" * 60)
    print(f"📋 Report: {report_text}")
    print()
    
    # Detailed analysis
    analyze_report_detailed(report_text)
    
    print("📊 TECHNICAL SUMMARY:")
    print(enhanced_summarize(report_text))
    print()
    
    print("👥 PATIENT-FRIENDLY SUMMARY:")
    print(enhanced_patient_summary(report_text))
    print()
    
    print("=" * 60)
    print("⚠️  For educational purposes only - always consult your doctor!")

if __name__ == "__main__":
    main()
