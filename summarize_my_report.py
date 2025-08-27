#!/usr/bin/env python3
"""
Simple Medical Report Summarizer
Use this script to summarize your personal medical reports
"""

import json
import os
import re
from typing import Optional

def simple_summarize(text):
    """Extract explicit findings only, grouped into technical and patient-friendly summaries.

    - Only includes terms explicitly present in the report.
    - Handles basic negations (e.g., "no lymphadenopathy").
    - Separates abnormal and normal mentions.
    """

    text_lower = text.lower()

    # Terms to look for. Order matters for some overlapping terms.
    target_terms = [
        r"\bpneumonia\b",
        r"\bconsolidation\b",
        r"\bpleural effusion\b|\beffusion\b",
        r"\bcardiomegaly\b|\benlarged heart\b",
        r"\bedema\b",
        r"\batelectasis\b",
        r"\bpneumothorax\b|\bcollapsed lung\b",
        r"\bfracture\b",
        r"\bcopd\b",
        r"\bhyperinflation\b",
        r"\bdiaphragm\b",
        r"\blymphadenopathy\b|\benlarged lymph nodes\b",
        # Abdomen-specific
        r"\bhepatomegaly\b|\benlarged liver\b",
        r"\bfatty infiltration\b|\bfatty liver\b|\bhepatic steatosis\b",
        r"\bsplenomegaly\b|\bmild splenomegaly\b|\benlarged spleen\b",
        r"\bgallbladder is distended\b|\bdistended gallbladder\b",
        r"\bfocal hepatic lesions?\b|\bhepatic lesions?\b",
        r"\bhydronephrosis\b",
        r"\bstones?\b|\bcholelithiasis\b",
        # Renal/kidney cysts (laterality captured from the text itself)
        r"\b(?:left\s+|right\s+)?renal cortical cyst\b|\brenal cortical cyst\b|\brenal cyst\b|\bkidney cyst\b|\bcortical cyst\b",
    ]

    negation_words = r"no|without|denies|absent|negative for|not seen|no evidence of"

    technical_abnormal: list[str] = []
    technical_normal: list[str] = []

    # Collect findings exactly as written where possible
    for pattern in target_terms:
        for m in re.finditer(pattern, text_lower, flags=re.IGNORECASE):
            start, end = m.span()
            # Check for negation up to 5 words before
            pre_window_lower = text_lower[max(0, start - 100):start]
            pre_window_org = text[max(0, start - 100):start]
            if re.search(rf"(?:{negation_words})\s+(?:\w+\s+){{0,5}}$", pre_window_lower):
                # Capture the negated phrase as written (approximate): negation + matched term
                neg_match = re.search(rf"({negation_words})\s+(?:\w+\s+){{0,5}}$", pre_window_lower)
                if neg_match:
                    phrase = (pre_window_org[neg_match.start():] + text[start:end]).strip()
                    if phrase not in technical_normal:
                        technical_normal.append(phrase)
                continue

            # Positive (abnormal) finding
            exact_phrase = text[start:end]
            if exact_phrase not in technical_abnormal:
                technical_abnormal.append(exact_phrase)

    # Also capture explicit overall normals like "normal" or "clear" (non-negated)
    # Make sure not preceded by "abnormal" within a small window
    for m in re.finditer(r"\b(normal|clear)\b", text_lower):
        start, end = m.span()
        pre_window = text_lower[max(0, start - 15):start]
        if not re.search(r"abnormal", pre_window):
            exact_phrase = text[start:end]
            if exact_phrase not in technical_normal:
                technical_normal.append(exact_phrase)

    # Build technical summary string
    tech_lines = []
    if technical_abnormal:
        tech_lines.append("Abnormal findings:")
        for item in technical_abnormal:
            tech_lines.append(f"- {item}")
    if technical_normal:
        tech_lines.append("Normal findings:")
        for item in technical_normal:
            tech_lines.append(f"- {item}")
    if not tech_lines:
        tech_lines.append("No significant findings explicitly stated.")
    technical_summary = "\n".join(tech_lines)

    # Build patient-friendly summary from extracted items only
    def to_friendly(term: str) -> str:
        mapping = {
            "pneumonia": "lung infection (pneumonia)",
            "consolidation": "areas of lung tissue that look solid (consolidation)",
            "pleural effusion": "fluid around the lungs",
            "effusion": "fluid around the lungs",
            "cardiomegaly": "heart appears larger than normal",
            "enlarged heart": "heart appears larger than normal",
            "edema": "excess fluid in tissues (edema)",
            "atelectasis": "partial collapse of lung tissue (atelectasis)",
            "pneumothorax": "air leak causing lung collapse (pneumothorax)",
            "collapsed lung": "air leak causing lung collapse",
            "fracture": "broken bone",
            "copd": "chronic lung condition (COPD)",
            "hyperinflation": "over-expanded lungs (hyperinflation)",
            "diaphragm": "changes involving the breathing muscle (diaphragm)",
            "lymphadenopathy": "swollen lymph nodes (lymphadenopathy)",
            "enlarged lymph nodes": "swollen lymph nodes (lymphadenopathy)",
            "renal cortical cyst": "fluid-filled cyst in the kidney",
            "renal cyst": "fluid-filled cyst in the kidney",
            "kidney cyst": "fluid-filled cyst in the kidney",
            "cortical cyst": "fluid-filled cyst in the kidney",
        }
        friendly = term
        for k, v in mapping.items():
            friendly = re.sub(k, v, friendly, flags=re.IGNORECASE)
        # Normalize whitespace
        return re.sub(r"\s+", " ", friendly).strip()

    friendly_lines = []
    if technical_abnormal:
        friendly_lines.append("Abnormal findings (explained):")
        for item in technical_abnormal:
            friendly_lines.append(f"- {to_friendly(item)}")
    if technical_normal:
        friendly_lines.append("Normal findings (as stated):")
        for item in technical_normal:
            # Keep meaning: e.g., "no pleural effusion" -> "no fluid around the lungs"
            norm = item
            norm = re.sub(r"no evidence of|negative for|not seen|without|absent|no", "no", norm, flags=re.IGNORECASE)
            # Replace target medical terms with friendly equivalents but keep the negation
            # Extract leading negation word if present
            neg_prefix_match = re.match(r"\s*(no)\s+(.*)", norm, flags=re.IGNORECASE)
            if neg_prefix_match:
                prefix = neg_prefix_match.group(1)
                rest = neg_prefix_match.group(2)
                rest_friendly = to_friendly(rest)
                norm_friendly = f"{prefix} {rest_friendly}"
            else:
                norm_friendly = to_friendly(norm)
            friendly_lines.append(f"- {norm_friendly}")
    if not friendly_lines:
        friendly_lines.append("No significant findings explicitly stated.")
    patient_friendly = "\n".join(friendly_lines)

    return technical_summary, patient_friendly

