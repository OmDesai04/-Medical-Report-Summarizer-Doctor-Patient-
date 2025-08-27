#!/usr/bin/env python3
"""
Accurate Medical Report Summarizer
Specifically designed for radiology reports and medical imaging findings
"""

import sys
import re

def accurate_summarize(text):
    """Highly accurate medical summarization with proper context understanding."""
    
    text_lower = text.lower()
    
    # Define findings with proper medical context
    findings = {
        # Lung parenchymal findings
        "ground-glass": "ground-glass opacities",
        "consolidation": "consolidation",
        "atelectasis": "atelectasis",
        "pneumonia": "pneumonia",
        "edema": "pulmonary edema",
        
        # Pleural findings
        "effusion": "pleural effusion",
        "pneumothorax": "pneumothorax",
        
        # Cardiac findings
        "atrial": "atrial enlargement",
        "ventricular": "ventricular enlargement",
        "cardiomegaly": "cardiomegaly",
        
        # Other findings
        "thickening": "septal thickening",
        "interlobular": "interlobular septal thickening",
        "fracture": "fracture"
    }
    
    # Negative indicators
    negative_words = ["no", "not", "negative", "absent", "without", "clear", "normal"]
    
    positive_findings = []
    negative_findings = []
    
    # Process the text systematically
    sentences = re.split(r'[.!?]+', text_lower)
    
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
            
        # Check if this sentence contains negative findings
        is_negative_sentence = any(neg in sentence for neg in negative_words)
        
        # Extract findings from this sentence
        for term, label in findings.items():
            if term in sentence:
                if is_negative_sentence:
                    # This is a negative finding
                    negative_findings.append(f"no {label}")
                else:
                    # This is a positive finding
                    positive_findings.append(label)
    
    # Remove duplicates
    positive_findings = list(dict.fromkeys(positive_findings))
    negative_findings = list(dict.fromkeys(negative_findings))
    
    # Generate summary
    summary_parts = []
    
    if positive_findings:
        if len(positive_findings) <= 3:
            summary_parts.append(f"🔍 Findings: {', '.join(positive_findings)}.")
        else:
            summary_parts.append(f"🔍 Multiple findings including: {', '.join(positive_findings[:3])}.")
    
    if negative_findings:
        summary_parts.append(f"✅ Normal: {', '.join(negative_findings)}.")
    
    if not summary_parts:
        return "No significant findings detected."
    
    return " ".join(summary_parts)

def accurate_patient_summary(text):
    """Accurate patient-friendly summary with proper medical explanations."""
    
    summary = accurate_summarize(text)
    
    # Comprehensive patient-friendly translations
    patient_terms = {
        "ground-glass opacities": "areas in the lungs that look hazy or cloudy (suggesting inflammation or infection)",
        "consolidation": "areas of lung tissue that appear solid (like in pneumonia)",
        "atelectasis": "partial collapse of small areas of the lung",
        "pneumonia": "lung infection (pneumonia)",
        "pulmonary edema": "excess fluid in the lung tissue (often related to heart problems)",
        "pleural effusion": "fluid around the lungs",
        "pneumothorax": "collapsed lung (air leak)",
        "atrial enlargement": "enlarged upper heart chamber",
        "ventricular enlargement": "enlarged lower heart chamber",
        "cardiomegaly": "enlarged heart",
        "septal thickening": "thickening of the lung tissue walls",
        "interlobular septal thickening": "thickening of the lung tissue walls between lung sections",
        "fracture": "broken bone"
    }
    
    # Apply translations
    for technical, friendly in patient_terms.items():
        summary = summary.replace(technical, friendly)
    
    return summary

def detailed_analysis(text):
    """Detailed analysis showing exactly what was found and what was normal."""
    
    text_lower = text.lower()
    
    print("🔬 DETAILED ANALYSIS:")
    print("-" * 50)
    
    # Analyze each sentence
    sentences = re.split(r'[.!?]+', text)
    
    for i, sentence in enumerate(sentences, 1):
        sentence = sentence.strip()
        if not sentence:
            continue
            
        print(f"\n📝 Sentence {i}: {sentence}")
        
        # Check for findings
        findings_in_sentence = []
        for term in ["ground-glass", "opacities", "consolidation", "atelectasis", "pneumonia", 
                     "effusion", "pneumothorax", "atrial", "ventricular", "cardiomegaly", 
                     "thickening", "interlobular", "edema", "fracture"]:
            if term in sentence.lower():
                findings_in_sentence.append(term)
        
        # Check if negative
        is_negative = any(neg in sentence.lower() for neg in ["no", "not", "negative", "absent", "without"])
        
        if findings_in_sentence:
            if is_negative:
                print(f"   ✅ Normal: No {'/'.join(findings_in_sentence)} detected")
            else:
                print(f"   🔍 Finding: {'/'.join(findings_in_sentence)} present")
        else:
            print(f"   ℹ️  No specific findings mentioned")
    
    print()

def main():
    if len(sys.argv) < 2:
        print("🏥 Accurate Medical Report Summarizer")
        print("=" * 70)
        print("Usage: python accurate_summarizer.py \"your medical report text\"")
        print()
        print("Example:")
        print("python accurate_summarizer.py \"Patchy bilateral ground-glass opacities with interlobular septal thickening. Small bilateral pleural effusions. Mild right atrial enlargement. No pneumothorax.\"")
        print()
        print("⚠️  For educational purposes only - always consult your doctor!")
        return
    
    # Get the medical report from command line arguments
    report_text = " ".join(sys.argv[1:])
    
    print("🏥 Accurate Medical Report Analysis")
    print("=" * 70)
    print(f"📋 Report: {report_text}")
    print()
    
    # Detailed analysis
    detailed_analysis(report_text)
    
    print("📊 TECHNICAL SUMMARY:")
    print(accurate_summarize(report_text))
    print()
    
    print("👥 PATIENT-FRIENDLY SUMMARY:")
    print(accurate_patient_summary(report_text))
    print()
    
    print("=" * 70)
    print("⚠️  For educational purposes only - always consult your doctor!")

if __name__ == "__main__":
    main()
