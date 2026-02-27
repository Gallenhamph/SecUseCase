# app.py
import streamlit as st
import io
import re
import textwrap
from google import genai
from fpdf import FPDF
from pptx import Presentation
from prompts import SYSTEM_PERSONA, build_scenario_prompt

# --- BACKEND LOGIC ---
class CyberScenarioGenerator:
    def __init__(self, api_key):
        self.api_key = api_key
        # Initialize the new Google GenAI Client
        if self.api_key and self.api_key != "YOUR_API_KEY_HERE":
            self.client = genai.Client(api_key=self.api_key)
        else:
            self.client = None
    
    def fetch_osint(self, vendor):
        simulated_osint = {
            "Fortinet": "Recent CVEs regarding SSL-VPN unauthorized execution.",
            "Palo Alto": "Exploitation of unpatched PAN-OS vulnerabilities.",
            "Cisco": "Vulnerabilities in AnyConnect allowing privilege escalation."
        }
        return simulated_osint.get(vendor, f"General misconfigurations and unpatched internet-facing assets tied to {vendor}.")

    def generate_recommendations(self, inputs):
        recs = []
        if inputs['in_house_team'] == "Yes (24/7)" and inputs['savviness'] == "High":
             recs.append("Secureworks Adversary Exercises (Red Teaming): Emulate a sophisticated adversary to stress-test your mature 24/7 SOC.")
        elif inputs['in_house_team'] != "No":
             recs.append("Sophos Internal Penetration Testing: Simulate an attacker who has bypassed the perimeter to test domain compromise.")
             recs.append("Secureworks Tabletop Exercises: Ensure leadership and the internal security team are aligned during a crisis.")
        else:
            recs.append("Sophos Emergency Incident Response Retainer: Crucial for organizations without dedicated internal IR teams.")

        if inputs['public_web_apps']:
            recs.append("Sophos Web Application Security Assessment: Identify coding flaws in your public-facing web applications.")
            recs.append("Sophos External Penetration Testing: Manual attempts to breach your internet-facing assets.")

        if inputs['physical_locations'] > 1:
             recs.append("Sophos Wireless Network Penetration Testing: Evaluate wireless security across your physical locations.")

        if inputs['servers'] > 50:
            recs.append("Sophos Compromise Assessment: Proactively hunt for existing persistence mechanisms in your data center.")
        
        recs.append("Sophos Managed Risk: Implement continuous external attack surface management.")
        return recs

    def call_llm(self, prompt):
        if not self.client:
            return "⚠️ Error: Please enter a valid Gemini API Key in the application code or via Streamlit secrets."
            
        full_prompt = f"{SYSTEM_PERSONA}\n\n{prompt}"
        
        try:
            # Using the new models.generate_content format
            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=full_prompt
            )
            return response.text
        except Exception as e:
            return f"⚠️ An error occurred while communicating with the Gemini API: {e}"

# --- EXPORT LOGIC ---
# --- EXPORT LOGIC ---
def clean_text(text):
    """Strips Markdown and non-ASCII characters without breaking line structures."""
    if not text: return ""
    text = text.replace('\xa0', ' ').replace('\t', ' ')
    text = text.replace('**', '').replace('*', '').replace('#', '')
    text = text.replace('“', '"').replace('”', '"').replace('‘', "'").replace('’', "'")
    text = text.replace('–', '-').replace('—', '-')
    text = text.encode('ascii', 'ignore').decode('ascii')
    return text.strip()

def write_safe_text(pdf, text):
    """
    Bypasses FPDF's fragile multi_cell word-wrap engine. 
    Uses Python's native textwrap to forcefully slice text into lines of 95 chars.
    """
    paragraphs = text.split('\n')
    for paragraph in paragraphs:
        if paragraph.strip():
            # Force wraps lines and cuts aggressively long strings (like URLs)
            lines = textwrap.wrap(paragraph, width=95, break_long_words=True)
            for line in lines:
                # Print single lines natively - impossible to trigger horizontal space errors
                pdf.cell(w=0, h=6, txt=line, new_x="LMARGIN", new_y="NEXT")
        else:
            # Maintain paragraph breaks naturally
            pdf.ln(4)

