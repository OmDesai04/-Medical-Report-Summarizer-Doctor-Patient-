#!/usr/bin/env python3
"""
Comprehensive Medical Report Summarizer
Handles all organ systems: chest, abdomen, pelvis, bones, etc.
"""

import sys
import re

def comprehensive_summarize(text):
    """Comprehensive medical summarization covering all organ systems."""
    
    text_lower = text.lower()
    
    # Comprehensive medical findings by organ system
    findings = {
        # Liver findings
        "hepatomegaly": "hepatomegaly",
        "fatty infiltration": "fatty infiltration",
        "hepatic lesions": "hepatic lesions",
        "liver": "liver findings",
        
        # Gallbladder findings
        "gallbladder": "gallbladder findings",
        "gallstones": "gallstones",
        "pericholecystic": "pericholecystic fluid",
        "wall thickening": "wall thickening",
        
        # Spleen findings
        "splenomegaly": "splenomegaly",
        "spleen": "spleen findings",
        
        # Kidney findings
        "renal": "renal findings",
        "cortical cysts": "cortical cysts",
        "hydronephrosis": "hydronephrosis",
        "kidney": "kidney findings",
        
        # Pancreas findings
        "pancreas": "pancreas findings",
        "peripancreatic": "peripancreatic fluid",
        
        # Vascular findings
        "aorta": "aortic findings",
        "ectasia": "ectasia",
        "aneurysm": "aneurysm",
        
        # Fluid findings
        "ascites": "ascites",
        "fluid": "fluid",
        
        # Bone/spine findings
        "degenerative": "degenerative changes",
        "lumbar": "lumbar findings",
        "fracture": "fracture",
        "osteoporosis": "osteoporosis",
        
        # Lymph findings
        "lymphadenopathy": "lymphadenopathy",
        "lymph": "lymph node findings",
        
        # Bowel findings
        "bowel obstruction": "bowel obstruction",
        "free air": "free air",
        "bowel": "bowel findings",
        
        # Lung findings (from previous version)
        "ground-glass": "ground-glass opacities",
        "consolidation": "consolidation",
        "atelectasis": "atelectasis",
        "pneumonia": "pneumonia",
        "effusion": "pleural effusion",
        "pneumothorax": "pneumothorax",
        "edema": "pulmonary edema",
        
        # Heart findings
        "cardiomegaly": "cardiomegaly",
        "atrial": "atrial enlargement",
        "ventricular": "ventricular enlargement",
        
        # Other findings
        "thickening": "thickening",
        "cysts": "cysts",
        "lesions": "lesions"
    }
    
    # Negative indicators
    negative_words = ["no", "not", "negative", "absent", "without", "clear", "normal", "unremarkable"]
    
    positive_findings = []
    negative_findings = []
    
    # Process the text systematically
    sentences = re.split(r'[.!?]+', text_lower)
    
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
            
        # Extract findings from this sentence with more precise context
        for term, label in findings.items():
            if term in sentence:
                # Check if this specific term is negated
                is_negated = False
                
                # Look for negation patterns specific to this term
                neg_patterns = [
                    rf"no\s+.*{re.escape(term)}",
                    rf"not\s+.*{re.escape(term)}",
                    rf"negative\s+.*{re.escape(term)}",
                    rf"absent\s+.*{re.escape(term)}",
                    rf"without\s+.*{re.escape(term)}",
                    rf"{re.escape(term)}\s+.*normal",
                    rf"normal\s+.*{re.escape(term)}"
                ]
                
                for pattern in neg_patterns:
                    if re.search(pattern, sentence):
                        is_negated = True
                        break
                
                if is_negated:
                    # This is a negative finding
                    negative_findings.append(f"no {label}")
                else:
                    # This is a positive finding
                    positive_findings.append(label)
    
    # Remove duplicates while preserving order
    positive_findings = list(dict.fromkeys(positive_findings))
    negative_findings = list(dict.fromkeys(negative_findings))
    
    # Generate summary
    summary_parts = []
    
    if positive_findings:
        if len(positive_findings) <= 4:
            summary_parts.append(f"🔍 Findings: {', '.join(positive_findings)}.")
        else:
            summary_parts.append(f"🔍 Multiple findings including: {', '.join(positive_findings[:4])}.")
    
    if negative_findings:
        if len(negative_findings) <= 4:
            summary_parts.append(f"✅ Normal: {', '.join(negative_findings)}.")
        else:
            summary_parts.append(f"✅ Normal findings include: {', '.join(negative_findings[:4])}.")
    
    if not summary_parts:
        return "No significant findings detected."
    
    return " ".join(summary_parts)

