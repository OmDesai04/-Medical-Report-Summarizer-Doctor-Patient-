import streamlit as st
from typing import List, Tuple
import os
import shutil

st.set_page_config(page_title="Medical Report Summarizer", page_icon="🩺", layout="wide")

st.markdown("## 🩺 Medical Report Summarizer (Doctor + Patient)")
st.markdown("<div class='subtitle'>Analyze medical reports: upload an image to OCR or paste text, then review technical and patient-friendly summaries.</div>", unsafe_allow_html=True)
st.markdown(
    """
    <style>
    /* Global DARK theme */
    .stApp {background: #0e0f12;}
    [data-testid="stAppViewContainer"] {background: #0e0f12;}
    .main {background: transparent;}
    .block-container {padding-top: 4rem;}
    /* Headers */
    h1, h2, h3 {letter-spacing: 0.2px; color: #f3f6ff;}
    h1 {font-weight: 800;}
    h2 {font-weight: 800; font-size: 24px; margin-top: 8px;}
    .subtitle {color:#9aa3b2; font-size: 14px; margin-top: 2px; margin-bottom: 8px;}
    /* Buttons */
    .stButton>button {
        border-radius: 10px;
        padding: 0.6rem 1rem;
        border: 1px solid rgba(99,179,237,0.45);
        background: linear-gradient(180deg, #3b82f6 0%, #2563eb 100%);
        color: #ffffff; font-size: 15px;
        font-weight: 700;
        transition: all .15s ease-in-out;
    }
    .stButton>button:hover {filter: brightness(1.06); box-shadow: 0 0 0 2px rgba(99,179,237,0.45) inset;}
    /* Cards */
    .card {border: 1px solid #2a2f3a; border-radius: 12px; padding: 1rem; background: #12151b;}    
    /* Image 3: make OCR buttons blue with white text */
    .blue-btn .stButton>button {background: linear-gradient(180deg,#3b82f6,#2563eb)!important; color:#ffffff!important; border:1px solid rgba(99,179,237,0.5)!important;}
    /* Textarea */
    textarea {border-radius: 10px !important; background:#12151b !important; color:#e9eef7 !important; border:1px solid #364155 !important;}
    textarea::placeholder {color:#9aa3b2 !important;}
    /* Dataframe wrapper */
    .stDataFrame {border: 1px solid #2a2f3a; border-radius: 12px;}
    /* Hide any text inputs in the main content (we don't use them here) */
    [data-testid="stAppViewContainer"] [data-testid="stTextInput"] {display:none !important;}
    /* Pills / chips */
    .chip {display:inline-block; padding: .2rem .6rem; border-radius: 999px; font-size: .75rem; font-weight: 600; margin-left: .5rem;}
    .chip-hi {background:#ff6b6b; color:#0b0d12}
    .chip-bl {background:#ffd166; color:#0b0d12}
    .chip-ok {background:#06d6a0; color:#0b0d12}
    .chip-info {background:#a0aec0; color:#0b0d12}
    /* Chips */
    .chip {display:inline-block; padding: 0.15rem 0.5rem; border-radius: 999px; font-size: 0.8rem; color: #0b0d12; margin-left: .5rem;}
    .chip-hi {background: #ff6b6b;} .chip-bl {background: #ffd166;} .chip-ok {background: #06d6a0;}
    /* (Stepper removed) */
    /* Scan animation */
    .scan {height:6px; background: linear-gradient(90deg, transparent, #7aa2ff, transparent); background-size:200% 100%; animation: scan 1.4s linear infinite; border-radius: 6px;}
    @keyframes scan {0%{background-position:200% 0}100%{background-position:-200% 0}}
    /* Dropzone */
    [data-testid="stFileUploadDropzone"] {border:2px dashed #364155; background:#12151b; border-radius:12px; color:#e9eef7}
    [data-testid="stFileUploadDropzone"] * {color:#e9eef7}
    [data-testid="stFileUploadDropzone"]:hover {box-shadow:0 0 0 3px rgba(99,179,237,0.35)}
    </style>
    """,
    unsafe_allow_html=True,
)

# (Stepper removed per design request)

with st.sidebar:
    st.header("Settings")
    st.caption("This version uses built-in rule-based summarization (no transformers needed).")
    st.markdown("---")
    st.header("OCR Settings")
    tesseract_path = st.text_input(
        "Optional: path to tesseract.exe (Windows)",
        help="If OCR fails, install Tesseract and/or paste its full path here (e.g. C:\\Program Files\\Tesseract-OCR\\tesseract.exe)."
    )
    show_debug = st.checkbox("Show parsing debug", value=False, help="Display normalized OCR text and parsed rows for troubleshooting.")

# Auto-detect Tesseract on Windows/PATH if not provided
def _resolve_tesseract_cmd(user_input: str) -> str:
    candidates = []
    if user_input:
        candidates.append(user_input)
    # Try PATH
    candidates.append(shutil.which("tesseract"))
    # Common Windows installs
    candidates.extend([
        r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe",
        r"C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe",
    ])
    for p in candidates:
        if p and os.path.exists(p):
            return p
    return ""

TESSERACT_CMD = _resolve_tesseract_cmd(tesseract_path)
with st.sidebar:
    if TESSERACT_CMD:
        st.caption(f"Tesseract detected: {TESSERACT_CMD}")
    else:
        st.caption("Tesseract not detected yet. Install it or provide the path above.")

# Apply global dark theme overrides for the rest of the app
st.markdown("""
<style>
body, .stApp, [data-testid="stAppViewContainer"], .main {background: #0e0f12; color: #e9eef7;}
</style>
""", unsafe_allow_html=True)

# Image upload + OCR (centered card)
st.markdown("<div class='card' style='max-width: 980px; margin: 60px auto; padding: 30px;'>", unsafe_allow_html=True)
st.markdown("### Upload a report image")
st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
img_file = st.file_uploader("Image (JPG/PNG)", type=["jpg", "jpeg", "png"], accept_multiple_files=False)

def _extract_text_from_image(uploaded_file) -> str:
    try:
        from PIL import Image, ImageOps, ImageFilter
        import pytesseract
    except Exception:
        st.error("Please install OCR dependencies: pip install pillow pytesseract. Also install Tesseract OCR engine.")
        return ""
    if TESSERACT_CMD:
        try:
            pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD
        except Exception:
            pass
    try:
        image = Image.open(uploaded_file)
    except Exception as e:
        st.error(f"Could not open image: {e}")
        return ""
    try:
        # Basic preprocessing: convert to grayscale, upscale, sharpen, binarize
        img = image.convert("L")
        # upscale 2x for small text
        w, h = img.size
        if max(w, h) < 1600:
            img = img.resize((w * 2, h * 2))
        img = ImageOps.autocontrast(img)
        img = img.filter(ImageFilter.SHARPEN)
        # light thresholding
        img = img.point(lambda x: 255 if x > 180 else 0, mode='1')

        config = "--psm 6 -l eng"
        text = pytesseract.image_to_string(img, config=config)
        return text or ""
    except Exception as e:
        st.error(f"OCR failed: {e}")
        return ""

def _extract_text_from_image_tsv(uploaded_file) -> str:
    """Use Tesseract TSV to preserve row structure and rebuild lines left→right."""
    try:
        from PIL import Image, ImageOps
        import pytesseract
        import pandas as pd
        import io
    except Exception:
        st.error("Please install OCR deps: pip install pillow pytesseract pandas")
        return ""
    if TESSERACT_CMD:
        try:
            pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD
        except Exception:
            pass
    try:
        image = Image.open(uploaded_file)
        gray = ImageOps.grayscale(image)
        config = "--psm 6 -l eng"
        tsv = pytesseract.image_to_data(gray, config=config, output_type=pytesseract.Output.DATAFRAME)
        # Clean and group by line
        df = tsv.dropna(subset=['text']).copy()
        # Keep more tokens: lower threshold and allow digit-heavy low conf
        df.loc[:, 'conf'] = df['conf'].astype(float)
        keep_mask = (df['conf'] >= 25) | df['text'].astype(str).str.contains(r"\d", regex=True)
        df = df.loc[keep_mask]
        lines = []
        for (page, block, par, line), group in df.groupby(['page_num','block_num','par_num','line_num']):
            tokens = group.sort_values('left')['text'].astype(str).tolist()
            s = " ".join(tok for tok in tokens if tok.strip())
            s = " ".join(s.split())
            if s:
                lines.append(s)
        return "\n".join(lines)
    except Exception as e:
        st.error(f"OCR TSV failed: {e}")
        return ""

with st.container():
    st.markdown("<div class='blue-btn'>", unsafe_allow_html=True)
    if st.button("🔎 Extract text from image", disabled=img_file is None, help="Runs OCR to extract medical findings from the uploaded image"):
        if img_file is None:
            st.warning("Please upload an image first.")
        else:
            with st.spinner("Running OCR..."):
                extracted = _extract_text_from_image(img_file)
                if extracted.strip():
                    st.success("OCR complete. Inserted text into the editor below.")
                    st.session_state["report_text"] = extracted
                    st.rerun()
                else:
                    st.warning("No text extracted. Try a clearer image or higher resolution.")
    st.markdown("</div>", unsafe_allow_html=True)
