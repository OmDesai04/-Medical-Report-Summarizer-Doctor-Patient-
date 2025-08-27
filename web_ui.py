#!/usr/bin/env python3
"""
Medical Report Summarizer - Enhanced Web UI
Modern, accessible, and user-friendly interface using Streamlit
"""

import streamlit as st
import re
from datetime import datetime
import json
from typing import List, Tuple, Dict, Optional

# Page configuration with better defaults
st.set_page_config(
    page_title="Medical Report Summarizer",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/your-repo/medical-report-summarizer',
        'Report a bug': "https://github.com/your-repo/medical-report-summarizer/issues",
        'About': "Medical Report Summarizer - For educational purposes only"
    }
)

# Enhanced CSS with better accessibility, mobile responsiveness, and modern design
st.markdown("""
<style>
    /* Global styles */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main header with better typography */
    .main-header {
        font-size: clamp(2rem, 5vw, 3.5rem);
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 2rem;
        line-height: 1.2;
    }
    
    /* Sub headers */
    .sub-header {
        font-size: clamp(1.2rem, 3vw, 1.8rem);
        font-weight: 600;
        color: #2d3748;
        margin-bottom: 1.5rem;
        border-bottom: 2px solid #e2e8f0;
        padding-bottom: 0.5rem;
    }
    
    /* Enhanced finding boxes with better contrast and accessibility */
    .finding-box {
        background: linear-gradient(135deg, #fff5f5 0%, #fed7d7 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 6px solid #e53e3e;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .finding-box:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.15);
    }
    
    .normal-box {
        background: linear-gradient(135deg, #f0fff4 0%, #c6f6d5 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 6px solid #38a169;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .normal-box:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.15);
    }
    
    .warning-box {
        background: linear-gradient(135deg, #fffbeb 0%, #fef5e7 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 6px solid #d69e2e;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .warning-box:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.15);
    }
    
    .info-box {
        background: linear-gradient(135deg, #ebf8ff 0%, #bee3f8 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 6px solid #3182ce;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .info-box:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.15);
    }
    
    /* Enhanced text area styling */
    .stTextArea > div > div > textarea {
        background-color: #f7fafc;
        border: 2px solid #e2e8f0;
        border-radius: 8px;
        font-size: 16px;
        line-height: 1.6;
        transition: border-color 0.2s ease, box-shadow 0.2s ease;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        outline: none;
    }
    
    /* Enhanced button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 16px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
        background: linear-gradient(135deg, #5a67d8 0%, #6b46c1 100%);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Secondary button styling */
    .secondary-button > button {
        background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 16px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .secondary-button > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
        background: linear-gradient(135deg, #38a169 0%, #2f855a 100%);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #f7fafc 0%, #edf2f7 100%);
    }
    
    /* Progress bar styling */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Card styling for examples */
    .example-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border: 1px solid #e2e8f0;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .example-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.15);
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2rem;
        }
        
        .sub-header {
            font-size: 1.3rem;
        }
        
        .finding-box, .normal-box, .warning-box, .info-box {
            padding: 1rem;
            margin: 0.5rem 0;
        }
    }
    
    /* Accessibility improvements */
    .sr-only {
        position: absolute;
        width: 1px;
        height: 1px;
        padding: 0;
        margin: -1px;
        overflow: hidden;
        clip: rect(0, 0, 0, 0);
        white-space: nowrap;
        border: 0;
    }
    
    /* Focus indicators for accessibility */
    button:focus, input:focus, textarea:focus {
        outline: 2px solid #667eea;
        outline-offset: 2px;
    }
    
    /* Loading animation */
    .loading-spinner {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid #f3f3f3;
        border-top: 3px solid #667eea;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Status indicators */
    .status-indicator {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 500;
        font-size: 14px;
    }
    
    .status-success {
        background-color: #c6f6d5;
        color: #22543d;
    }
    
    .status-warning {
        background-color: #fef5e7;
        color: #744210;
    }
    
    .status-error {
        background-color: #fed7d7;
        color: #742a2a;
    }
    
    /* Tooltip styling */
    .tooltip {
        position: relative;
        display: inline-block;
    }
    
    .tooltip .tooltiptext {
        visibility: hidden;
        width: 200px;
        background-color: #2d3748;
        color: white;
        text-align: center;
        border-radius: 6px;
        padding: 8px;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        margin-left: -100px;
        opacity: 0;
        transition: opacity 0.3s;
        font-size: 12px;
    }
    
    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for better user experience
if 'analysis_history' not in st.session_state:
    st.session_state.analysis_history = []
if 'user_preferences' not in st.session_state:
    st.session_state.user_preferences = {
        'show_technical': True,
        'show_patient_friendly': True,
        'auto_analyze': False,
        'save_history': True
    }

def comprehensive_summarize(text: str) -> Tuple[List[str], List[str]]:
    """Enhanced comprehensive medical summarization with better accuracy."""
    
    text_lower = text.lower()
    
    # Enhanced medical findings by organ system with better categorization
    findings = {
        # Cardiovascular system
        "cardiomegaly": "cardiomegaly",
        "atrial": "atrial enlargement",
        "ventricular": "ventricular enlargement",
        "aortic": "aortic findings",
        "ectasia": "ectasia",
        "aneurysm": "aneurysm",
        "pericardial": "pericardial effusion",
        
        # Respiratory system
        "ground-glass": "ground-glass opacities",
        "consolidation": "consolidation",
        "atelectasis": "atelectasis",
        "pneumonia": "pneumonia",
        "effusion": "pleural effusion",
        "pneumothorax": "pneumothorax",
        "edema": "pulmonary edema",
        "emphysema": "emphysema",
        "bronchiectasis": "bronchiectasis",
        
        # Gastrointestinal system
        "hepatomegaly": "hepatomegaly",
        "fatty infiltration": "fatty infiltration",
        "hepatic lesions": "hepatic lesions",
        "liver": "liver findings",
        "gallbladder": "gallbladder findings",
        "gallstones": "gallstones",
        "pericholecystic": "pericholecystic fluid",
        "wall thickening": "wall thickening",
        "splenomegaly": "splenomegaly",
        "spleen": "spleen findings",
        "renal": "renal findings",
        "cortical cysts": "cortical cysts",
        "hydronephrosis": "hydronephrosis",
        "kidney": "kidney findings",
        "pancreas": "pancreas findings",
        "peripancreatic": "peripancreatic fluid",
        "bowel obstruction": "bowel obstruction",
        "free air": "free air",
        "bowel": "bowel findings",
        
        # Musculoskeletal system
        "degenerative": "degenerative changes",
        "lumbar": "lumbar findings",
        "fracture": "fracture",
        "osteoporosis": "osteoporosis",
        "osteopenia": "osteopenia",
        "arthritis": "arthritis",
        
        # Lymphatic system
        "lymphadenopathy": "lymphadenopathy",
        "lymph": "lymph node findings",
        
        # Fluid and other findings
        "ascites": "ascites",
        "fluid": "fluid",
        "thickening": "thickening",
        "cysts": "cysts",
        "lesions": "lesions",
        "masses": "masses",
        "nodules": "nodules"
    }
    
    # Enhanced negative indicators
    negative_words = ["no", "not", "negative", "absent", "without", "clear", "normal", "unremarkable", "within normal limits"]
    
    positive_findings = []
    negative_findings = []
    
    # Process the text systematically with better sentence parsing
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
    
    # Remove duplicates while preserving order
    positive_findings = list(dict.fromkeys(positive_findings))
    negative_findings = list(dict.fromkeys(negative_findings))
    
    return positive_findings, negative_findings

def patient_friendly_summary(positive_findings: List[str], negative_findings: List[str]) -> Tuple[List[str], List[str]]:
    """Enhanced patient-friendly summary with better explanations."""
    
    # Comprehensive patient-friendly translations
    patient_terms = {
        # Cardiovascular
        "cardiomegaly": "enlarged heart",
        "atrial enlargement": "enlarged upper heart chamber",
        "ventricular enlargement": "enlarged lower heart chamber",
        "aortic findings": "changes in the main blood vessel (aorta)",
        "ectasia": "widening of blood vessel",
        "aneurysm": "ballooning of blood vessel",
        "pericardial effusion": "fluid around the heart",
        
        # Respiratory
        "ground-glass opacities": "areas in the lungs that look hazy or cloudy",
        "consolidation": "areas of lung tissue that appear solid",
        "atelectasis": "partial collapse of small areas of the lung",
        "pneumonia": "lung infection",
        "pleural effusion": "fluid around the lungs",
        "pneumothorax": "collapsed lung",
        "pulmonary edema": "excess fluid in the lung tissue",
        "emphysema": "damage to the air sacs in the lungs",
        "bronchiectasis": "widening of the airways in the lungs",
        
        # Gastrointestinal
        "hepatomegaly": "enlarged liver",
        "fatty infiltration": "fat deposits in the liver",
        "hepatic lesions": "spots or masses in the liver",
        "liver findings": "liver changes",
        "gallbladder findings": "gallbladder changes",
        "gallstones": "stones in the gallbladder",
        "pericholecystic fluid": "fluid around the gallbladder",
        "wall thickening": "thickened walls",
        "splenomegaly": "enlarged spleen",
        "spleen findings": "spleen changes",
        "renal findings": "kidney changes",
        "cortical cysts": "small fluid-filled sacs in the kidneys",
        "hydronephrosis": "swelling of the kidney due to urine backup",
        "kidney findings": "kidney changes",
        "pancreas findings": "pancreas changes",
        "peripancreatic fluid": "fluid around the pancreas",
        "bowel obstruction": "blockage in the intestines",
        "free air": "air leak in the belly",
        "bowel findings": "intestine changes",
        
        # Musculoskeletal
        "degenerative changes": "wear-and-tear changes (arthritis-like)",
        "lumbar findings": "lower back changes",
        "fracture": "broken bone",
        "osteoporosis": "thinning of bones",
        "osteopenia": "mild thinning of bones",
        "arthritis": "joint inflammation",
        
        # Lymphatic
        "lymphadenopathy": "enlarged lymph nodes",
        "lymph node findings": "lymph node changes",
        
        # Other
        "ascites": "fluid in the belly",
        "fluid": "excess fluid",
        "thickening": "thickening",
        "cysts": "fluid-filled sacs",
        "lesions": "spots or masses",
        "masses": "lumps or growths",
        "nodules": "small lumps or growths"
    }
    
    # Convert positive findings
    patient_positive = []
    for finding in positive_findings:
        patient_positive.append(patient_terms.get(finding, finding))
    
    # Convert negative findings
    patient_negative = []
    for finding in negative_findings:
        if finding.startswith("no "):
            term = finding[3:]  # Remove "no " prefix
            patient_negative.append(f"no {patient_terms.get(term, term)}")
        else:
            patient_negative.append(finding)
    
    return patient_positive, patient_negative

def validate_input(text: str) -> Tuple[bool, str]:
    """Validate input text for medical report analysis."""
    if not text.strip():
        return False, "Please enter a medical report to analyze."
    
    if len(text.strip()) < 10:
        return False, "Please enter a more detailed medical report (at least 10 characters)."
    
    if len(text.strip()) > 10000:
        return False, "Report is too long. Please enter a shorter report (maximum 10,000 characters)."
    
    return True, ""

def save_analysis_history(report_text: str, positive_findings: List[str], negative_findings: List[str]):
    """Save analysis to session history."""
    if st.session_state.user_preferences['save_history']:
        analysis = {
            'timestamp': datetime.now().isoformat(),
            'report_preview': report_text[:100] + "..." if len(report_text) > 100 else report_text,
            'positive_findings': positive_findings,
            'negative_findings': negative_findings
        }
        st.session_state.analysis_history.append(analysis)
        
        # Keep only last 10 analyses
        if len(st.session_state.analysis_history) > 10:
            st.session_state.analysis_history = st.session_state.analysis_history[-10:]

def main():
    """Main application function with enhanced UI/UX."""
    
    # Header with improved accessibility
    st.markdown('<h1 class="main-header" role="heading" aria-level="1">🏥 Medical Report Summarizer</h1>', unsafe_allow_html=True)
    
    # Sidebar with enhanced functionality
    with st.sidebar:
        st.markdown("### ⚙️ Settings")
        
        # User preferences
        st.markdown("**Display Options:**")
        st.session_state.user_preferences['show_technical'] = st.checkbox(
            "Show technical summary", 
            value=st.session_state.user_preferences['show_technical'],
            help="Display medical terminology in results"
        )
        st.session_state.user_preferences['show_patient_friendly'] = st.checkbox(
            "Show patient-friendly summary", 
            value=st.session_state.user_preferences['show_patient_friendly'],
            help="Display simple explanations for patients"
        )
        st.session_state.user_preferences['auto_analyze'] = st.checkbox(
            "Auto-analyze on input", 
            value=st.session_state.user_preferences['auto_analyze'],
            help="Automatically analyze when text is entered"
        )
        st.session_state.user_preferences['save_history'] = st.checkbox(
            "Save analysis history", 
            value=st.session_state.user_preferences['save_history'],
            help="Keep track of recent analyses"
        )
        
        st.markdown("---")
        
        # Instructions with better organization
        st.markdown("### 📋 How to Use")
        st.markdown("""
        1. **Paste your medical report** in the text area
        2. **Click 'Analyze Report'** to get summaries
        3. **View both technical and patient-friendly** explanations
        
        **Supported formats:**
        - Radiology reports
        - Lab results
        - Clinical notes
        - Imaging findings
        """)
        
        # Enhanced disclaimer
        st.markdown("### ⚠️ Important Disclaimer")
        st.markdown("""
        **For educational purposes only**
        
        This tool is NOT a diagnostic tool and should NOT replace professional medical advice.
        
        Always consult with your healthcare provider for medical decisions.
        
        **Privacy:** All processing happens locally on your computer.
        """)
        
        # What it detects with better organization
        st.markdown("### 🔬 What It Detects")
        st.markdown("""
        **Organ Systems:**
        - **Heart & Blood Vessels** - cardiomegaly, aneurysms
        - **Lungs** - pneumonia, effusions, opacities
        - **Liver & Gallbladder** - hepatomegaly, gallstones
        - **Kidneys & Pancreas** - cysts, fluid collections
        - **Bones & Spine** - fractures, degenerative changes
        - **Bowel & Lymph** - obstructions, enlarged nodes
        """)
        
        # Analysis history
        if st.session_state.analysis_history:
            st.markdown("### 📚 Recent Analyses")
            for i, analysis in enumerate(reversed(st.session_state.analysis_history[-5:])):
                with st.expander(f"Analysis {len(st.session_state.analysis_history) - i}"):
                    st.write(f"**Preview:** {analysis['report_preview']}")
                    st.write(f"**Time:** {analysis['timestamp'][:19]}")
                    if analysis['positive_findings']:
                        st.write(f"**Findings:** {', '.join(analysis['positive_findings'][:3])}")
    
    # Main content area with better layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<h2 class="sub-header">📋 Enter Your Medical Report</h2>', unsafe_allow_html=True)
        
        # Enhanced text input area
        report_text = st.text_area(
            "Paste your medical report here:",
            height=300,
            placeholder="Example: Mild hepatomegaly with early fatty infiltration. Gallbladder wall thickening. No gallstones or pericholecystic fluid. Pancreas normal, no peripancreatic fluid.",
            help="Copy and paste your complete medical report text. The system will analyze it for medical findings and provide both technical and patient-friendly summaries.",
            key="report_input"
        )
        
        # Character count and validation
        char_count = len(report_text) if report_text else 0
        st.caption(f"Characters: {char_count}/10,000")
        
        # Auto-analyze functionality
        if st.session_state.user_preferences['auto_analyze'] and report_text:
            is_valid, error_msg = validate_input(report_text)
            if is_valid and char_count > 50:  # Only auto-analyze if substantial text
                st.info("🔄 Auto-analyzing... (You can disable this in settings)")
                analyze_report(report_text)
        
        # Manual analyze button with enhanced styling
        col_button1, col_button2 = st.columns(2)
        
        with col_button1:
            analyze_button = st.button(
                "🔍 Analyze Report", 
                type="primary", 
                use_container_width=True,
                help="Click to analyze your medical report"
            )
        
        with col_button2:
            if st.button("🗑️ Clear", use_container_width=True, help="Clear the text area"):
                st.session_state.report_input = ""
                st.rerun()
        
        # Analysis results
        if analyze_button:
            analyze_report(report_text)
    
    with col2:
        st.markdown('<h2 class="sub-header">💡 Example Reports</h2>', unsafe_allow_html=True)
        
        # Enhanced example cards
        examples = [
            {
                "title": "🔬 Abdominal CT Report",
                "content": "Mild hepatomegaly with early fatty infiltration. Gallbladder wall thickening. Mild splenomegaly. Bilateral renal cortical cysts. Trace ascites. Mild abdominal aorta ectasia. Mild lumbar degenerative changes.",
                "category": "CT Scan"
            },
            {
                "title": "🫁 Chest X-Ray Report", 
                "content": "There is consolidation in the right lower lobe. No pleural effusion. Mild cardiomegaly. Lungs are clear. No acute osseous abnormality.",
                "category": "X-Ray"
            },
            {
                "title": "🩺 Normal Report",
                "content": "Lungs are clear. No acute osseous abnormality. Cardiomediastinal silhouette within normal limits. No pneumothorax or pleural effusion.",
                "category": "Normal"
            },
            {
                "title": "💓 Cardiac Report",
                "content": "Mild cardiomegaly. No pericardial effusion. Aortic ectasia. No significant valvular disease. Normal left ventricular function.",
                "category": "Cardiac"
            }
        ]
        
        for example in examples:
            with st.expander(example["title"]):
                st.markdown(f"**{example['content']}**")
                st.caption(f"Category: {example['category']}")
                if st.button(f"Use Example", key=f"example_{example['title']}"):
                    st.session_state.report_input = example['content']
                    st.rerun()
        
        st.markdown("---")
        st.markdown("### 📱 Quick Tips")
        st.markdown("""
        - **Copy** your medical report
        - **Paste** it in the text area
        - **Click** 'Analyze Report'
        - **Get** instant summaries
        - **Save** your preferences in settings
        """)
    
    # Footer with enhanced information
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 1rem; background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%); border-radius: 12px;'>
        <p style='font-weight: 600; margin-bottom: 0.5rem;'>🏥 Medical Report Summarizer</p>
        <p style='font-size: 14px; margin-bottom: 0.5rem;'>For educational purposes only | Always consult healthcare professionals</p>
        <p style='font-size: 12px; margin: 0;'>Built with ❤️ using Streamlit | Enhanced UI/UX Design</p>
    </div>
    """, unsafe_allow_html=True)

