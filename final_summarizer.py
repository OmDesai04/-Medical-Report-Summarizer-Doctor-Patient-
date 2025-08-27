#!/usr/bin/env python3
"""
Final Medical Report Summarizer
Accurately handles medical qualifiers and comprehensive organ systems
"""

import sys
import re

def final_summarize(text):
    """Final comprehensive medical summarization with proper qualifier handling."""
    
    text_lower = text.lower()
    
    # Medical findings organized by system
    findings = {
        # Liver
        "hepatomegaly": "hepatomegaly",
        "fatty infiltration": "fatty infiltration", 
        "hepatic lesions": "hepatic lesions",
        
        # Gallbladder
        "gallbladder wall thickening": "gallbladder wall thickening",
        "wall thickening": "wall thickening",
        "gallstones": "gallstones",
        "pericholecystic fluid": "pericholecystic fluid",
        
        # Spleen
        "splenomegaly": "splenomegaly",
        
        # Kidneys
        "renal cortical cysts": "renal cortical cysts", 
        "cortical cysts": "cortical cysts",
        "hydronephrosis": "hydronephrosis",
        
        # Pancreas
        "peripancreatic fluid": "peripancreatic fluid",
        
        # Fluid/Ascites
        "ascites": "ascites",
        
        # Vascular
        "aorta ectasia": "aorta ectasia",
        "ectasia": "ectasia",
        
        # Spine/Bones
        "lumbar degenerative changes": "lumbar degenerative changes",
        "degenerative changes": "degenerative changes",
        
        # Lymph
        "lymphadenopathy": "lymphadenopathy",
        
        # Bowel
        "bowel obstruction": "bowel obstruction",
        "free air": "free air",
        
        # Lungs (previous)
        "ground-glass opacities": "ground-glass opacities",
        "consolidation": "consolidation",
        "atelectasis": "atelectasis", 
        "pneumonia": "pneumonia",
        "pleural effusion": "pleural effusion",
        "pneumothorax": "pneumothorax",
        
        # Heart
        "cardiomegaly": "cardiomegaly",
        "atrial enlargement": "atrial enlargement"
    }
    
    positive_findings = []
    negative_findings = []
    
    # Process each sentence
    sentences = re.split(r'[.!?]+', text)
    
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
            
        sentence_lower = sentence.lower()
        
        # Check each finding
        for term, label in findings.items():
            if term in sentence_lower:
                # Check for explicit negation
                negation_patterns = [
                    rf"\bno\s+{re.escape(term)}",
                    rf"\bno\s+.*{re.escape(term)}",
                    rf"{re.escape(term)}\s+.*\bnormal\b",
                    rf"\bnormal\b.*{re.escape(term)}",
                    rf"\bnegative\b.*{re.escape(term)}",
                    rf"\babsent\b.*{re.escape(term)}",
                    rf"\bwithout\b.*{re.escape(term)}"
                ]
                
                is_negated = any(re.search(pattern, sentence_lower) for pattern in negation_patterns)
                
                if is_negated:
                    negative_findings.append(f"no {label}")
                else:
                    # Check for medical qualifiers that indicate positive findings
                    qualifiers = ["mild", "moderate", "severe", "trace", "small", "large", "bilateral", "unilateral"]
                    has_qualifier = any(qualifier in sentence_lower for qualifier in qualifiers)
                    
                    # If it has a qualifier or no explicit negation, it's a positive finding
                    positive_findings.append(label)
    
    # Remove duplicates
    positive_findings = list(dict.fromkeys(positive_findings))
    negative_findings = list(dict.fromkeys(negative_findings))
    
    # Generate summary
    summary_parts = []
    
    if positive_findings:
        if len(positive_findings) <= 5:
            summary_parts.append(f"🔍 Findings: {', '.join(positive_findings)}.")
        else:
            summary_parts.append(f"🔍 Multiple findings including: {', '.join(positive_findings[:5])}.")
    
    if negative_findings:
        if len(negative_findings) <= 5:
            summary_parts.append(f"✅ Normal: {', '.join(negative_findings)}.")
        else:
            summary_parts.append(f"✅ Normal findings include: {', '.join(negative_findings[:5])}.")
    
    if not summary_parts:
        return "No significant findings detected."
    
    return " ".join(summary_parts)