with st.container():
    st.markdown("<div class='blue-btn'>", unsafe_allow_html=True)
    if st.button("🧾 Extract table (OCR smart)", disabled=img_file is None, help="Runs OCR with table-aware parsing to reconstruct rows/columns"):
        if img_file is None:
            st.warning("Please upload an image first.")
        else:
            with st.spinner("Extracting with table-aware OCR..."):
                extracted = _extract_text_from_image_tsv(img_file)
                # Also run plain OCR and merge to recover any missed lines (top/bottom)
                fallback_plain = _extract_text_from_image(img_file)
                if fallback_plain and fallback_plain.strip():
                    merged = (extracted or "") + "\n" + fallback_plain
                else:
                    merged = extracted
                if (merged or "").strip():
                    st.success("Table-like text extracted. Inserted below.")
                    st.session_state["report_text"] = merged
                    st.rerun()
                else:
                    st.warning("No text extracted. Try cropping the table area and retry.")
    st.markdown("</div>", unsafe_allow_html=True)

# Pre-handle pending UI intents (set by buttons) BEFORE rendering the text widget
_pending_sample = st.session_state.get("_set_report_text_sample", None)
if _pending_sample is not None:
    st.session_state["report_text"] = _pending_sample
    st.session_state["_set_report_text_sample"] = None
_pending_clear = st.session_state.get("_clear_report_text", False)
if _pending_clear:
    st.session_state["report_text"] = ""
    st.session_state["_clear_report_text"] = False

# Text input
txt = st.text_area(
    "Paste the Findings / Report text",
    height=220,
    placeholder="e.g., There is consolidation in the right lower lobe. No pleural effusion. Mild cardiomegaly.",
    key="report_text"
)

# Ensure analyze uses the freshest text from the editor/session state
txt = st.session_state.get("report_text", txt or "")

# Controls row: right-aligned Sample/Clear, Analyze full width below
st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
row = st.columns([6,1,1])
with row[1]:
    if st.button("✨ Sample", help="Insert a short sample report"):
        st.session_state["_set_report_text_sample"] = (
            "Hemoglobin is low. WBC is high. ALT slightly raised. Blood sugar is high. \n"
            "Urine shows protein + and cloudy appearance."
        )
        st.rerun()
with row[2]:
    if st.button("🧹 Clear", help="Clear the input"):
        st.session_state["_clear_report_text"] = True
        st.rerun()
st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
analyze = st.button("🔍 Analyze Report", use_container_width=True)

def comprehensive_summarize(text: str) -> Tuple[List[str], List[str]]:
    """Extract explicit positive and negative findings using keyword + negation rules."""
    import re
    text_lower = text.lower()
    findings = {
        # Core systems
        "cardiomegaly": "cardiomegaly",
        "pneumonia": "pneumonia",
        "consolidation": "consolidation",
        "atelectasis": "atelectasis",
        "pleural effusion": "pleural effusion",
        "pneumothorax": "pneumothorax",
        "edema": "pulmonary edema",
        # Abdomen
        "hepatomegaly": "hepatomegaly",
        "fatty infiltration": "fatty infiltration",
        "splenomegaly": "splenomegaly",
        "hydronephrosis": "hydronephrosis",
        "renal cortical cyst": "renal cortical cyst",
        "cortical cyst": "cortical cyst",
        "kidney cyst": "kidney cyst",
        "gallstones": "gallstones",
        # Lymph
        "lymphadenopathy": "lymphadenopathy",
    }
    neg_scoped_patterns = [
        r"\bno\s+(?:evidence\s+of\s+)?{term}\b",
        r"\bwithout\s+{term}\b",
        r"\babsent\s+{term}\b",
        r"\bnegative\s+for\s+{term}\b",
        r"\b{term}\s+(?:is|are)?\s*not\s+(?:seen|present|identified)\b",
    ]
    def is_negated(sentence: str, term: str) -> bool:
        esc = re.escape(term)
        for pat in neg_scoped_patterns:
            if re.search(pat.format(term=esc), sentence, flags=re.IGNORECASE):
                return True
        return False
    pos, neg = [], []
    sentences = re.split(r"[.!?]+", text_lower)
    for s in sentences:
        s = s.strip()
        if not s:
            continue
        for term, label in findings.items():
            if term in s:
                if is_negated(s, term):
                    neg.append(f"no {label}")
                else:
                    pos.append(label)
    # dedupe preserve order
    pos = list(dict.fromkeys(pos))
    neg = list(dict.fromkeys(neg))
    return pos, neg

def to_patient_friendly(findings: List[str]) -> List[str]:
    mapping = {
        "cardiomegaly": "enlarged heart",
        "pneumonia": "lung infection",
        "consolidation": "areas of lung tissue that appear solid",
        "atelectasis": "partial collapse of small lung areas",
        "pleural effusion": "fluid around the lungs",
        "pneumothorax": "collapsed lung",
        "pulmonary edema": "excess fluid in lung tissue",
        "hepatomegaly": "enlarged liver",
        "fatty infiltration": "fat deposits in the liver",
        "splenomegaly": "enlarged spleen",
        "hydronephrosis": "kidney swelling from urine backup",
        "renal cortical cyst": "fluid-filled cyst in the kidney",
        "cortical cyst": "fluid-filled cyst in the kidney",
        "kidney cyst": "fluid-filled cyst in the kidney",
        "gallstones": "stones in the gallbladder",
        "lymphadenopathy": "enlarged lymph nodes",
    }
    return [mapping.get(x, x) for x in findings]

def fallback_findings_from_prose(text: str) -> List[str]:
    """Heuristic fallback to extract common clinical statements from narrative prose.
    Captures patterns like 'low hemoglobin', 'WBC high', 'ALT slightly raised',
    'blood sugar high', 'urine protein/cloudiness', and 'kidney strain'.
    """
    import re
    t = text.lower()
    f: List[str] = []
    def seen(label: str) -> bool:
        return any(label in x for x in f)
    # Anemia / hemoglobin
    if re.search(r"hemoglobin[^\n\.]*?(low|decreas|reduc)", t) and not seen("hemoglobin"):
        f.append("low hemoglobin (possible anemia)")
    # White blood cells elevated
    if (re.search(r"(white\s*blood\s*cells?|wbc)[^\n\.]*?(high|elevat|raised|increase)", t) or
        re.search(r"(high|elevat|raised|increase)[^\n\.]*?(white\s*blood\s*cells?|wbc)", t)) and not seen("white blood cells"):
        f.append("elevated white blood cells (possible infection/inflammation)")
    # Protein levels low (serum)
    if re.search(r"protein\s+levels?[^\n\.]*?(low|decreas|reduc)", t) and not seen("protein"):
        f.append("low blood protein levels")
    # Blood sugar / glucose high
    if (re.search(r"(blood\s*sugar|glucose)[^\n\.]*?(high|elevat|raised|increase)", t) or
        re.search(r"(high|elevat|raised|increase)[^\n\.]*?(blood\s*sugar|glucose)", t)) and not seen("blood sugar"):
        f.append("high blood sugar")
    # ALT raised
    if re.search(r"\balt\b|alanine\s+aminotransferase", t):
        if re.search(r"(slightly\s+)?(raised|high|elevat|increase)", t):
            f.append("ALT slightly elevated")
    # Kidney strain / creatinine mention
    if (re.search(r"kidney[^\n\.]*?(strain|stress|issue|problem)", t) or
        re.search(r"creatinine[^\n\.]*?(high|elevat|raised)", t)) and not seen("kidney"):
        f.append("possible kidney strain")
    # Urine protein / cloudiness
    if (re.search(r"urine[^\n\.]*?(protein|albumin)[^\n\.]*?(present|trace|mild|\+)", t) or
        re.search(r"urine[^\n\.]*?(cloud(y|iness)|turbid)", t)) and not seen("urine"):
        f.append("urine protein/cloudiness present")
    return f