def patient_friendly_summary(text):
    """Wrapper that preserves previous API: returns only the friendly summary string."""
    _tech, friendly = simple_summarize(text)
    return friendly

def ocr_extract_text(image_path: str) -> Optional[str]:
    """Extract text from an image file using Tesseract OCR if available.

    Returns extracted text on success, or None with console guidance on failure.
    """
    try:
        from PIL import Image
    except Exception:
        print("❌ PIL (Pillow) is not installed. Install with: pip install pillow")
        return None
    try:
        import pytesseract
    except Exception:
        print("❌ pytesseract is not installed. Install with: pip install pytesseract")
        print("ℹ️ Also install the Tesseract OCR engine: https://tesseract-ocr.github.io/tessdoc/Installation.html")
        return None
    
    # Ensure Tesseract executable is available; if not, guide user to set it up
    def configure_tesseract_path_interactive() -> bool:
        """Try to auto-detect or prompt user for tesseract.exe path on Windows. Returns True if configured."""
        common_paths = [
            r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe",
            r"C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe",
        ]
        for p in common_paths:
            if os.path.isfile(p):
                pytesseract.pytesseract.tesseract_cmd = p
                print(f"✅ Using Tesseract at: {p}")
                return True
        user_path = input("🔧 Tesseract not found. Enter full path to tesseract.exe (or press Enter to cancel): ").strip().strip('"')
        if user_path and os.path.isfile(user_path):
            pytesseract.pytesseract.tesseract_cmd = user_path
            print(f"✅ Using Tesseract at: {user_path}")
            return True
        print("❌ Tesseract path not set. Please install Tesseract or provide a valid path.")
        return False
    
    # Check availability and optionally configure
    try:
        _ = pytesseract.get_tesseract_version()
    except Exception:
        if os.name == "nt":
            if not configure_tesseract_path_interactive():
                return None
        else:
            print("❌ Tesseract not available. Install it and ensure it's on PATH.")
            return None
    try:
        image = Image.open(image_path)
    except Exception as e:
        print(f"❌ Could not open image: {e}")
        return None
    try:
        # Basic OCR; could be enhanced with preprocessing if needed
        text = pytesseract.image_to_string(image)
        if not text or not text.strip():
            print("⚠️ OCR returned no text. Try a clearer image or higher resolution.")
            return None
        return text
    except Exception as e:
        # One retry if on Windows and we can configure path interactively
        if os.name == "nt":
            print(f"⚠️ OCR failed: {e}")
            print("Attempting to configure Tesseract path...")
            if configure_tesseract_path_interactive():
                try:
                    text = pytesseract.image_to_string(image)
                    if not text or not text.strip():
                        print("⚠️ OCR returned no text. Try a clearer image or higher resolution.")
                        return None
                    return text
                except Exception as e2:
                    print(f"❌ OCR failed after configuration: {e2}")
                    return None
        print(f"❌ OCR failed: {e}")
        print("ℹ️ Ensure Tesseract is installed and available on PATH.")
        return None

