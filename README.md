# 🩺 Medical Report Summarizer  

A complete end-to-end system that parses medical reports, extracts lab values, and generates both **technical (doctor-focused)** and **patient-friendly** summaries. It combines **OCR, table-aware reconstruction, advanced normalization, and an interactive Streamlit UI** for smooth use.  

---

## ✨ Key Features  

- **Dual Summaries**  
  - 🧑‍⚕️ Doctor’s Summary: concise technical findings with abnormal highlights.  
  - 👥 Patient-Friendly Summary: simple, plain-language explanations for easy understanding.  

- **OCR + Table-Aware Extraction**  
  - Standard OCR for scanned images.  
  - Table-aware OCR to **reconstruct rows/columns from lab sheets**.  
  - Smart merging of outputs to fix missing headers/footers.  

- **Robust Lab Parsing**  
  - Extracts **numeric values, units, and reference ranges**.  
  - Auto-corrects OCR errors (e.g., missing decimals, unit mismatches, ×10 shifts).  
  - Supports **qualitative reports** (Present/Absent, + to +++, counts like /hpf).  

- **Streamlit UI**  
  - Clean, centered card-based layout with **high contrast and easy navigation**.  
  - **Sample + Clear buttons** for quick testing.  
  - Progress indicators while analyzing reports.  

- **Flexible Input Modes**  
  - 📂 Upload image (JPG/PNG) → choose standard OCR or smart table-aware OCR.  
  - 📋 Paste plain text → direct analysis.  

- **Rich Output**  
  - 📊 Parsed Labs Table: values, units, reference ranges, and status (Normal/Abnormal).  
  - 🧑‍⚕️ Doctor’s Technical Summary.  
  - 👥 Patient-Friendly Summary.  

---

## 🚀 Quickstart  

### 1) Setup Environment (Windows PowerShell)  

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt

streamlit run src/app_streamlit.py
```
## 📸 Screenshots
### 1) Home Page
<img width="1863" height="816" alt="image" src="https://github.com/user-attachments/assets/0ea25d8a-ae7d-4d84-b9c0-7926478ed24b" />

### 2) Report(differnet types of tests)extracted from image and summary & Extracted Table View
<img width="1653" height="857" alt="image" src="https://github.com/user-attachments/assets/713d8ee1-534b-4a0b-9a9d-e94bde4c6208" />

### 3) Medical report directly pasted in the result section
<img width="1875" height="849" alt="image" src="https://github.com/user-attachments/assets/c1cdb69e-7211-49fb-a493-d33bf1168919" />

### 4)Techinal and Patient Friendly Summary of that report
<img width="1007" height="854" alt="image" src="https://github.com/user-attachments/assets/be50c07d-1074-44d7-a4d9-5efe6c5e944f" />