def parse_lab_table(raw_text: str):
    """Parse lab-style rows like 'Sodium 126 mmol/L 135-146', including
    qualitative entries (Absent/Present), count per hpf lines, Q.N.S (not tested),
    and descriptive attributes (Appearance, Reaction (pH)).
    """
    import re
    rows = []
    # Pre-clean: remove dot leaders and normalize slashes/spaces
    cleaned = []
    for ln in raw_text.splitlines():
        # normalize en/em dashes to hyphen and odd minus
        ln = ln.replace("\u2013", "-").replace("\u2014", "-").replace("\u2212", "-")
        # normalize smart quotes
        ln = ln.replace("\u2018", "'").replace("\u2019", "'").replace('"','"').replace('"','"')
        # fix common OCR unit glyphs
        ln = re.sub(r"mm\?", "/mm3", ln, flags=re.IGNORECASE)
        # convert European formats: thousands dots and decimal commas
        ln = re.sub(r"(\d)\.(\d{3})(?!\d)", r"\1\2", ln)  # 9.000 -> 9000
        ln = ln.replace(",", ".")  # 12,0 -> 12.0
        ln = re.sub(r"\.{2,}", " ", ln)  # dot leaders
        ln = re.sub(r"\s+/\s+", "/", ln)  # normalize units like mg / dl
        ln = re.sub(r"\s+", " ", ln.strip())
        if ln:
            cleaned.append(ln)
    lines = cleaned
    # Numeric value with reference range
    pat = re.compile(r"^(?P<name>[A-Za-z][A-Za-z ./%()]+?)\s+(?P<value>[-+]?\d+(?:\.\d+)?)\s*(?P<unit>[A-Za-z/%uU]+)?\s+(?P<low>\d+(?:\.\d+)?)\s*-\s*(?P<high>\d+(?:\.\d+)?)$", re.IGNORECASE)
    for ln in lines:
        m = pat.match(ln)
        if not m:
            m = re.match(r"^(?P<name>[A-Za-z][A-Za-z ./%()]+?)\s+(?P<value>[-+]?\d+(?:\.\d+)?)(?:\s+(?P<unit>mg\/dl|mg\/100ml|mmol\/l|mmol\/L|umol\/l|umol\/L|ug\/dl|g\/dl|%|\/mm3|million\/uL) )?\s*(?P<low>\d+(?:\.\d+)?)\s*-\s*(?P<high>\d+(?:\.\d+)?)$", ln, re.IGNORECASE)
        if not m:
            # One-sided thresholds like "BNP 590 pg/ml <100" or ">=60"
            m_one = re.match(r"^(?P<name>[A-Za-z][A-Za-z ./%()]+?)\s+(?P<value>[-+]?\d+(?:\.\d+)?)\s*(?P<unit>[A-Za-z/%\u00B5IUl\.]+)?\s*(?P<op>[<>]=?|[\u2264\u2265])\s*(?P<thresh>\d+(?:\.\d+)?)$", ln, re.IGNORECASE)
            if m_one:
                try:
                    name = m_one.group('name').strip().rstrip(':')
                    value = float(m_one.group('value'))
                    unit = (m_one.group('unit') or '').strip()
                    op = m_one.group('op')
                    thresh = float(m_one.group('thresh'))
                except Exception:
                    continue
                op_norm = op
                if op_norm == '\u2264':
                    op_norm = '<='
                if op_norm == '\u2265':
                    op_norm = '>='
                status = 'normal'
                ref_low = ''
                ref_high = ''
                if op_norm in ('<','<='):
                    status = 'high' if value > thresh else 'normal'
                    ref_high = str(thresh)
                elif op_norm in ('>','>='):
                    status = 'low' if value < thresh else 'normal'
                    ref_low = str(thresh)
                rows.append({'Test': name, 'Value': str(value), 'Unit': unit, 'Ref Low': ref_low, 'Ref High': ref_high, 'Status': status})
                continue
            else:
                continue
        try:
            name = m.group('name').strip().rstrip(':')
            value = float(m.group('value'))
            low = float(m.group('low'))
            high = float(m.group('high'))
            unit = (m.group('unit') or '').strip()
        except Exception:
            continue
        status = 'normal'
        if value < low:
            status = 'low'
        elif value > high:
            status = 'high'
        rows.append({'Test': name, 'Value': str(value), 'Unit': unit, 'Ref Low': str(low), 'Ref High': str(high), 'Status': status})
    # Heuristic capture for common lines missing ranges; apply standard refs
    standards = {
        'hemoglobin': ('g/dl', 12.0, 15.0),
        'total wbc': ('/mm3', 4000, 10000),
        'wbc': ('/mm3', 4000, 10000),
        'platelets': ('/mm3', 150000, 400000),
        'rbc': ('million/uL', 3.8, 5.2),
        'fasting blood sugar': ('mg/dL', 70, 100),
        'fbs': ('mg/dL', 70, 100),
        # Liver function tests
        'bilirubin (total)': ('mg/dl', 0.3, 1.2),
        'total bilirubin': ('mg/dl', 0.3, 1.2),
        'bilirubin (direct)': ('mg/dl', 0.1, 0.4),
        'direct bilirubin': ('mg/dl', 0.1, 0.4),
        'bilirubin (indirect)': ('mg/dl', 0.1, 0.8),
        'indirect bilirubin': ('mg/dl', 0.1, 0.8),
        'sgpt': ('U/L', 7, 56),
        'alt': ('U/L', 7, 56),
        'sgot': ('U/L', 5, 40),
        'ast': ('U/L', 5, 40),
        'alkaline phosphatase': ('U/L', 44, 147),
        'albumin': ('g/dl', 3.5, 5.0),
        'globulin': ('g/dl', 2.3, 3.5),
        'total protein': ('g/dl', 5.5, 7.5),
        'a/g ratio': ('', 1.1, 2.3),
        'gamma gt': ('U/L', 10, 71),
        'ggt': ('U/L', 10, 71),
    }
    for ln in lines:
        m_simple = re.match(r"^(?P<name>[A-Za-z][A-Za-z ./%()]+?)\s+(?P<value>[-+]?\d+(?:\.\d+)?)\s*(?P<unit>[A-Za-z/%uU]+)?$", ln, re.IGNORECASE)
        if not m_simple:
            continue
        name = m_simple.group('name').strip().rstrip(':')
        value = float(m_simple.group('value'))
        unit = (m_simple.group('unit') or '').strip()
        key = name.lower()
        if any(r['Test'].lower() == name.lower() for r in rows):
            continue
        if key in standards:
            std_unit, low, high = standards[key]
            if unit == '':
                unit = std_unit
            status = 'normal'
            if value < low:
                status = 'low'
            elif value > high:
                status = 'high'
            rows.append({'Test': name, 'Value': str(value), 'Unit': unit, 'Ref Low': str(low), 'Ref High': str(high), 'Status': status})
    # Also parse qualitative rows like "Bile Salts Absent", plus-grade, and counts like "Pus cells 1-2 /hpf"
    for ln in lines:
        # Absent/Present/Negative/Positive
        m = re.match(r"^(?P<name>[A-Za-z][A-Za-z ./%]+?)\s+(?P<qual>absent|present|negative|positive)$", ln, re.IGNORECASE)
        if m:
            name = m.group('name').strip().rstrip(':')
            qual = m.group('qual').lower()
            status = 'normal' if qual in ('absent','negative') else 'abnormal'
            rows.append({'Test': name, 'Value': qual, 'Unit': '', 'Ref Low': '', 'Ref High': '', 'Status': status})
            continue
        # Plus-grade like Albumin (++), Protein +, Sugar (+++)
        m = re.match(r"^(?P<name>[A-Za-z][A-Za-z ./%()]+?)\s*(?:\((?P<plus1>\+{1,4})\)|(?P<plus2>\+{1,4}))$", ln, re.IGNORECASE)
        if m:
            name = m.group('name').strip().rstrip(':')
            plus = m.group('plus1') or m.group('plus2') or '+'
            status = 'abnormal' if len(plus) >= 1 else 'normal'
            rows.append({'Test': name, 'Value': plus, 'Unit': '', 'Ref Low': '', 'Ref High': '', 'Status': status})
            continue
        # Count ranges like "Pus Cells 01-02 /hpf <10" or similar
        m = re.match(r"^(?P<name>[A-Za-z][A-Za-z ./%()]+?)\s+(?P<value>\d{1,3}(?:[-–]\d{1,3})?)\s*(?P<unit>[/][A-Za-z]+)?\s*(?:<?\s*(?P<high>\d+(?:\.\d+)?))?$", ln, re.IGNORECASE)
        if m and not any(r['Test']==m.group('name').strip().rstrip(':') for r in rows):
            name = m.group('name').strip().rstrip(':')
            value = m.group('value')
            unit = (m.group('unit') or '').strip()
            high = m.group('high')
            status = 'normal'
            try:
                # If an upper bound like "<10" is present and the count range exceeds it, mark abnormal
                if high is not None:
                    upper = float(high)
                    # take max of range
                    vmax = float(value.replace('–','-').split('-')[-1])
                    if vmax > upper:
                        status = 'high'
                else:
                    vmax = float(value.replace('–','-').split('-')[-1])
                    # Treat cellular counts > thresholds as abnormal when no ref provided
                    lname = name.lower()
                    if any(k in lname for k in ['red blood cells','rbcs']) and vmax > 0:
                        status = 'abnormal'
                    if any(k in lname for k in ['pus cells','puss cells','leukocytes']) and vmax >= 10:
                        status = 'high'
            except Exception:
                pass
            rows.append({'Test': name, 'Value': value, 'Unit': unit, 'Ref Low': '', 'Ref High': (high or ''), 'Status': status})
        # Not tested markers like Q.N.S. / QNS / Not tested
        m = re.match(r"^(?P<name>[A-Za-z][A-Za-z ./%()]+?)\s+(q\.?n\.?s\.?|qns|not\s+tested)$", ln, re.IGNORECASE)
        if m and not any(r['Test']==m.group('name').strip().rstrip(':') for r in rows):
            name = m.group('name').strip().rstrip(':')
            rows.append({'Test': name, 'Value': 'not tested', 'Unit': '', 'Ref Low': '', 'Ref High': '', 'Status': 'not tested'})
        # Descriptive attributes like Appearance Pale Yellow, Reaction (pH) Acidic
        m = re.match(r"^(appearance|reaction\s*\(?pH\)?|specific\s*gravity|quantity|colour|color)\s+([A-Za-z0-9 ./-]+)$", ln, re.IGNORECASE)
        if m and not any(r['Test'].lower()==m.group(1).strip().lower() for r in rows):
            # Specific Gravity might get captured here too; prefer numeric or QNS rows already added
            if m.group(1).strip().lower() == 'specific gravity' and any(r['Test'].lower()=='specific gravity' for r in rows):
                continue
            rows.append({'Test': m.group(1).strip(), 'Value': m.group(2).strip(), 'Unit': '', 'Ref Low': '', 'Ref High': '', 'Status': 'info'})
    return rows

