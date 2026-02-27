# MDR & Offensive Security Scenario Generator

This application dynamically generates tailored, highly realistic cybersecurity attack scenarios based on a customer's specific IT estate. Powered by **Google Gemini Pro**, it highlights the critical need for Managed Detection and Response (MDR), focusing heavily on the human element of cybersecurity.

## 🎯 Purpose
Move away from generic cybersecurity pitches. This app takes customer telemetry, enriches it with OSINT regarding their specific tech stack, and generates an AI-driven narrative that maps weaknesses to specific Sophos MDR and Secureworks testing solutions.

## ✨ Features
* **Google Gemini Pro Integration:** Generates highly realistic, contextual attack narratives based on industry, user count, and existing tech stack.
* **OSINT Enrichment:** Applies recent threat intelligence vectors to the scenario based on the declared security solutions.
* **Advisory & Testing Mapping:** Automatically suggests follow-up services like External Pen Testing, Wireless Assessments, or Compromise Assessments based on the estate's physical and digital footprint.
* **Instant Export:** Generates downloadable client-ready PDF reports and PowerPoint presentations on the fly.

## 🚀 Getting Started
1. Clone this repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Add your Google Gemini API key to `app.py` (or use Streamlit secrets).
4. Run the application: `streamlit run app.py`