def main():
    print("🏥 Personal Medical Report Summarizer")
    print("=" * 50)
    print("This tool helps summarize medical reports in simple terms.")
    print("⚠️  For educational purposes only - always consult your doctor!")
    print()
    
    while True:
        print("\nChoose an option:")
        print("1. Summarize a medical report (paste text)")
        print("2. View example")
        print("3. Summarize from an image (OCR)")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            print("\n" + "="*50)
            print("📋 Paste your medical report below (press Enter twice when done):")
            
            lines = []
            while True:
                line = input()
                if line.strip() == "":
                    break
                lines.append(line)
            
            report_text = " ".join(lines)
            
            if report_text.strip():
                print("\n" + "="*50)
                print("📊 TECHNICAL SUMMARY:")
                tech, friendly = simple_summarize(report_text)
                print(tech)
                
                print("\n👥 PATIENT-FRIENDLY SUMMARY:")
                print(friendly)
                
                print("\n" + "="*50)
            else:
                print("❌ No text entered. Please try again.")
                
        elif choice == "2":
            print("\n📖 EXAMPLE MEDICAL REPORT:")
            example = "There is consolidation in the right lower lobe. No pleural effusion. Mild cardiomegaly."
            print(example)
            
            print("\n📊 TECHNICAL SUMMARY:")
            tech, friendly = simple_summarize(example)
            print(tech)
            
            print("\n👥 PATIENT-FRIENDLY SUMMARY:")
            print(friendly)
            
        elif choice == "3":
            print("\n" + "="*50)
            image_path = input("📷 Enter the path to the report image file: ").strip().strip('"')
            if not image_path:
                print("❌ No path provided.")
            elif not os.path.isfile(image_path):
                print("❌ File not found. Please check the path and try again.")
            else:
                print("🔎 Running OCR... This may take a few seconds.")
                extracted = ocr_extract_text(image_path)
                if extracted:
                    print("\n📝 OCR EXTRACTED TEXT (preview):")
                    preview = extracted.strip()
                    print(preview[:500] + ("..." if len(preview) > 500 else ""))
                    print("\n" + "="*50)
                    print("📊 TECHNICAL SUMMARY:")
                    tech, friendly = simple_summarize(extracted)
                    print(tech)
                    print("\n👥 PATIENT-FRIENDLY SUMMARY:")
                    print(friendly)
                # If OCR failed, ocr_extract_text already printed guidance

        elif choice == "4":
            print("👋 Goodbye! Take care!")
            break
            
        else:
            print("❌ Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