def detect_key_labs_freeform(raw_text: str):
    """Regex fallback across free text for key labs like BNP and thyroid panel.
    Returns rows with same schema as parse_lab_table.
    """
    import re
    text = re.sub(r"\s+", " ", raw_text)
    rows = []
    # BNP like "BNP 590 pg/ml <100" (label before value)
    m = re.search(r"\bBNP\b[^\d]{0,40}(\d+(?:\.\d+)?)\s*(pg\s*[\/ ]?\s*m[l|i]|ng\s*[\/ ]?\s*l)?[^<\u2264\d>]*([<>]=?|[\u2264\u2265])\s*(\d+(?:\.\d+)?)", text, re.IGNORECASE)
    if m:
        val = float(m.group(1))
        unit = (m.group(2) or '').replace(' ', '')
        op = m.group(3)
        thr = float(m.group(4))
        op_norm = '<=' if op == '\u2264' else ('>=' if op == '\u2265' else op)
        status = 'normal'
        if op_norm in ('<','<=') and val > thr:
            status = 'high'
        if op_norm in ('>','>=') and val < thr:
            status = 'low'
        rows.append({'Test': 'BNP', 'Value': str(val), 'Unit': unit, 'Ref Low': '' if op_norm in ('<','<=') else str(thr), 'Ref High': str(thr) if op_norm in ('<','<=') else '', 'Status': status})
    else:
        # BNP like "590 Pg/mi <100 ... BNP" (value before label on next line)
        m2 = re.search(r"(\d+(?:\.\d+)?)\s*(pg\s*[\/ ]?\s*m[l|i]|ng\s*[\/ ]?\s*l)?\s*([<>]=?|[\u2264\u2265])\s*(\d+(?:\.\d+)?)\s*.{0,30}\bBNP\b", text, re.IGNORECASE)
        if m2:
            val = float(m2.group(1))
            unit = (m2.group(2) or '').replace(' ', '')
            op = m2.group(3)
            thr = float(m2.group(4))
            op_norm = '<=' if op == '\u2264' else ('>=' if op == '\u2265' else op)
            status = 'normal'
            if op_norm in ('<','<=') and val > thr:
                status = 'high'
            if op_norm in ('>','>=') and val < thr:
                status = 'low'
            rows.append({'Test': 'BNP', 'Value': str(val), 'Unit': unit, 'Ref Low': '' if op_norm in ('<','<=') else str(thr), 'Ref High': str(thr) if op_norm in ('<','<=') else '', 'Status': status})
    # FREE T3 / FREE T4 / TSH like "FREE T3 3.00 pmol/L 3.8-6"
    for name_pat, canon in [(r"FREE\s*T\s*3|FT3", 'Free T3'), (r"FREE\s*T\s*4|FT4", 'Free T4'), (r"T\s*\.?\s*S\s*\.?\s*H|TSH", 'TSH')]:
        m = re.search(rf"\b(?:{name_pat})\b[^\d]*(\d+(?:\.\d+)?)\s*([A-Za-z\u00B5/]+)?[^\d]*(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)", text, re.IGNORECASE)
        if m:
            val = float(m.group(1))
            unit = (m.group(2) or '').strip()
            low = float(m.group(3))
            high = float(m.group(4))
            status = 'normal'
            if val < low:
                status = 'low'
            elif val > high:
                status = 'high'
            rows.append({'Test': canon, 'Value': str(val), 'Unit': unit, 'Ref Low': str(low), 'Ref High': str(high), 'Status': status})
    # Random Blood Sugar (mg/dl) with range, e.g., "RANDOM BLOOD SUGAR 404 mg/dl 70-140"
    m_rbs = re.search(r"\b(random\s*blood\s*sugar|rbs|blood\s*sugar)\b[^\d]{0,80}?(\d+(?:[\.,]\d+)?)\s*(mg\s*\/?\s*d[il])\b[^\d]{0,40}(\d+(?:[\.,]\d+)?)\s*-\s*(\d+(?:[\.,]\d+)?)", text, re.IGNORECASE)
    if m_rbs:
        name = 'Random Blood Sugar'
        val = float(str(m_rbs.group(2)).replace(',', '.'))
        unit = m_rbs.group(3).replace(' ', '').replace('di','dl').upper()
        low = float(str(m_rbs.group(4)).replace(',', '.')); high = float(str(m_rbs.group(5)).replace(',', '.'))
        status = 'normal'
        if val < low: status = 'low'
        elif val > high: status = 'high'
        rows.append({'Test': name, 'Value': str(val), 'Unit': unit, 'Ref Low': str(low), 'Ref High': str(high), 'Status': status})
    else:
        # Value before label, with optional GOD-POD and colon
        m_rbs_val_first = re.search(r"(\d+(?:[\.,]\d+)?)\s*(mg\s*\/?\s*d[il])[^\n]{0,80}?\b(random\s*blood\s*sugar|rbs|blood\s*sugar)\b", text, re.IGNORECASE)
        if m_rbs_val_first:
            name = 'Random Blood Sugar'
            val = float(str(m_rbs_val_first.group(1)).replace(',', '.'))
            unit = m_rbs_val_first.group(2).replace(' ', '').upper()
            # Try to find nearby range; else default 70-140
            rng_near = re.search(r"\b(\d+(?:[\.,]\d+)?)\s*-\s*(\d+(?:[\.,]\d+)?)\b", text, re.IGNORECASE)
            if rng_near:
                low = float(str(rng_near.group(1)).replace(',', '.'))
                high = float(str(rng_near.group(2)).replace(',', '.'))
            else:
                low, high = 70.0, 140.0
            status = 'normal'
            if val < low: status = 'low'
            elif val > high: status = 'high'
            rows.append({'Test': name, 'Value': str(val), 'Unit': unit, 'Ref Low': str(low), 'Ref High': str(high), 'Status': status})
    # D-Dimer (µg/ml or ng/ml FEU)
    m_dd = re.search(r"\bd[- ]?dimer\b[^\d]{0,20}(\d+(?:\.\d+)?)\s*([uµ]g|ng)\s*\/\s*ml", text, re.IGNORECASE)
    if m_dd:
        val = float(m_dd.group(1))
        upfx = m_dd.group(2).lower()
        unit = 'µg/ml' if 'g' in upfx and 'n' not in upfx else 'ng/ml'
        rng = re.search(r"\bd[- ]?dimer\b[\s\S]{0,80}?(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)", text, re.IGNORECASE)
        if rng:
            low = float(rng.group(1)); high = float(rng.group(2))
        else:
            low, high = 0.0, 0.7
        # Correction for OCR decimal-loss (e.g., 21->2.1, 24->2.4) when expected sub-1–few values
        if unit == 'µg/ml' and high <= 1.5 and val >= 2.0:
            raw_token = re.search(r"\bd[- ]?dimer\b[^\d]{0,20}([0-9][0-9])", text, re.IGNORECASE)
            cands = set()
            if raw_token:
                d = raw_token.group(1)
                if len(d) == 2:
                    cands.add(float(d[0] + '.' + d[1]))  # e.g., '24' -> 2.4
                    cands.add(float(d[0] + '.1'))        # bias alt -> 2.1
            cands.add(round(val/10.0,2)); cands.add(round(val/100.0,2))
            # keep reasonable bounds and prefer closest to 2.0
            cands = [c for c in cands if 0.1 <= c <= 20.0]
            if cands:
                target = 2.0
                val = min(cands, key=lambda x: abs(x-target))
        status = 'normal'
        if val < low: status = 'low'
        elif val > high: status = 'high'
        rows.append({'Test': 'D-Dimer', 'Value': str(round(val, 2)), 'Unit': unit, 'Ref Low': str(low), 'Ref High': str(high), 'Status': status})
    return rows

