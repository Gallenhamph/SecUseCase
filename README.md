# 🛡️ MDR & Offensive Security Scenario Generator

A dynamic, AI-powered sales engineering and consulting tool designed to generate highly tailored, realistic cybersecurity attack scenarios. 

Instead of relying on generic cybersecurity pitches, this application takes a customer's specific IT estate telemetry, enriches it with Threat Intelligence (OSINT), and uses **Google Gemini 2.5 Pro** to weave a compelling narrative. It highlights the critical need for Managed Detection and Response (MDR), focuses heavily on the human element, and maps estate weaknesses directly to the **Sophos** and **Secureworks** advisory and testing portfolios.

## ✨ Key Features

* **🧠 Advanced AI Narrative Generation:** Powered by the modern `google-genai` SDK and Gemini 2.5 Flash. The AI acts as a Principal Cybersecurity Architect, blending real-world news, OSINT, and customer telemetry into a seamless, highly realistic attack narrative.
* **🎯 Sophos & Secureworks Mapping:** Automatically recommends tailored security assessments based on the customer's digital and physical footprint, including:
  * Secureworks Adversary Exercises (Red Teaming) & Tabletop Exercises
  * Sophos Internal/External & Wireless Penetration Testing
  * Sophos Web Application Security Assessments
  * Sophos Compromise Assessments & Managed Risk
* **🏢 "Bring Your Own Tech" (BYOT) Focus:** Illustrates how siloed security tools (e.g., standalone third-party firewalls) fail to stop lateral movement, positioning Sophos MDR's cross-vendor telemetry ingestion as the ultimate solution.
* **📄 Professional PDF Export:** Includes a custom-built, crash-proof PDF generator (via `fpdf2` and `textwrap`) that outputs consultant-ready deliverables with custom branding, shaded summary boxes, and stylized section headers.
* **📊 PowerPoint Generation:** Instantly builds a foundational PPTX slide deck based on the generated narrative for immediate executive presentations.
* **🔒 Secure by Design:** Utilizes Streamlit's local secrets management to ensure your LLM API keys are never hardcoded or exposed.

## 🛠️ Technology Stack
* **Frontend:** [Streamlit](https://streamlit.io/) (Interactive Web UI)
* **LLM Engine:** Google Gemini (`gemini-2.5-flash` via `google-genai`)
* **Document Generation:** `fpdf2` (PDFs) and `python-pptx` (Presentations)
* **Data Processing:** Python 3.x native libraries (`re`, `textwrap`, `io`)

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone [https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git)
cd YOUR_REPO_NAME
```

### 2. Install Dependencies
It is recommended to use a virtual environment (`venv`).
```bash
pip install -r requirements.txt
```

### 3. Configure Your Gemini API Key
For security, this application uses Streamlit Secrets. You must create a local secrets file before running the app.

1. Create a hidden `.streamlit` folder in the root directory:
   ```bash
   mkdir .streamlit
   ```
2. Create a `secrets.toml` file inside that folder:
   ```bash
   touch .streamlit/secrets.toml
   ```
3. Add your Google Gemini API key to the `secrets.toml` file:
   ```toml
   GEMINI_API_KEY = "your_actual_api_key_here"
   ```
*(Note: The `.gitignore` file is configured to ensure this file is never pushed to GitHub).*

### 4. Run the Application
```bash
streamlit run app.py
```
The application will automatically open in your default web browser at `http://localhost:8501`.

---

## 📁 Project Structure

```text
├── app.py               # Main Streamlit application and export logic (PDF/PPTX)
├── prompts.py           # System personas, core objectives, and LLM prompt engineering
├── requirements.txt     # Python package dependencies
├── .gitignore           # Git ignore rules (protects API keys and environments)
└── .streamlit/          # (Local only) Contains secrets.toml for API key management
```

## 💡 How It Works
1. **Input:** The consultant enters the customer's engagement details (industry, user count, savviness, firewall vendor, physical locations, etc.) into the Streamlit sidebar.
2. **OSINT Enrichment:** The app fetches simulated, relevant threat intelligence based on the declared perimeter technologies.
3. **Generation:** Gemini 2.5 Flash processes the prompt, generating a 4-paragraph brief that details initial access, lateral movement, the Sophos MDR differentiator, and a proactive product/testing summary.
4. **Export:** The consultant can instantly download the AI-generated scenario as a beautifully formatted PDF report or a PPTX deck to hand straight to the client.