def analyze_report(report_text: str):
    """Analyze the medical report and display results."""
    
    # Input validation
    is_valid, error_msg = validate_input(report_text)
    if not is_valid:
        st.error(f"❌ {error_msg}")
        return
    
    # Show loading state
    with st.spinner("🔬 Analyzing your medical report..."):
        # Process the report
        positive_findings, negative_findings = comprehensive_summarize(report_text)
        patient_positive, patient_negative = patient_friendly_summary(positive_findings, negative_findings)
        
        # Save to history
        save_analysis_history(report_text, positive_findings, negative_findings)
        
        # Display results with enhanced styling
        st.markdown("---")
        st.markdown('<h2 class="sub-header">📊 Analysis Results</h2>', unsafe_allow_html=True)
        
        # Status indicator
        if positive_findings:
            st.markdown('<div class="status-indicator status-warning">🔍 Findings Detected</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-indicator status-success">✅ No Significant Findings</div>', unsafe_allow_html=True)
        
        # Technical summary (if enabled)
        if st.session_state.user_preferences['show_technical']:
            st.markdown('<h3 class="sub-header">🔬 Technical Summary</h3>', unsafe_allow_html=True)
            
            if positive_findings:
                st.markdown('<div class="finding-box">', unsafe_allow_html=True)
                st.markdown("**🔍 Findings Detected:**")
                for finding in positive_findings:
                    st.markdown(f"• {finding}")
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="normal-box">', unsafe_allow_html=True)
                st.markdown("**✅ No significant findings detected**")
                st.markdown('</div>', unsafe_allow_html=True)
            
            if negative_findings:
                st.markdown('<div class="normal-box">', unsafe_allow_html=True)
                st.markdown("**✅ Normal Findings:**")
                for finding in negative_findings:
                    st.markdown(f"• {finding}")
                st.markdown('</div>', unsafe_allow_html=True)
        
        # Patient-friendly summary (if enabled)
        if st.session_state.user_preferences['show_patient_friendly']:
            st.markdown('<h3 class="sub-header">👥 Patient-Friendly Summary</h3>', unsafe_allow_html=True)
            
            if patient_positive:
                st.markdown('<div class="finding-box">', unsafe_allow_html=True)
                st.markdown("**🔍 What was found:**")
                for finding in patient_positive:
                    st.markdown(f"• {finding}")
                st.markdown('</div>', unsafe_allow_html=True)
            
            if patient_negative:
                st.markdown('<div class="normal-box">', unsafe_allow_html=True)
                st.markdown("**✅ What's normal:**")
                for finding in patient_negative:
                    st.markdown(f"• {finding}")
                st.markdown('</div>', unsafe_allow_html=True)
        
        # Summary statistics
        col_stats1, col_stats2, col_stats3 = st.columns(3)
        with col_stats1:
            st.metric("Total Findings", len(positive_findings))
        with col_stats2:
            st.metric("Normal Results", len(negative_findings))
        with col_stats3:
            st.metric("Analysis Time", f"{datetime.now().strftime('%H:%M:%S')}")
        
        # Timestamp
        st.caption(f"*Analysis completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")

if __name__ == "__main__":
    main()