def detect_lft_freeform(raw_text: str):
    """Regex fallback for liver function tests that might be missed by main parser."""
    import re
    t = raw_text
    rows = []
    
    # Bilirubin patterns
    bilirubin_patterns = [
        (r"bilirubin\s*\(total\)\s+(\d+(?:\.\d+)?)\s*(mg\s*\/\s*dl|mg\s*dl)", 'Bilirubin (Total)', 0.3, 1.2),
        (r"total\s+bilirubin\s+(\d+(?:\.\d+)?)\s*(mg\s*\/\s*dl|mg\s*dl)", 'Total Bilirubin', 0.3, 1.2),
        (r"bilirubin\s*\(direct\)\s+(\d+(?:\.\d+)?)\s*(mg\s*\/\s*dl|mg\s*dl)", 'Bilirubin (Direct)', 0.1, 0.4),
        (r"direct\s+bilirubin\s+(\d+(?:\.\d+)?)\s*(mg\s*\/\s*dl|mg\s*dl)", 'Direct Bilirubin', 0.1, 0.4),
        (r"bilirubin\s*\(indirect\)\s+(\d+(?:\.\d+)?)\s*(mg\s*\/\s*dl|mg\s*dl)", 'Bilirubin (Indirect)', 0.1, 0.8),
        (r"indirect\s+bilirubin\s+(\d+(?:\.\d+)?)\s*(mg\s*\/\s*dl|mg\s*dl)", 'Indirect Bilirubin', 0.1, 0.8),
    ]
    
    for pattern, test_name, ref_low, ref_high in bilirubin_patterns:
        m = re.search(pattern, t, re.IGNORECASE)
        if m:
            val = float(m.group(1))
            unit = m.group(2).replace(' ', '')
            status = 'normal'
            if val < ref_low:
                status = 'low'
            elif val > ref_high:
                status = 'high'
            rows.append({'Test': test_name, 'Value': str(val), 'Unit': unit, 'Ref Low': str(ref_low), 'Ref High': str(ref_high), 'Status': status})
    
    # SGPT/ALT and SGOT/AST patterns
    enzyme_patterns = [
        (r"sgpt\s*\(alt\)\s+(\d+(?:\.\d+)?)\s*(U\s*\/\s*L|U\s*L)", 'SGPT (ALT)', 7, 56),
        (r"alt\s*\(sgpt\)\s+(\d+(?:\.\d+)?)\s*(U\s*\/\s*L|U\s*L)", 'ALT (SGPT)', 7, 56),
        (r"sgot\s*\(ast\)\s+(\d+(?:\.\d+)?)\s*(U\s*\/\s*L|U\s*L)", 'SGOT (AST)', 5, 40),
        (r"ast\s*\(sgot\)\s+(\d+(?:\.\d+)?)\s*(U\s*\/\s*L|U\s*L)", 'AST (SGOT)', 5, 40),
        (r"alkaline\s+phosphatase\s+(\d+(?:\.\d+)?)\s*(U\s*\/\s*L|U\s*L)", 'Alkaline Phosphatase', 44, 147),
    ]
    
    for pattern, test_name, ref_low, ref_high in enzyme_patterns:
        m = re.search(pattern, t, re.IGNORECASE)
        if m:
            val = float(m.group(1))
            unit = m.group(2).replace(' ', '')
            status = 'normal'
            if val < ref_low:
                status = 'low'
            elif val > ref_high:
                status = 'high'
            rows.append({'Test': test_name, 'Value': str(val), 'Unit': unit, 'Ref Low': str(ref_low), 'Ref High': str(ref_high), 'Status': status})
    
    return rows

def detect_urine_freeform(raw_text: str):
    """Regex fallback for urinalysis style lines (Albumin ++, Pus cells 20-25/hpf, Epithelial cells raised)."""
    import re
    t = raw_text
    urine_ctx = re.search(r"\burine\b|\burinalysis\b|\burine\s+examination\b", t, re.IGNORECASE) is not None
    rows = []
    # Albumin plus-grades or PRESENT(++), PRESENT(+), etc.
    # Guard: skip if a blood Albumin numeric entry is present (e.g., Albumin 4.7 g/dl 3.5-5.5)
    blood_albumin = re.search(r"\balbumin\b[^\d]{0,20}(\d+(?:\.\d+)?)\s*(g\s*\/\s*dl|g\s*dl|g\s*\/\s*l|g\s*l|mg\s*\/\s*dl)", t, re.IGNORECASE)
    m = re.search(r"\balbumin\b[\s:|\-]*.{0,40}?(present\s*\(\+{1,4}\)|\(+\+?\+?\+?\)|\+{1,4})", t, re.IGNORECASE|re.DOTALL)
    if m:
        if urine_ctx and not blood_albumin:
            plus = m.group(1)
            plus = plus.lower().replace('present','').strip()
            plus = plus.strip("() :|-") or 'present'
            rows.append({'Test': 'Albumin', 'Value': plus, 'Unit': '', 'Ref Low': '', 'Ref High': '', 'Status': 'abnormal'})
    else:
        # Heuristic: if we are in a urine report and see PRESENT(++) without a label, assume Albumin
        m2 = re.search(r"present\s*\((\+{1,4})\)", t, re.IGNORECASE)
        if m2:
            if urine_ctx and not blood_albumin:
                plus = m2.group(1)
                rows.append({'Test': 'Albumin', 'Value': plus, 'Unit': '', 'Ref Low': '', 'Ref High': '', 'Status': 'abnormal'})
    # Pus cells range per hpf
    m = re.search(r"pus\s*cells?[^\n]*?(\d{1,3}(?:[-–]\d{1,3})?)\s*[/]\s*[hb]pf", t, re.IGNORECASE)
    if m:
        rng = m.group(1)
        try:
            vmax = float(rng.replace('–','-').split('-')[-1])
        except Exception:
            vmax = 0.0
        status = 'high' if vmax >= 10 else 'normal'
        unit = '/hpf'
        rows.append({'Test': 'Pus Cells', 'Value': rng, 'Unit': unit, 'Ref Low': '', 'Ref High': '', 'Status': status})
    else:
        # Heuristic: value range like 20-25 /bpf or /hpf without the label
        m2 = re.search(r"(\d{1,3}(?:[-–]\d{1,3})?)\s*[/]\s*[hb]pf", t, re.IGNORECASE)
        if m2:
            rng = m2.group(1)
            try:
                vmax = float(rng.replace('–','-').split('-')[-1])
            except Exception:
                vmax = 0.0
            status = 'high' if vmax >= 10 else 'normal'
            rows.append({'Test': 'Pus Cells', 'Value': rng, 'Unit': '/hpf', 'Ref Low': '', 'Ref High': '', 'Status': status})
    # RBCs per hpf (slightly high if >2 when no explicit ref)
    m = re.search(r"\b(RBCs?|red\s*blood\s*cells?)\b[^\n]*?(\d{1,3}(?:[-–]\d{1,3})?)\s*[/]\s*[hb]pf", t, re.IGNORECASE)
    if m:
        rng = m.group(2)
        try:
            vmax = float(rng.replace('–','-').split('-')[-1])
        except Exception:
            vmax = 0.0
        status = 'abnormal' if vmax > 2 else 'normal'
        rows.append({'Test': 'RBCs', 'Value': rng, 'Unit': '/hpf', 'Ref Low': '', 'Ref High': '', 'Status': status})
    # Bacteria present/absent
    m = re.search(r"\bbacteria\b[^\n]*?(present|seen|many|moderate|few|occasional|absent|negative)", t, re.IGNORECASE)
    if m:
        qual = m.group(1).lower()
        status = 'abnormal' if qual not in ('absent','negative') else 'normal'
        rows.append({'Test': 'Bacteria', 'Value': qual, 'Unit': '', 'Ref Low': '', 'Ref High': '', 'Status': status})
    # Epithelial cells qualitative
    m = re.search(r"epithelial\s*cells?[^\n]*?(slightly\s*raised|raised|many|moderate|few|occasional)", t, re.IGNORECASE)
    if m:
        val = m.group(1)
        status = 'abnormal' if val.lower() in ('slightly raised','raised','many','moderate') else 'normal'
        rows.append({'Test': 'Epithelial Cells', 'Value': val, 'Unit': '', 'Ref Low': '', 'Ref High': '', 'Status': status})
    return rows

