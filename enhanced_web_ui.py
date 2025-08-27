#!/usr/bin/env python3
"""
Enhanced Medical Report Summarizer - Web UI
Modern, accessible, and user-friendly interface using Streamlit.
"""

import re
from datetime import datetime
from typing import List, Tuple

import streamlit as st

# Page config
st.set_page_config(
    page_title="Medical Report Summarizer (Enhanced)",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Styles
st.markdown(
    """
<style>
  .main-header { font-size: 2.4rem; font-weight: 800; text-align: center; margin: 0 0 1rem; }
  .sub-header { font-size: 1.2rem; font-weight: 700; color: #2d3748; margin: 0.5rem 0 0.75rem; }
  .finding-box { background: #fff5f5; padding: 1rem; border-radius: 10px; border-left: 6px solid #e53e3e; margin: 0.75rem 0; }
  .normal-box { background: #f0fff4; padding: 1rem; border-radius: 10px; border-left: 6px solid #38a169; margin: 0.75rem 0; }
  .info-box { background: #ebf8ff; padding: 1rem; border-radius: 10px; border-left: 6px solid #3182ce; margin: 0.75rem 0; }
  .stTextArea > div > div > textarea {
    background: #f7fafc; /* light background for readability on dark theme */
    color: #1a202c;      /* dark text color so pasted text is visible */
    caret-color: #1a202c;/* visible caret */
  }
  .status { display: inline-block; padding: 0.3rem 0.6rem; border-radius: 12px; font-size: 0.85rem; font-weight: 600; }
  .status-ok { background:#c6f6d5; color:#22543d; }
  .status-attn { background:#fff3cd; color:#744210; }
</style>
""",
    unsafe_allow_html=True,
)

# Session state
if "prefs" not in st.session_state:
    st.session_state.prefs = {
        "show_technical": True,
        "show_patient": True,
        "save_history": True,
        "auto_analyze": False,
    }
if "history" not in st.session_state:
    st.session_state.history = []

# Core logic

def _set_report_text(value: str = "") -> None:
    """Helper to set report_text in session_state before text area renders."""
    st.session_state["report_text"] = value

def comprehensive_summarize(text: str) -> Tuple[List[str], List[str]]:
    text_lower = text.lower()
    # Keep only specific, clinically meaningful terms to reduce false matches
    findings = {
        "cardiomegaly": "cardiomegaly",
        "pneumonia": "pneumonia",
        "consolidation": "consolidation",
        "atelectasis": "atelectasis",
        # be specific about effusion types to avoid false matches
        "pleural effusion": "pleural effusion",
        "pericardial effusion": "pericardial effusion",
        "pneumothorax": "pneumothorax",
        "edema": "pulmonary edema",
        "hepatomegaly": "hepatomegaly",
        "fatty infiltration": "fatty infiltration",
        "gallstones": "gallstones",
        "pericholecystic": "pericholecystic fluid",
        "wall thickening": "wall thickening",
        # cardiac muscle thickening
        "left ventricular hypertrophy": "left ventricular hypertrophy",
        "ventricular hypertrophy": "ventricular hypertrophy",
        "splenomegaly": "splenomegaly",
        # localised non-pleural fluid
        "perisplenic fluid": "perisplenic fluid",
        "cortical cysts": "cortical cysts",
        "hydronephrosis": "hydronephrosis",
        "peripancreatic": "peripancreatic fluid",
        "ectasia": "ectasia",
        "aneurysm": "aneurysm",
        "ascites": "ascites",
        "degenerative": "degenerative changes",
        "fracture": "fracture",
        "lymphadenopathy": "lymphadenopathy",
        "bowel obstruction": "bowel obstruction",
        "free air": "free air",
        "ground-glass": "ground-glass opacities",
    }

    # Negation patterns scoped to a term (avoids sentence-wide negation)
    neg_scoped_patterns = [
        r"\bno\s+(?:evidence\s+of\s+)?{term}\b",
        r"\bwithout\s+{term}\b",
        r"\babsent\s+{term}\b",
        r"\bfree\s+of\s+{term}\b",
        r"\b{term}\s+(?:is|are)?\s*not\s+(?:seen|present|identified)\b",
        r"\bnegative\s+for\s+{term}\b",
    ]

    def is_term_negated(sentence: str, term: str) -> bool:
        escaped = re.escape(term)
        for pat in neg_scoped_patterns:
            if re.search(pat.format(term=escaped), sentence, flags=re.IGNORECASE):
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
                if is_term_negated(s, term):
                    neg.append(f"no {label}")
                else:
                    pos.append(label)

    # Remove duplicates while preserving order
    pos = list(dict.fromkeys(pos))
    neg = list(dict.fromkeys(neg))
    return pos, neg


def patient_friendly_summary(pos: List[str], neg: List[str]) -> Tuple[List[str], List[str]]:
    mapping = {
        "cardiomegaly": "enlarged heart",
        "pneumonia": "lung infection",
        "consolidation": "areas of lung tissue that appear solid",
        "atelectasis": "partial collapse of small lung areas",
        "pleural effusion": "fluid around the lungs",
        "pericardial effusion": "fluid around the heart",
        "pneumothorax": "collapsed lung",
        "pulmonary edema": "excess fluid in lung tissue",
        "left ventricular hypertrophy": "thickened muscle of the left lower heart chamber",
        "ventricular hypertrophy": "thickened heart muscle",
        "hepatomegaly": "enlarged liver",
        "fatty infiltration": "fat deposits in the liver",
        "gallstones": "stones in the gallbladder",
        "pericholecystic fluid": "fluid around the gallbladder",
        "wall thickening": "thickened walls",
        "splenomegaly": "enlarged spleen",
        "renal findings": "kidney changes",
        "cortical cysts": "small fluid-filled sacs in the kidneys",
        "hydronephrosis": "kidney swelling from urine backup",
        "peripancreatic fluid": "fluid around the pancreas",
        "perisplenic fluid": "small amount of fluid near the spleen",
        "aortic findings": "changes in the main blood vessel",
        "ectasia": "widening of a blood vessel",
        "aneurysm": "ballooning of a blood vessel",
        "ascites": "fluid in the belly",
        "degenerative changes": "wear-and-tear changes",
        "fracture": "broken bone",
        "lymphadenopathy": "enlarged lymph nodes",
        "bowel obstruction": "blockage in the intestines",
        "free air": "air leak in the belly",
        "ground-glass opacities": "hazy lung areas",
    }
    pos_h = [mapping.get(x, x) for x in pos]
    neg_h = []
    for x in neg:
        if x.startswith("no "):
            term = x[3:]
            neg_h.append("no " + mapping.get(term, term))
        else:
            neg_h.append(x)
    return pos_h, neg_h


def validate(text: str) -> Tuple[bool, str]:
    if not text.strip():
        return False, "Please enter a medical report to analyze."
    if len(text.strip()) < 10:
        return False, "Please enter a bit more detail (≥ 10 characters)."
    if len(text) > 10000:
        return False, "Report too long (max 10,000 characters)."
    return True, ""


def analyze_and_render(report_text: str) -> None:
    ok, msg = validate(report_text)
    if not ok:
        st.error(msg)
        return
    with st.spinner("Analyzing report..."):
        pos, neg = comprehensive_summarize(report_text)
        pos_h, neg_h = patient_friendly_summary(pos, neg)
    if st.session_state.prefs["save_history"]:
        st.session_state.history.append({
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "preview": (report_text[:100] + "...") if len(report_text) > 100 else report_text,
            "pos": pos,
            "neg": neg,
        })
        st.session_state.history = st.session_state.history[-10:]

    st.markdown("---")
    st.markdown('<div class="sub-header">📊 Analysis Results</div>', unsafe_allow_html=True)
    st.write(
        f"Status: <span class='status {'status-attn' if pos else 'status-ok'}'>{'Findings detected' if pos else 'No significant findings'}</span>",
        unsafe_allow_html=True,
    )

    if st.session_state.prefs["show_technical"]:
        st.markdown('<div class="sub-header">🔬 Technical Summary</div>', unsafe_allow_html=True)
        if pos:
            st.markdown('<div class="finding-box">', unsafe_allow_html=True)
            for f in pos:
                st.markdown(f"• {f}")
            st.markdown('</div>', unsafe_allow_html=True)
        if neg:
            st.markdown('<div class="normal-box">', unsafe_allow_html=True)
            st.markdown("**Normal Findings:**")
            for f in neg:
                st.markdown(f"• {f}")
            st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.prefs["show_patient"]:
        st.markdown('<div class="sub-header">👥 Patient-Friendly Summary</div>', unsafe_allow_html=True)
        if pos_h:
            st.markdown('<div class="finding-box">', unsafe_allow_html=True)
            st.markdown("**What was found:**")
            for f in pos_h:
                st.markdown(f"• {f}")
            st.markdown('</div>', unsafe_allow_html=True)
        if neg_h:
            st.markdown('<div class="normal-box">', unsafe_allow_html=True)
            st.markdown("**What looks normal:**")
            for f in neg_h:
                st.markdown(f"• {f}")
            st.markdown('</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    c1.metric("Total findings", len(pos))
    c2.metric("Normal results", len(neg))
    c3.metric("Timestamp", datetime.now().strftime("%H:%M:%S"))


def main():
    st.markdown('<div class="main-header">🏥 Medical Report Summarizer</div>', unsafe_allow_html=True)

    with st.sidebar:
        st.header("Settings")
        st.session_state.prefs["show_technical"] = st.checkbox(
            "Show technical summary", st.session_state.prefs["show_technical"]
        )
        st.session_state.prefs["show_patient"] = st.checkbox(
            "Show patient-friendly summary", st.session_state.prefs["show_patient"]
        )
        st.session_state.prefs["auto_analyze"] = st.checkbox(
            "Auto-analyze on input", st.session_state.prefs["auto_analyze"]
        )
        st.session_state.prefs["save_history"] = st.checkbox(
            "Save analysis history", st.session_state.prefs["save_history"]
        )

        st.markdown("---")
        st.subheader("How to use")
        st.caption(
            "Paste your report, click Analyze. Works for radiology, labs, notes."
        )

        if st.session_state.history:
            st.subheader("Recent analyses")
            for item in reversed(st.session_state.history[-5:]):
                with st.expander(item["time"]):
                    st.write("Preview:", item["preview"]) 
                    if item["pos"]:
                        st.write("Findings:", ", ".join(item["pos"]))

    col1, col2 = st.columns([2, 1])

    # IMPORTANT: Render example/clear buttons BEFORE the text area, so that
    # any session_state mutations happen prior to widget instantiation.
    with col2:
        st.markdown('<div class="sub-header">💡 Example Reports</div>', unsafe_allow_html=True)
        examples = [
            ("🔬 Abdominal CT Report", "Mild hepatomegaly with early fatty infiltration. Gallbladder wall thickening. Mild splenomegaly. Bilateral renal cortical cysts. Trace ascites. Mild abdominal aorta ectasia. Mild lumbar degenerative changes."),
            ("🫁 Chest X-Ray Report", "There is consolidation in the right lower lobe. No pleural effusion. Mild cardiomegaly. Lungs are clear. No acute osseous abnormality."),
            ("🩺 Normal Report", "Lungs are clear. No acute osseous abnormality. Cardiomediastinal silhouette within normal limits. No pneumothorax or pleural effusion."),
            ("💓 Cardiac Report", "Mild cardiomegaly. No pericardial effusion. Aortic ectasia. No significant valvular disease. Normal left ventricular function."),
        ]
        for i, (title, content) in enumerate(examples):
            with st.expander(title):
                st.markdown(f"**{content}**")
                st.button(
                    "Use this example",
                    key=f"ex_{i}",
                    on_click=_set_report_text,
                    kwargs={"value": content},
                    use_container_width=False,
                )
        st.markdown("&nbsp;", unsafe_allow_html=True)

    with col1:
        st.markdown('<div class="sub-header">📋 Enter Your Medical Report</div>', unsafe_allow_html=True)

        # Clear button BEFORE the text area so it can mutate session_state safely
        _clear = st.button("🗑️ Clear", use_container_width=False, key="btn_clear", on_click=_set_report_text)

        text = st.text_area(
            "Paste your medical report here:",
            height=260,
            placeholder=(
                "Example: Mild hepatomegaly with early fatty infiltration. Gallbladder wall thickening. "
                "No gallstones or pericholecystic fluid. Pancreas normal."
            ),
            key="report_text",
        )
        st.caption(f"Characters: {len(text) if text else 0}/10,000")

        # Live input preview for visibility/confirmation
        if text:
            st.markdown('<div class="sub-header">🔎 Input Preview</div>', unsafe_allow_html=True)
            st.markdown(
                f"<div class='info-box' style='white-space: pre-wrap'>{text}</div>",
                unsafe_allow_html=True,
            )

        do_analyze = st.button("🔍 Analyze Report", use_container_width=True)

        if (st.session_state.prefs["auto_analyze"] and text and len(text) > 50) or do_analyze:
            analyze_and_render(text)

    st.markdown("---")
    st.caption(
        "For education only. Not a diagnostic tool. Always consult licensed clinicians."
    )


if __name__ == "__main__":
    main()