def final_patient_summary(text):
    """Final patient-friendly summary with comprehensive explanations."""
    
    summary = final_summarize(text)
    
    # Patient-friendly translations
    patient_terms = {
        "hepatomegaly": "enlarged liver",
        "fatty infiltration": "fat deposits in the liver",
        "hepatic lesions": "spots or masses in the liver",
        "gallbladder wall thickening": "thickened gallbladder wall",
        "wall thickening": "thickened wall",
        "gallstones": "stones in the gallbladder", 
        "pericholecystic fluid": "fluid around the gallbladder",
        "splenomegaly": "enlarged spleen",
        "renal cortical cysts": "small fluid-filled sacs in the outer part of the kidneys",
        "cortical cysts": "small fluid-filled sacs in the kidneys",
        "hydronephrosis": "swelling of the kidney due to urine backup",
        "peripancreatic fluid": "fluid around the pancreas",
        "ascites": "fluid in the belly",
        "aorta ectasia": "widening of the main blood vessel",
        "ectasia": "widening of blood vessel",
        "lumbar degenerative changes": "wear-and-tear changes in the lower back",
        "degenerative changes": "wear-and-tear changes (arthritis-like)",
        "lymphadenopathy": "enlarged lymph nodes",
        "bowel obstruction": "blockage in the intestines",
        "free air": "air leak in the belly",
        "ground-glass opacities": "areas in the lungs that look hazy or cloudy",
        "consolidation": "areas of lung tissue that appear solid",
        "atelectasis": "partial collapse of small areas of the lung",
        "pneumonia": "lung infection",
        "pleural effusion": "fluid around the lungs",
        "pneumothorax": "collapsed lung",
        "cardiomegaly": "enlarged heart",
        "atrial enlargement": "enlarged upper heart chamber"
    }
    
    for technical, friendly in patient_terms.items():
        summary = summary.replace(technical, friendly)
    
    return summary

def final_detailed_analysis(text):
    """Final detailed analysis with proper finding classification."""
    
    print("🔬 COMPREHENSIVE ANALYSIS:")
    print("-" * 70)
    
    sentences = re.split(r'[.!?]+', text)
    
    for i, sentence in enumerate(sentences, 1):
        sentence = sentence.strip()
        if not sentence:
            continue
            
        print(f"\n📝 Sentence {i}: {sentence}")
        
        sentence_lower = sentence.lower()
        
        # Look for specific medical terms
        medical_terms = ["hepatomegaly", "fatty", "infiltration", "gallbladder", "wall", "thickening",
                        "splenomegaly", "renal", "cortical", "cysts", "ascites", "aorta", "ectasia", 
                        "degenerative", "lumbar", "lesions", "gallstones", "pericholecystic",
                        "hydronephrosis", "pancreas", "peripancreatic", "bowel", "obstruction",
                        "lymphadenopathy", "ground-glass", "opacities", "consolidation", "atelectasis",
                        "pneumonia", "effusion", "pneumothorax", "cardiomegaly", "atrial"]
        
        found_terms = [term for term in medical_terms if term in sentence_lower]
        
        # Check for negation
        is_negative = any(neg in sentence_lower for neg in ["no ", "not ", "negative", "absent", "without", " normal"])
        
        # Check for positive qualifiers
        has_qualifier = any(qual in sentence_lower for qual in ["mild", "moderate", "severe", "trace", "small", "large", "bilateral"])
        
        if found_terms:
            if is_negative:
                print(f"   ✅ Normal: No {'/'.join(found_terms)} (negative finding)")
            elif has_qualifier:
                print(f"   🔍 Finding: {'/'.join(found_terms)} present (qualified as positive)")
            else:
                print(f"   🔍 Finding: {'/'.join(found_terms)} present")
        else:
            print(f"   ℹ️  General statement, no specific findings")
    
    print()

def main():
    if len(sys.argv) < 2:
        print("🏥 Final Medical Report Summarizer")
        print("=" * 80)
        print("Accurately handles:")
        print("• Medical qualifiers (mild, moderate, severe, trace, etc.)")
        print("• Negative findings (no, normal, absent, etc.)")
        print("• All organ systems comprehensively")
        print()
        print("Usage: python final_summarizer.py \"your medical report text\"")
        print()
        print("⚠️  For educational purposes only - always consult your doctor!")
        return
    
    report_text = " ".join(sys.argv[1:])
    
    print("🏥 Final Medical Report Analysis")
    print("=" * 80)
    print(f"📋 Report: {report_text}")
    print()
    
    final_detailed_analysis(report_text)
    
    print("📊 TECHNICAL SUMMARY:")
    print(final_summarize(report_text))
    print()
    
    print("👥 PATIENT-FRIENDLY SUMMARY:")
    print(final_patient_summary(report_text))
    print()
    
    print("=" * 80)
    print("⚠️  For educational purposes only - always consult your doctor!")

if __name__ == "__main__":
    main()