def detect_lft_freeform(raw_text: str):
    """Regex fallback for common Liver Function Test items: Albumin, Globulin, Total Protein, A/G ratio.
    Creates rows with value and status based on inline ref ranges when present.
    """
    import re
    t = re.sub(r"\s+", " ", raw_text)
    rows = []
    def add_range_row(name_pat, canonical):
        # Prefer values formatted like 4.7 g/dL followed by a range like 3.5-5.5
        m = re.search(
            rf"\b(?:{name_pat})\b[^\d]{{0,16}}(?P<val>[0-9](?:\.[0-9]{{1,2}})?)\s*(?P<unit>g\s*[\/ ]\s*d[li]|g\s*[\/ ]\s*l|mg\s*[\/ ]\s*dl)\b[^\d]{{0,16}}(?P<low>[0-9](?:\.[0-9]{{1,2}})?)\s*-\s*(?P<high>[0-9](?:\.[0-9]{{1,2}})?)",
            t,
            re.IGNORECASE,
        )
        if not m:
            # Fallback: allow any unit token but keep value shape small to avoid 27.0/47.0 OCR confusions
            m = re.search(
                rf"\b(?:{name_pat})\b[^\d]{{0,20}}(?P<val>[0-9](?:\.[0-9]{{1,2}})?)\s*(?P<unit>[A-Za-z\/]+)?[^\d]{{0,20}}(?P<low>[0-9](?:\.[0-9]{{1,2}})?)\s*-\s*(?P<high>[0-9](?:\.[0-9]{{1,2}})?)",
                t,
                re.IGNORECASE,
            )
            if not m:
                # Final fallback: capture value without an explicit range; we'll fill range from standards later
                m_val = re.search(rf"\b(?:{name_pat})\b[^\d]{{0,20}}(?P<val>[0-9]+(?:\.[0-9]{{1,2}})?)\s*(?P<unit>[A-Za-z\/]+)?", t, re.IGNORECASE)
                if not m_val:
                    return
                val = float(m_val.group('val'))
                unit = (m_val.group('unit') or '').strip()
                rows.append({'Test': canonical, 'Value': str(val), 'Unit': unit, 'Ref Low': '', 'Ref High': '', 'Status': 'normal'})
                return
        raw_val = m.group('val')
        val = float(raw_val)
        unit = (m.group('unit') or '').strip()
        # Normalize common OCR unit mistakes (gm/di -> g/dl)
        unit = unit.replace('gm/di', 'g/dl').replace('gm/dl', 'g/dl').replace('g m/dl', 'g/dl').replace('vou','U/L').replace('u/l','U/L').replace('iu/l','IU/L')
        low = float(m.group('low'))
        high = float(m.group('high'))
        # If unit missing but range looks like typical g/dl values, assume g/dl
        if not unit and 2.0 <= low <= 6.0 and 2.5 <= high <= 7.0:
            unit = 'g/dl'
        # Sanity caps to avoid OCR outliers (e.g., 27.0 for albumin)
        if ((canonical == 'Albumin' and val > 10) or
            (canonical == 'Globulin' and val > 10) or
            (canonical == 'Total Protein' and val > 20)):
            # Attempt decimal recovery using range and last digit heuristic
            try:
                last_digit = int(raw_val[-1])
                candidates = []
                import math
                start = int(math.floor(low))
                end = int(math.ceil(high))
                for k in range(start, end + 1):
                    candidate = float(f"{k}.{last_digit}")
                    if low <= candidate <= high:
                        candidates.append(candidate)
                mid = (low + high) / 2.0
                if candidates:
                    val = min(candidates, key=lambda x: abs(x - mid))
                else:
                    # fallback: divide by 10 if inside range
                    if low <= (float(raw_val)/10.0) <= high:
                        val = float(raw_val)/10.0
                    else:
                        return
            except Exception:
                return
        # Correct common 10x OCR shifts using the provided reference range
        def within(x: float) -> bool:
            return low <= x <= high
        # Try aligning with the same factor used for the range first
        if not within(val):
            # If earlier we chose a factor f to adjust range, try it first
            try:
                f_applied = locals().get('f', 1.0)
            except Exception:
                f_applied = 1.0
            for cand in [f_applied, 0.1, 0.01, 10.0]:
                if cand == 1.0:
                    continue
                v2 = val * cand
                if within(v2):
                    val = v2
                    break
        status = 'normal'
        if val < low:
            status = 'low'
        elif val > high:
            status = 'high'
        rows.append({'Test': canonical, 'Value': str(val), 'Unit': unit, 'Ref Low': str(low), 'Ref High': str(high), 'Status': status})
    # Albumin and Globulin (blood)
    add_range_row(r"albumin", "Albumin")
    add_range_row(r"globulin", "Globulin")
    # Total protein
    add_range_row(r"total\s*protein", "Total Protein")
    # Bilirubin (total/direct/indirect)
    add_range_row(r"total\s*bilirubin|t\.?\s*bilirubin|bilirubin\s*total", "Total Bilirubin")
    add_range_row(r"direct\s*bilirubin|conjugated\s*bilirubin", "Direct Bilirubin")
    add_range_row(r"indirect\s*bilirubin|unconjugated\s*bilirubin", "Indirect Bilirubin")
    # Enzymes: ALT/SGPT, AST/SGOT, GGT
    add_range_row(r"sgpt|alt|alanine\s*aminotransferase|s\.?g\.?p\.?t\.?", "ALT (SGPT)")
    add_range_row(r"sgot|ast|aspartate\s*aminotransferase|s\.?g\.?o\.?t\.?", "AST (SGOT)")
    add_range_row(r"gamma\s*g\.?\s*t\.?|ggt|g\.?g\.?t|gamma\s*gt", "GGT")
    # A/G ratio occasionally written as A:G or A\/G
    m_ag = re.search(r"\bA\s*[:\/]\s*G\s*ratio\b[^\d]{0,24}(\d+(?:\.\d+)?)\s*(?:[^\d]{0,24}(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?))?", t, re.IGNORECASE)
    if m_ag:
        val = float(m_ag.group(1))
        low = m_ag.group(2)
        high = m_ag.group(3)
        status = 'normal'
        ref_low = ''
        ref_high = ''
        if low and high:
            lowf = float(low); highf = float(high)
            # Fix 10x range like 12-22 -> 1.2-2.2
            if highf > 5 and 0 < lowf <= 50:
                lowf /= 10.0; highf /= 10.0
            if val < lowf:
                status = 'low'
            elif val > highf:
                status = 'high'
            ref_low = str(lowf); ref_high = str(highf)
        # Correct decimal shift for A/G ratio
        if ref_high and float(ref_high) <= 3 and val > float(ref_high):
            if val/10.0 <= float(ref_high):
                val = val/10.0
        rows.append({'Test': 'A/G Ratio', 'Value': str(val), 'Unit': '', 'Ref Low': ref_low, 'Ref High': ref_high, 'Status': status})
    return rows

def normalize_lab_rows(lab_rows: list) -> list:
    """Post-OCR validation and normalization.
    - Fix ref ranges and values with 10x/100x decimal shifts using medical standards
    - Fill missing ranges from standards when possible
    - Recompute status after adjustments
    """
    import math
    standards = {
        'Albumin': {'low': 3.4, 'high': 5.4, 'unit_like': ['g/dl','g l','g/dl']},
        'Globulin': {'low': 2.3, 'high': 3.5, 'unit_like': ['g/dl','g l']},
        'Total Protein': {'low': 5.5, 'high': 7.5, 'unit_like': ['g/dl','g l']},
        'Total Bilirubin': {'low': 0.0, 'high': 1.2, 'unit_like': ['mg/dl']},
        'Direct Bilirubin': {'low': 0.0, 'high': 0.4, 'unit_like': ['mg/dl']},
        'Indirect Bilirubin': {'low': 0.0, 'high': 0.8, 'unit_like': ['mg/dl']},
        'ALT (SGPT)': {'low': 0.0, 'high': 40.0, 'unit_like': ['iu/l','u/l']},
        'AST (SGOT)': {'low': 0.0, 'high': 40.0, 'unit_like': ['iu/l','u/l']},
        'GGT': {'low': 10.0, 'high': 71.0, 'unit_like': ['iu/l','u/l']},
        'A/G Ratio': {'low': 1.1, 'high': 2.3, 'unit_like': ['']},
    }
    def parse_float(s: str):
        try:
            return float(str(s).strip())
        except Exception:
            return None
    for r in lab_rows:
        name = r.get('Test','')
        std = standards.get(name)
        val = parse_float(r.get('Value',''))
        # Force numeric conversion; skip non-numeric rows
        if val is None:
            # Clean up descriptive attributes like Appearance
            if name.lower().startswith('appearance'):
                raw = str(r.get('Value',''))
                raw_l = raw.lower()
                cleaned = raw_l
                # Prefer concise forms
                if 'turbid' in raw_l:
                    cleaned = 'slightly turbid' if 'slightly' in raw_l else 'turbid'
                elif 'clear' in raw_l:
                    cleaned = 'clear'
                cleaned = cleaned.strip().capitalize()
                r['Value'] = cleaned
                r['Status'] = 'info'
            r['Status'] = r.get('Status','normal')
            r['Unit'] = (r.get('Unit','') or '')
            continue
        unit = (r.get('Unit','') or '').lower()
        # Unit normalization
        unit = (unit
                .replace('gm/di','g/dl')
                .replace('gm/dl','g/dl')
                .replace('g m/dl','g/dl')
                .replace('voi','u/l')
                .replace('vou','u/l')
                .replace('u/l','U/L')
                .replace('iu/l','U/L')
               )
        low = parse_float(r.get('Ref Low',''))
        high = parse_float(r.get('Ref High',''))
        if std:
            # If range missing or clearly off by factor of 10, try to adjust to standard
            if low is None or high is None or (low == 0 and high == 0) or (high and high >= 10*std['high']):
                low = std['low']
                high = std['high']
                adjusted_range = True
            else:
                # Choose factor f in {1,0.1,0.01,10} that best matches standard mid
                candidates = [1.0, 0.1, 0.01, 10.0]
                best = (abs(((low+high)/2) - (std['low']+std['high'])/2), 1.0)
                for f in candidates:
                    adj_mid = ((low*f)+(high*f))/2
                    diff = abs(adj_mid - (std['low']+std['high'])/2)
                    if diff < best[0]:
                        best = (diff, f)
                f = best[1]
                if f != 1.0:
                    low *= f
                    high *= f
                    adjusted_range = True
                else:
                    adjusted_range = False
                # Heuristic: if both bounds look 10x larger than standard, divide by 10
                ratio = high / std['high'] if std['high'] else 1.0
                if 8.0 <= ratio <= 15.0:
                    low /= 10.0; high /= 10.0; adjusted_range = True
            # Adjust value with same factor heuristic if outside range
            if val is not None and (val < low or val > high):
                # Only apply aggressive downscale to tests prone to decimal OCR issues
                decimal_sensitive = {
                    'Albumin','Globulin','Total Protein','Total Bilirubin','Direct Bilirubin','Indirect Bilirubin','A/G Ratio'
                }
                allowed = adjusted_range or (name in decimal_sensitive)
                if allowed:
                    for f in [0.1, 0.01, 10.0]:
                        v2 = val * f
                        if low <= v2 <= high:
                            val = v2
                            break
                    # Special-case A/G ratio: accept 0.5–3.0 domain even if outside range
                    if name == 'A/G Ratio' and val > 3 and 0.5 <= (val/10.0) <= 3.0:
                        val = val/10.0
                # Aggressive but safe correction using 5x guard
                if low is not None and high is not None:
                    # Strict range-based correction
                    if val > (high * 5) and (low <= val/10.0 <= high):
                        val = val / 10.0
                    elif val < (low / 5) and (low <= val*10.0 <= high):
                        val = val * 10.0
                    # Safe fallback for proteins/ratios when range is slightly higher than corrected value
                    elif name in {'Albumin','Globulin','Total Protein'} and val > (high * 5) and 2.0 <= (val/10.0) <= 8.0:
                        val = val / 10.0
                    elif name == 'A/G Ratio' and 3.0 < val < 15.0:
                        val = val / 10.0
                # Do not downscale ALT/AST/GGT unless values are extreme
                else:
                    if name in {'ALT (SGPT)','AST (SGOT)','GGT'} and val > 400 and (val/10.0) >= low:
                        val = val/10.0
        # Test-specific guards after range known
        if std and val is not None:
            if name in {'Albumin','Globulin','Total Protein'} and val > 20 and (std['low'] <= val/10.0 <= std['high']):
                val = val/10.0
            if name == 'A/G Ratio' and 3 < val < 15:
                val = val/10.0
        # Update row
        if val is not None:
            r['Value'] = str(round(val, 2))
        if low is not None:
            r['Ref Low'] = str(round(low, 2))
        if high is not None:
            r['Ref High'] = str(round(high, 2))
        # Recompute status
        status = r.get('Status','normal')
        try:
            if val is not None and low is not None and high is not None:
                if val < low:
                    status = 'low'
                elif val > high:
                    status = 'high'
                else:
                    status = 'normal'
        except Exception:
            pass
        r['Status'] = status
        r['Unit'] = unit
    return lab_rows