def comprehensive_patient_summary(text):
    """Comprehensive patient-friendly summary with explanations for all organ systems."""
    
    summary = comprehensive_summarize(text)
    
    # Comprehensive patient-friendly translations
    patient_terms = {
        # Liver
        "hepatomegaly": "enlarged liver",
        "fatty infiltration": "fat deposits in the liver",
        "hepatic lesions": "spots or masses in the liver",
        "liver findings": "liver changes",
        
        # Gallbladder
        "gallbladder findings": "gallbladder changes",
        "gallstones": "stones in the gallbladder",
        "pericholecystic fluid": "fluid around the gallbladder",
        "wall thickening": "thickened walls",
        
        # Spleen
        "splenomegaly": "enlarged spleen",
        "spleen findings": "spleen changes",
        
        # Kidneys
        "renal findings": "kidney changes",
        "cortical cysts": "small fluid-filled sacs in the kidneys",
        "hydronephrosis": "swelling of the kidney due to urine backup",
        "kidney findings": "kidney changes",
        
        # Pancreas
        "pancreas findings": "pancreas changes",
        "peripancreatic fluid": "fluid around the pancreas",
        
        # Vascular
        "aortic findings": "changes in the main blood vessel",
        "ectasia": "widening of blood vessel",
        "aneurysm": "ballooning of blood vessel",
        
        # Fluid
        "ascites": "fluid in the belly",
        "fluid": "excess fluid",
        
        # Bones
        "degenerative changes": "wear-and-tear changes (arthritis-like)",
        "lumbar findings": "lower back changes",
        "fracture": "broken bone",
        "osteoporosis": "thinning of bones",
        
        # Lymph
        "lymphadenopathy": "enlarged lymph nodes",
        "lymph node findings": "lymph node changes",
        
        # Bowel
        "bowel obstruction": "blockage in the intestines",
        "free air": "air leak in the belly",
        "bowel findings": "intestine changes",
        
        # Lungs (from previous version)
        "ground-glass opacities": "areas in the lungs that look hazy or cloudy",
        "consolidation": "areas of lung tissue that appear solid",
        "atelectasis": "partial collapse of small areas of the lung",
        "pneumonia": "lung infection",
        "pleural effusion": "fluid around the lungs",
        "pneumothorax": "collapsed lung",
        "pulmonary edema": "excess fluid in the lung tissue",
        
        # Heart
        "cardiomegaly": "enlarged heart",
        "atrial enlargement": "enlarged upper heart chamber",
        "ventricular enlargement": "enlarged lower heart chamber",
        
        # General
        "thickening": "thickening",
        "cysts": "fluid-filled sacs",
        "lesions": "spots or masses"
    }
    
    # Apply translations
    for technical, friendly in patient_terms.items():
        summary = summary.replace(technical, friendly)
    
    return summary

def detailed_analysis(text):
    """Detailed analysis showing exactly what was found in each sentence."""
    
    print("🔬 DETAILED ANALYSIS:")
    print("-" * 60)
    
    # Analyze each sentence
    sentences = re.split(r'[.!?]+', text)
    
    for i, sentence in enumerate(sentences, 1):
        sentence = sentence.strip()
        if not sentence:
            continue
            
        print(f"\n📝 Sentence {i}: {sentence}")
        
        # Check for findings
        findings_in_sentence = []
        medical_terms = ["hepatomegaly", "fatty", "infiltration", "gallbladder", "wall", "thickening", 
                        "splenomegaly", "renal", "cortical", "cysts", "ascites", "aorta", "ectasia",
                        "degenerative", "lumbar", "lesions", "gallstones", "pericholecystic", 
                        "hydronephrosis", "pancreas", "peripancreatic", "bowel", "obstruction",
                        "lymphadenopathy", "ground-glass", "opacities", "consolidation", "atelectasis",
                        "pneumonia", "effusion", "pneumothorax", "cardiomegaly", "atrial", "ventricular"]
        
        for term in medical_terms:
            if term in sentence.lower():
                findings_in_sentence.append(term)
        
        # Check if negative
        is_negative = any(neg in sentence.lower() for neg in ["no", "not", "negative", "absent", "without", "normal"])
        
        if findings_in_sentence:
            if is_negative:
                print(f"   ✅ Normal: No {'/'.join(findings_in_sentence)} detected")
            else:
                print(f"   🔍 Finding: {'/'.join(findings_in_sentence)} present")
        else:
            print(f"   ℹ️  No specific medical findings mentioned")
    
    print()

def main():
    if len(sys.argv) < 2:
        print("🏥 Comprehensive Medical Report Summarizer")
        print("=" * 80)
        print("Usage: python comprehensive_summarizer.py \"your medical report text\"")
        print()
        print("Handles all organ systems:")
        print("• Liver, gallbladder, spleen")
        print("• Kidneys, pancreas")
        print("• Heart, lungs, blood vessels")
        print("• Bones, spine")
        print("• Bowel, lymph nodes")
        print()
        print("Example:")
        print("python comprehensive_summarizer.py \"Mild hepatomegaly with early fatty infiltration. Gallbladder wall thickening. No gallstones.\"")
        print()
        print("⚠️  For educational purposes only - always consult your doctor!")
        return
    
    # Get the medical report from command line arguments
    report_text = " ".join(sys.argv[1:])
    
    print("🏥 Comprehensive Medical Report Analysis")
    print("=" * 80)
    print(f"📋 Report: {report_text}")
    print()
    
    # Detailed analysis
    detailed_analysis(report_text)
    
    print("📊 TECHNICAL SUMMARY:")
    print(comprehensive_summarize(report_text))
    print()
    
    print("👥 PATIENT-FRIENDLY SUMMARY:")
    print(comprehensive_patient_summary(report_text))
    print()
    
    print("=" * 80)
    print("⚠️  For educational purposes only - always consult your doctor!")

if __name__ == "__main__":
    main()