def create_pdf(inputs, osint, scenario, recs):
    pdf = FPDF()
    pdf.add_page()
    
    # Title
    pdf.set_font("helvetica", "B", 16)
    pdf.cell(w=0, h=10, txt="Cybersecurity Threat & Advisory Report", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(5)
    
    # Section 1: Summary
    pdf.set_font("helvetica", "B", 12)
    pdf.cell(w=0, h=10, txt="Client Estate Summary", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", "", 10)
    summary_text = f"Industry: {inputs['industry']} | Users: {inputs['users']} | Endpoints: {inputs['endpoints']}\nFirewall: {inputs['firewall']} | In-House Team: {inputs['in_house_team']}"
    write_safe_text(pdf, clean_text(summary_text))
    pdf.ln(5)
    
    # Section 2: OSINT
    pdf.set_font("helvetica", "B", 12)
    pdf.cell(w=0, h=10, txt="Applied Threat Intelligence (OSINT)", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", "", 10)
    write_safe_text(pdf, clean_text(osint))
    pdf.ln(5)
    
    # Section 3: Scenario
    pdf.set_font("helvetica", "B", 12)
    pdf.cell(w=0, h=10, txt="Targeted Threat Narrative", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", "", 10)
    write_safe_text(pdf, clean_text(scenario))
    pdf.ln(5)
    
    # Section 4: Recommendations
    pdf.set_font("helvetica", "B", 12)
    pdf.cell(w=0, h=10, txt="Recommended Advisory & Testing Services", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", "", 10)
    for r in recs:
        write_safe_text(pdf, clean_text(f"- {r}"))
        
    return bytes(pdf.output())

# ... Keep create_pptx below exactly as it was!

def create_pptx(inputs, osint, scenario, recs):
    prs = Presentation()
    
    title_slide_layout = prs.slide_layouts[0]
    slide = prs.slides.add_slide(title_slide_layout)
    title = slide.shapes.title
    subtitle = slide.placeholders[1]
    title.text = "Threat Modeling & MDR Assessment"
    subtitle.text = f"Prepared for {inputs['industry']} Sector"
    
    bullet_slide_layout = prs.slide_layouts[1]
    slide2 = prs.slides.add_slide(bullet_slide_layout)
    shapes2 = slide2.shapes
    title_shape2 = shapes2.title
    body_shape2 = shapes2.placeholders[1]
    title_shape2.text = "Attack Scenario"
    tf2 = body_shape2.text_frame
    tf2.text = osint
    p = tf2.add_paragraph()
    p.text = scenario[:250] + "..." 
    
    slide3 = prs.slides.add_slide(bullet_slide_layout)
    shapes3 = slide3.shapes
    title_shape3 = shapes3.title
    body_shape3 = shapes3.placeholders[1]
    title_shape3.text = "Testing & MDR Recommendations"
    tf3 = body_shape3.text_frame
    for r in recs:
        p = tf3.add_paragraph()
        p.text = r
        
    pptx_stream = io.BytesIO()
    prs.save(pptx_stream)
    return pptx_stream.getvalue()

# --- STREAMLIT FRONTEND ---
st.set_page_config(page_title="MDR & Testing Scenario Generator", page_icon="🛡️", layout="wide")

st.title("🛡️ MDR & Offensive Security Scenario Generator")
st.markdown("Generate highly tailored cyberattack scenarios and export to PDF/PPTX using Google Gemini Pro.")

try:
    gemini_key = st.secrets["GEMINI_API_KEY"]
except KeyError:
    st.error("Missing API Key! Please add GEMINI_API_KEY to your .streamlit/secrets.toml file.")
    gemini_key = None

app_engine = CyberScenarioGenerator(api_key=gemini_key)

with st.sidebar:
    st.header("🏢 Client Estate Details")
    industry = st.selectbox("Industry Vertical", ["Healthcare", "Finance", "Manufacturing", "Retail", "Technology", "Education"])
    critical_infra = st.text_input("Critical Infrastructure/Crown Jewels", "Patient Records Database")
    
    st.subheader("👥 The Human Element")
    users = st.number_input("Number of Users", min_value=1, value=500)
    savviness = st.select_slider("User Security Savviness", options=["Low", "Medium", "High"])
    in_house_team = st.radio("In-House Security Team?", ["No", "Yes (9-to-5)", "Yes (24/7)"])
    
    st.subheader("💻 Technology Stack")
    endpoints = st.number_input("Number of Endpoints", min_value=1, value=600)
    servers = st.number_input("Number of Servers", min_value=1, value=50)
    firewall = st.selectbox("Firewall Vendor", ["Fortinet", "Palo Alto", "Cisco", "Check Point", "Sophos", "Other"])
    other_vendors = st.text_input("Other Security Tools", "Microsoft Defender")

    st.subheader("🎯 Additional Attack Surfaces")
    physical_locations = st.number_input("Number of Physical Offices/Locations", min_value=1, value=3)
    public_web_apps = st.checkbox("Host Public-Facing Web Applications?")

    generate_btn = st.button("Generate Scenario", type="primary")

if generate_btn:
    client_inputs = {
        "industry": industry, "users": users, "savviness": savviness, 
        "endpoints": endpoints, "servers": servers, "critical_infra": critical_infra,
        "firewall": firewall, "other_vendors": other_vendors, "in_house_team": in_house_team,
        "physical_locations": physical_locations, "public_web_apps": public_web_apps
    }
    
    with st.spinner("Analyzing estate and generating narrative with Gemini Pro..."):
        osint_data = app_engine.fetch_osint(firewall)
        prompt = build_scenario_prompt(client_inputs, osint_data)
        scenario = app_engine.call_llm(prompt)
        recs = app_engine.generate_recommendations(client_inputs)
        
    st.success("Analysis Complete!")
    
    st.subheader("📝 Generated Threat Narrative")
    st.info(f"**OSINT Context Applied:** {osint_data}")
    st.write(scenario)
    
    st.subheader("🎯 Recommended Security Testing & Advisory")
    for rec in recs:
        st.markdown(f"- {rec}")
        
    st.divider()
    
    if "⚠️ Error" not in scenario and "⚠️ An error" not in scenario:
        pdf_bytes = create_pdf(client_inputs, osint_data, scenario, recs)
        pptx_bytes = create_pptx(client_inputs, osint_data, scenario, recs)
        
        st.subheader("📥 Export Client Deliverables")
        dl_col1, dl_col2 = st.columns(2)
        
        with dl_col1:
            st.download_button(
                label="📄 Download PDF Report",
                data=pdf_bytes,
                file_name="MDR_Scenario_Report.pdf",
                mime="application/pdf"
            )
            
        with dl_col2:
            st.download_button(
                label="📊 Download PowerPoint Deck",
                data=pptx_bytes,
                file_name="MDR_Scenario_Deck.pptx",
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
            )