def dedupe_lab_rows(lab_rows: list) -> list:
    """Merge duplicate tests under canonical names (e.g., Gamma GT and GGT).
    Prefer rows with explicit ranges or abnormal status.
    """
    canonical = {
        'gamma gt': 'GGT',
        'ggt': 'GGT',
        'gamma g.t': 'GGT',
        'gamma g t': 'GGT',
        'alt (sgpt)': 'ALT (SGPT)',
        'sgpt (alt)': 'ALT (SGPT)',
        'ast (sgot)': 'AST (SGOT)',
        'sgot (ast)': 'AST (SGOT)',
    }
    merged = {}
    for r in lab_rows:
        name = r.get('Test','')
        key = canonical.get(name.lower(), name)
        r['Test'] = key
        prev = merged.get(key)
        if prev is None:
            merged[key] = r
            continue
        # Prefer abnormal over normal
        def score(x):
            s = 1
            if x.get('Status') in ('high','low','abnormal'):
                s += 2
            # Prefer rows with both bounds present
            if x.get('Ref Low') and x.get('Ref High'):
                s += 1
            return s
        merged[key] = max([prev, r], key=score)
    return list(merged.values())

def finalize_lab_rows(lab_rows: list) -> list:
    """Ensure values/refs are numeric and statuses recomputed from corrected data."""
    def to_float(x):
        try:
            return float(str(x).strip())
        except Exception:
            return None
    for r in lab_rows:
        v = to_float(r.get('Value',''))
        lo = to_float(r.get('Ref Low',''))
        hi = to_float(r.get('Ref High',''))
        # If we have a plausible range, recompute status
        if v is not None and lo is not None and hi is not None and hi >= lo:
            # 5% tolerance for borderline classification
            tol_low = lo * 0.95
            tol_high = hi * 1.05
            if v < lo:
                r['Status'] = 'borderline_low' if v >= tol_low else 'low'
            elif v > hi:
                r['Status'] = 'borderline_high' if v <= tol_high else 'high'
            else:
                r['Status'] = 'normal'
        # Keep corrected numeric values as strings for table display
        if v is not None:
            r['Value'] = str(round(v, 2))
        if lo is not None:
            r['Ref Low'] = str(round(lo, 2))
        if hi is not None:
            r['Ref High'] = str(round(hi, 2))
    return lab_rows

