# 🛡️ Sophos MDR & Offensive Security Scenario Generator

A powerful, Streamlit-based web application designed for Cybersecurity Architects, Sales Engineers, and Consultants. This tool leverages Google's **Gemini 2.5 Flash** model to dynamically generate highly tailored, highly technical cyberattack narratives, simulated MDR case logs, and targeted product recommendations based on a client's specific IT estate.

## ✨ Key Features

* **Dynamic Threat Intelligence (OSINT):** Automatically maps the client's current technology stack (Firewall, Endpoint, Identity, Email, Cloud) to a built-in database of real-world CVEs and active threat trends.
* **Guaranteed Originality:** Randomly selects from a massive pool of modern Initial Access vectors (e.g., AiTM phishing, zero-day VPN exploits, malicious insiders) to ensure every generated report is unique.
* **Custom Scenario Override:** Allows consultants to input a specific threat or "What If" scenario (e.g., "How would Sophos MDR detect a BlackBasta deployment via VPN?"), seamlessly adapting the narrative to focus on early MDR detection.
* **Strict Brand Guardrails:** Prompt engineering ensures the AI never criticizes or blames Sophos products. If Sophos is in the stack, breaches are intelligently mapped to human error, third-party zero-days, or gross misconfigurations.
* **Microsoft 365 Integration Focus:** Dynamically highlights the value of Sophos MDR's native telemetry integrations with Microsoft Graph Security, Entra ID, and Defender based on the client's M365 licensing.
* **Visual Timeline Generation:** Outputs a chronological attack timeline emphasizing *early intervention* by Sophos MDR.
* **Simulated Sophos Central Logs:** Generates a realistic, highly technical Tier 3 MDR case log mimicking what a customer would see in the Sophos Central dashboard.
* **Hyperlinked Recommendations:** Recommends hyperlinked Sophos (NDR, ITDR, Managed Risk) and Secureworks (Red Teaming, Tabletop Exercises) portfolio products directly mapped to the client's vulnerabilities.
* **Export to PDF & PPTX:** Automatically generates beautiful, formatted deliverables. The PDF includes a custom-drawn graphical timeline, and the PowerPoint deck maps the findings directly into presentation slides.

## 🛠️ Prerequisites

* Python 3.9+
* A Google Gemini API Key
* The required Python packages (see below)

## 📦 Installation

1. **Clone the repository or download the source files:**
   Ensure both `app.py` and `prompts.py` are in the same directory.

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
   google-genai>=1.0.0
   ```

3. **Configure your API Key:**
   Create a hidden Streamlit secrets directory and file:
   ```bash
   mkdir .streamlit
   touch .streamlit/secrets.toml
   ```
   Add your Gemini API key to `secrets.toml`:
   ```toml
   GEMINI_API_KEY = "your-actual-api-key-here"
   ```

## 🚀 Usage

Run the Streamlit application from your terminal:

```bash
streamlit run app.py
```

1. **Fill out the Client Profile:** Use the sidebar to input the customer's name, industry, user savviness, critical infrastructure, and complete technology stack (Endpoint, Firewall, Identity, M365 Licensing, Email, and Cloud).
2. **(Optional) Add a Custom Scenario:** Need to address a specific customer concern? Type it into the *Custom Scenario Override* box. If left blank, the app will generate a random, high-impact scenario based on their stack.
3. **Generate:** Click "Generate Full Scenario".
4. **Review & Export:** Review the Threat Narrative, Simulated MDR Log, and Recommendations across the UI tabs. Finally, download the generated **PDF Report** or **PowerPoint Deck** using the buttons at the bottom.

## 🏗️ File Structure

* `app.py`: The main Streamlit application. Handles the frontend UI, OSINT database mapping, recommendation logic, API calls to Gemini, and the FPDF/Python-PPTX export engines.
* `prompts.py`: Contains the `SYSTEM_PERSONA` and prompt-building functions. This enforces the strict tone, MITRE ATT&CK / CVE hyperlinking rules, and the 5-section layout formatting.
* `requirements.txt`: Python package dependencies.

## 📝 Tone & Formatting Notes

The underlying LLM is strictly instructed to act as a Principal Cybersecurity Architect. The output is sterile, objective, and highly technical. All MITRE T-codes and CVEs generated in the text are automatically converted to clickable Markdown hyperlinks in the UI, PDF, and PPTX outputs.