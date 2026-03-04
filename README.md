# 🛡️ Sophos MDR & Offensive Security Scenario Generator

A powerful, Streamlit-based web application designed for Cybersecurity Architects, Sales Engineers, and Consultants. This tool leverages the **Azure OpenAI Service (GPT-4o)** to dynamically generate highly tailored, highly technical cyberattack narratives, simulated MDR case logs, and targeted product recommendations based on a client's specific IT estate.

## ✨ Key Features

* **Azure OpenAI Powered:** Utilizes Microsoft's secure, enterprise-grade GPT-4o models to generate logical, highly technical attack paths and incident response logs.
* **Modular Architecture:** Cleanly separated codebase (`app.py`, `data.py`, `prompts.py`, `export.py`) for easy maintenance and scalability.
* **Massive Threat Intelligence Database:** Automatically maps the client's current technology stack to an expanded, built-in database of real-world CVEs and active threat trends.
* **Guaranteed Originality:** Randomly selects from over 25 modern Initial Access vectors (e.g., AiTM phishing, zero-day VPN exploits, NPM poisoning, MFA fatigue) to ensure every report is unique.
* **Custom Scenario Override & Security Guardrails:** Allows consultants to input specific "What If" scenarios while employing strict anti-prompt-injection instructions to prevent LLM manipulation.
* **Strict Brand Protection:** Prompt engineering ensures the AI never criticizes Sophos products. Breaches are intelligently mapped to human error, third-party zero-days, or misconfigurations.
* **Executive-Ready PowerPoint Exports:** Automatically builds a formatted PPTX deck featuring an estate overview, a concise executive summary, a graphically drawn attack timeline, and a clean recommendations list.
* **Robust PDF Generation:** Outputs beautiful, crash-proof PDF deliverables with native Markdown parsing, clickable hyperlinked CVEs/Products, and perfectly aligned monospaced MDR case logs.

## 🛠️ Prerequisites

* Python 3.9+
* Access to **Azure OpenAI Service** (with a deployed `gpt-4o` model)
* The required Python packages (see below)

## 📦 Installation

1. **Clone the repository:**
   Ensure all four Python files (`app.py`, `data.py`, `prompts.py`, `export.py`) are in the same root directory.

2. **Install dependencies:**
   It is recommended to use a virtual environment.
   ```bash
   pip install -r requirements.txt
   ```
   *Your `requirements.txt` should include:*
   ```text
   streamlit==1.32.0
   requests==2.31.0
   fpdf2==2.7.9
   python-pptx==0.6.23
   openai>=1.0.0
   ```

3. **Configure your Azure API Credentials:**
   Create a hidden Streamlit secrets directory and file:
   ```bash
   mkdir .streamlit
   touch .streamlit/secrets.toml
   ```
   Add your Azure OpenAI keys and endpoint to `secrets.toml`:
   ```toml
   AZURE_OPENAI_API_KEY = "your-azure-key-here"
   AZURE_OPENAI_ENDPOINT = "[https://your-resource-name.openai.azure.com/](https://your-resource-name.openai.azure.com/)"
   AZURE_OPENAI_DEPLOYMENT = "gpt-4o" # The specific name of your model deployment
   AZURE_OPENAI_API_VERSION = "2024-02-15-preview"
   ```

## 🚀 Usage

Run the Streamlit application from your terminal:

```bash
streamlit run app.py
```

1. **Fill out the Client Profile:** Use the sidebar to input the customer's name, industry, user savviness, critical infrastructure, and complete technology stack.
2. **(Optional) Add a Custom Scenario:** Address a specific customer concern by typing it into the *Custom Scenario Override* box (e.g., "How would Sophos detect BlackBasta?").
3. **Generate:** Click "Generate Full Scenario".
4. **Review & Export:** Review the Threat Narrative, Simulated MDR Log, and Recommendations across the UI tabs. Download the generated **PDF Report** or **PowerPoint Deck** using the buttons at the bottom.

## 🏗️ File Structure

* `app.py`: The main Streamlit application. Handles the frontend UI, session state, and coordinates the backend logic.
* `data.py`: Houses the expansive `ATTACK_VECTORS` list and `SIMULATED_OSINT` dictionaries to keep the main app lightweight.
* `prompts.py`: Contains the `SYSTEM_PERSONA` and prompt-building instructions. Enforces the strict technical tone, MITRE ATT&CK hyperlinking rules, and security guardrails.
* `export.py`: The dedicated document generation engine. Contains the FPDF and Python-PPTX classes, graphic drawing logic, and text-cleaning regex functions.

## 📝 Tone & Formatting Notes

The underlying LLM is strictly instructed to act as a Principal Cybersecurity Architect. The output is sterile, objective, and highly technical. All MITRE T-codes, CVEs, and Sophos/Secureworks products generated in the text are automatically converted to clickable Markdown hyperlinks in the UI and PDF, and formatted beautifully for presentation slides.