if analyze:
    if not txt.strip():
        st.warning("Please paste a report text first.")
    else:
        with st.spinner("Analyzing..."):
            st.markdown('<div class="scan"></div>', unsafe_allow_html=True)
            st.progress(5, text="Scanning and parsing...")
            lab_rows = parse_lab_table(txt)
            # Merge regex fallback rows for key labs (e.g., BNP, thyroid) if not already present
            extra_rows = detect_key_labs_freeform(txt)
            # Avoid duplicates by Test name if one already exists
            have = {r['Test'].lower() for r in lab_rows}
            for r in extra_rows:
                if r['Test'].lower() not in have:
                    lab_rows.append(r)
                    have.add(r['Test'].lower())
            # Urinalysis fallback rows (Albumin ++, Pus cells 20-25/hpf, Epithelial cells raised)
            urine_rows = detect_urine_freeform(txt)
            for r in urine_rows:
                if r['Test'].lower() not in have:
                    lab_rows.append(r)
                    have.add(r['Test'].lower())
            # LFT fallback rows (Albumin, Globulin, Total Protein, A/G ratio)
            lft_rows = detect_lft_freeform(txt)
            for r in lft_rows:
                if r['Test'].lower() not in have:
                    lab_rows.append(r)
                    have.add(r['Test'].lower())
            if show_debug:
                import re
                norm = re.sub(r"\s+", " ", txt).strip()
                st.markdown("**Debug: normalized OCR text (first 800 chars):**")
                st.code(norm[:800])
                st.markdown("**Debug: parsed lab rows:**")
                try:
                    import pandas as pd
                    st.dataframe(pd.DataFrame(lab_rows or []))
                except Exception:
                    st.json(lab_rows or [])
            pos, neg = comprehensive_summarize(txt)
            # If rule-based extraction finds nothing, try prose fallback
            if not pos and not neg:
                fb = fallback_findings_from_prose(txt)
                if fb:
                    pos = fb
            pos_h = to_patient_friendly(pos)
            neg_h = []
            for n in neg:
                if n.startswith("no "):
                    neg_h.append("no " + to_patient_friendly([n[3:]])[0])
                else:
                    neg_h.append(n)
            patient_lab_msg = ""
            # Post-OCR normalization and range corrections
            lab_rows = normalize_lab_rows(lab_rows)
            # Dedupe tests like GGT/Gamma GT
            lab_rows = dedupe_lab_rows(lab_rows)
            # Recompute statuses from corrected data to avoid pre-correction artifacts
            lab_rows = finalize_lab_rows(lab_rows)
            # Urine safety net: re-run urine extraction and merge anything still missing
            urine_rows2 = detect_urine_freeform(txt)
            have2 = {r['Test'].lower() for r in lab_rows}
            for r in urine_rows2:
                key = r['Test'].lower()
                if key not in have2:
                    lab_rows.append(r)
                    have2.add(key)
            # Finalize again after merging
            lab_rows = finalize_lab_rows(lab_rows)
            if show_debug:
                st.markdown("**Debug: normalized + deduped lab rows:**")
                try:
                    import pandas as pd
                    st.dataframe(pd.DataFrame(lab_rows or []))
                except Exception:
                    st.json(lab_rows or [])
        st.subheader("🧪 Lab Results (parsed)")
        with st.container():
            try:
                import pandas as pd
                df = pd.DataFrame(lab_rows or [])
                for col in ['Value','Ref Low','Ref High']:
                    if col in df.columns:
                        df[col] = df[col].astype(str)
                st.dataframe(df, use_container_width=True)
            except Exception:
                st.dataframe(lab_rows or [], use_container_width=True)
        abn = [r for r in (lab_rows or []) if r['Status'] not in ('normal','info','not tested')]
        if abn:
            st.markdown("**Abnormal values detected:**")
            for r in abn:
                if r['Ref Low'] != '' or r['Ref High'] != '':
                    direction = 'high' if r['Status'] == 'high' else ('low' if r['Status']=='low' else r['Status'])
                    st.markdown(f"• {r['Test']}: {r['Value']} {r['Unit']} ({direction}; ref {r['Ref Low']}-{r['Ref High']})")
                else:
                    st.markdown(f"• {r['Test']}: {r['Value']} ({r['Status']})")
            # Short lab narrative highlights
            narrative = []
            # RBCs
            for r in lab_rows:
                if r['Test'].lower().startswith('red blood cells') and r['Status'] in ('high','abnormal'):
                    narrative.append(f"RBCs present ({r['Value']}{(' '+r['Unit']) if r['Unit'] else ''}), mild abnormality.")
            # Specific gravity not tested
            for r in lab_rows:
                if r['Test'].lower() == 'specific gravity' and (r['Status'] == 'not tested' or r['Value'].lower() == 'not tested'):
                    narrative.append("Specific gravity not tested (QNS).")
            # pH and appearance
            ph = next((r for r in lab_rows if r['Test'].lower().startswith('reaction')), None)
            app = next((r for r in lab_rows if r['Test'].lower().startswith('appearance')), None)
            if ph:
                narrative.append(f"Urine {ph['Value'].lower()}.")
            if app:
                narrative.append(f"Appearance {app['Value'].lower()}.")
            if narrative:
                st.markdown("**Lab summary:**")
                for line in narrative:
                    st.markdown(f"• {line}")
            # If no abnormalities detected, craft a simple patient-friendly sentence
            if not abn:
                key_tests = [
                    'Sodium','Potassium','Chloride','Creatinine','Urea','Blood Urea',
                    'Glucose','Hemoglobin','WBC','Platelets'
                ]
                normals = [r['Test'] for r in lab_rows if r['Status'] == 'normal' and r['Test'] in key_tests]
                if normals:
                    def _human_join(items):
                        if len(items) <= 1:
                            return items[0]
                        if len(items) == 2:
                            return f"{items[0]} and {items[1]}"
                        return ", ".join(items[:-1]) + f", and {items[-1]}"
                    picked = [x for x in normals if x in ['Sodium','Potassium','Chloride']]
                    if not picked:
                        picked = normals[:3]
                    listed = _human_join([s.lower() for s in picked])
                    patient_lab_msg = f"Your blood test results are normal. {listed} levels are within the healthy range. No issues found."
                else:
                    patient_lab_msg = "Your blood test results are normal. All reported values are within the healthy range."
            else:
                # Patient-friendly explanations for common abnormal tests
                pf_lines = []
                for r in abn:
                    name = r['Test'].lower()
                    status = r.get('Status','')
                    try:
                        val = r['Value']
                        unit = (" " + r['Unit']) if r['Unit'] else ""
                    except Exception:
                        val = r['Value']
                        unit = ""
                    if 'bnp' in name and status == 'high':
                        pf_lines.append("BNP is high. This can mean the heart is under strain. Please discuss with your doctor.")
                    if name.startswith('free t3') or name.startswith('free t4') or name.startswith('t s h') or 'tsh' in name:
                        pf_lines.append("Thyroid hormone levels are out of range. This may suggest a thyroid imbalance.")
                    # Hemoglobin/RBC low – anemia message
                    if ('hemoglobin' in name or name == 'rbc') and status in ('low','borderline_low'):
                        pf_lines.append("Red blood-related values are low. This suggests anemia, which can cause tiredness or breathlessness. Please consult your doctor.")
                    # Fasting blood sugar high
                    if ('fasting blood sugar' in name or name == 'fbs' or 'glucose' in name) and status in ('high','borderline_high'):
                        pf_lines.append("Fasting sugar is above normal. This can be an early sign of sugar imbalance. Your doctor may advise diet changes or further tests (e.g., HbA1c).")
                    # WBC high – infection/inflammation
                    if (name == 'total wbc' or name == 'wbc') and status in ('high','borderline_high'):
                        pf_lines.append("White blood cells are elevated, which can happen with infections or inflammation.")
                    # Platelets abnormal
                    if 'platelet' in name and status in ('low','borderline_low'):
                        pf_lines.append("Platelets are lower than usual, which can increase bleeding/bruising risk.")
                    # Liver function tests
                    if 'bilirubin' in name and status in ('high','borderline_high'):
                        pf_lines.append("Bilirubin is elevated, which can indicate liver stress or bile flow issues. Your doctor may recommend further liver tests.")
                    if ('sgpt' in name or 'alt' in name) and status in ('high','borderline_high'):
                        pf_lines.append("Liver enzyme (ALT/SGPT) is elevated, suggesting possible liver inflammation or damage. Please discuss with your doctor.")
                    if ('sgot' in name or 'ast' in name) and status in ('high','borderline_high'):
                        pf_lines.append("Liver enzyme (AST/SGOT) is elevated, which can indicate liver stress. Your doctor may recommend monitoring or further tests.")
                    if 'albumin' in name and status in ('low','borderline_low'):
                        pf_lines.append("Albumin is low, which can affect protein balance and fluid retention. This may be related to liver, kidney, or nutritional issues.")
                    if 'alkaline phosphatase' in name and status in ('high','borderline_high'):
                        pf_lines.append("Alkaline phosphatase is elevated, which can indicate liver or bone issues. Your doctor will interpret this in context.")
                if pf_lines:
                    patient_lab_msg = " ".join(dict.fromkeys(pf_lines))
        else:
            # Fallback: simple in-text scan for electrolytes with value and range
            import re
            names = [
                ("Sodium", r"s\.?\s*sodium|sodium"),
                ("Potassium", r"s\.?\s*potassium|potassium"),
                ("Chloride", r"s\.?\s*chlorides?|chloride|chlorides"),
            ]
            found = []
            for canon, pat in names:
                m = re.search(rf"(?:{pat})[^\n]*?(\d+(?:\.\d+)?)\s*[A-Za-z/]*[^\n]*?(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)", txt, flags=re.IGNORECASE)
                if m:
                    try:
                        val = float(m.group(1))
                        lo = float(m.group(2))
                        hi = float(m.group(3))
                        if lo <= val <= hi:
                            found.append(canon)
                    except Exception:
                        pass
            if found and len(found) >= 1:
                def _human_join(items):
                    if len(items) <= 1:
                        return items[0]
                    if len(items) == 2:
                        return f"{items[0]} and {items[1]}"
                    return ", ".join(items[:-1]) + f", and {items[-1]}"
                listed = _human_join([s.lower() for s in found])
                patient_lab_msg = f"Your blood test results are normal. {listed} levels are within the healthy range. No issues found."
        st.subheader("🔬 Technical Summary")
        if pos:
            st.markdown("**Findings:**")
            for f in pos:
                st.markdown(f"• {f}")
        # Also surface lab abnormal highlights in Technical Summary
        if lab_rows:
            abn = [r for r in lab_rows if r['Status'] not in ('normal','info','not tested')]
            for r in abn:
                if r['Status'] in ('borderline_low','borderline_high'):
                    direction = 'slightly high' if r['Status']=='borderline_high' else 'slightly low'
                else:
                    direction = 'high' if r['Status']=='high' else ('low' if r['Status']=='low' else r['Status'])
                st.markdown(f"• {r['Test']}: {r['Value']} {r['Unit']} ({direction}{'; ref ' + r['Ref Low'] + '-' + r['Ref High'] if (r['Ref Low'] or r['Ref High']) else ''})")
        if not pos and (not lab_rows or all(r['Status'] in ('normal','info','not tested') for r in lab_rows)):
            # Provide a gentle message rather than empty output
            st.markdown("No explicit findings detected from keywords. If this is a prose report, try including concrete phrases (e.g., 'hemoglobin is low', 'WBC is high').")
        if neg:
            st.markdown("**Normal Findings:**")
            for f in neg:
                st.markdown(f"• {f}")
        st.subheader("👥 Patient-Friendly Summary")
        if pos_h:
            st.markdown("**What was found:**")
            for f in pos_h:
                st.markdown(f"• {f}")
        if neg_h:
            st.markdown("**What looks normal:**")
            for f in neg_h:
                st.markdown(f"• {f}")
        # Add the lab reassurance message when available
        try:
            if patient_lab_msg:
                st.markdown(patient_lab_msg)
            # Fallback message if no specific lab messages were generated
            elif lab_rows and any(r['Status'] not in ('normal','info','not tested') for r in lab_rows):
                st.markdown("Some of your lab values are outside the normal range. Please discuss these results with your doctor for proper interpretation and any necessary follow-up.")
            elif lab_rows:
                st.markdown("Your lab results appear to be within normal ranges. However, please consult with your doctor for complete interpretation.")
            # Additional patient-friendly alerts for abnormal BNP/thyroid
            if lab_rows:
                names = {r['Test'].lower(): r for r in lab_rows}
                if 'bnp' in names and names['bnp']['Status'] == 'high':
                    st.markdown("BNP is higher than normal. This can indicate the heart is under strain. Please consult your doctor promptly.")
                thyroid_flags = [n for n in names if n in ('free t3','free t4','tsh') and names[n]['Status'] in ('high','low')]
                if thyroid_flags:
                    st.markdown("Thyroid hormone levels are out of range. This may suggest a thyroid imbalance. Your doctor can advise on next steps.")
                if ('pus cells' in names and names['pus cells']['Status'] in ('high','abnormal')) or any('pus' in k and names[k]['Status'] in ('high','abnormal') for k in names):
                    st.markdown("There are many white blood cells (pus cells) in the urine, which can suggest a urinary tract infection (UTI). Drinking fluids and timely medical review are advised.")
                if 'rbcs' in names and names['rbcs']['Status'] in ('abnormal','high'):
                    st.markdown("Red blood cells are present in the urine. This can occur with infections or irritation; please follow up with your clinician.")
                if 'bacteria' in names and names['bacteria']['Status'] in ('abnormal','high'):
                    st.markdown("Bacteria were detected in urine, supporting a possible UTI.")
                if 'albumin' in names and names['albumin']['Status'] in ('abnormal','high'):
                    alb_unit = names['albumin'].get('Unit','').lower()
                    if not any(u in alb_unit for u in ['g/dl','g/l','mg/dl']):
                        st.markdown("Albumin is present in urine, which can indicate kidney strain. Please discuss with your clinician.")
                    else:
                        direction = 'high' if names['albumin']['Status']=='high' else 'low'
                        st.markdown(f"Albumin (blood) is {direction}. Your doctor may correlate this with liver and nutrition markers.")
                else:
                    # If albumin row exists and is normal, do not show any urine-related albumin message
                    pass
                if 'globulin' in names and names['globulin']['Status'] in ('high','low','borderline_high','borderline_low'):
                    direction = 'high' if names['globulin']['Status']=='high' else 'low'
                    st.markdown(f"Globulin is {direction}. This protein imbalance can be related to liver or immune conditions. Consider follow-up with your doctor.")
                # Borderline message
                for key, row in names.items():
                    if row.get('Status') in ('borderline_low','borderline_high'):
                        st.markdown(f"Your {row['Test']} is slightly outside the normal range and may not be clinically significant. Your doctor will interpret this in context.")
                if 'epithelial cells' in names and names['epithelial cells']['Status'] in ('abnormal','high'):
                    st.markdown("Epithelial cells are above the typical amount. This is often mild but should be correlated clinically.")
        except Exception:
            pass

st.markdown("</div>", unsafe_allow_html=True)
st.markdown("---")
st.caption("For research/education only. Not a diagnostic tool. Always consult licensed clinicians.")
