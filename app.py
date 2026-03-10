# app.py
import streamlit as st
import random
from pydantic import BaseModel, Field
from typing import List
from openai import AzureOpenAI
from data import ATTACK_VECTORS, SIMULATED_OSINT
from prompts import SYSTEM_PERSONA, build_scenario_prompt, build_mdr_case_prompt
from export import create_pdf, create_pptx

# --- PYDANTIC DATA MODELS (STRUCTURED OUTPUT) ---
class TimelineEvent(BaseModel):
    timestamp: str = Field(description="The timestamp of the event, e.g., '02:00 UTC' or 'Day 1 - 08:00'")
    event_description: str = Field(description="A detailed description of the attack progression or MDR intervention.")

class ScenarioReport(BaseModel):
    narrative: str = Field(description="Sections 1 through 4: The full, highly technical threat narrative and MDR response formatted in Markdown.")
    timeline: List[TimelineEvent] = Field(description="Section 5: The chronological attack timeline.")

# --- BACKEND LOGIC ---
class CyberScenarioGenerator:
    def __init__(self, api_key, endpoint, deployment, api_version):
        self.deployment = deployment
        if api_key and endpoint:
            self.client = AzureOpenAI(
                api_key=api_key,  
                api_version=api_version,
                azure_endpoint=endpoint
            )
        else:
            self.client = None
    
    def fetch_osint(self, vendor):
        options = SIMULATED_OSINT.get(vendor, [])
        return random.choice(options) if options else ""

    def generate_recommendations(self, inputs):
        recs = []
        recs.append("🛡️ **SECURITY ASSESSMENTS & ADVISORY**")
        
        if inputs['in_house_team'] == "Yes (24/7)" and inputs['savviness'] in ["Medium", "High"]:
             recs.append("• [Secureworks Adversary Exercises (Red Teaming)](https://www.secureworks.com/services/offensive-security): Emulate a sophisticated adversary to stress-test your mature 24/7 SOC and validate detection capabilities across the kill chain.")
             recs.append("• [Secureworks Threat Hunting Assessment](https://www.secureworks.com/services/threat-hunting): Proactively search your environment for undetected threats or persistence mechanisms that may have bypassed your existing defenses.")
        elif inputs['in_house_team'] != "No":
             recs.append("• [Sophos Internal Penetration Testing](https://www.sophos.com/en-us/services/penetration-testing): Simulate an attacker who has bypassed the perimeter to test domain compromise, internal lateral movement, and existing defenses.")
             recs.append("• [Secureworks Tabletop Exercises](https://www.secureworks.com/services/incident-response-readiness): Ensure leadership and the internal security team are aligned on communication, legal, and operational procedures during a crisis.")
        else:
            recs.append("• [Sophos Emergency Incident Response Retainer](https://www.sophos.com/en-us/services/incident-response-retainer): Crucial for organizations without dedicated internal IR teams to guarantee SLAs and immediate assistance during a live breach.")
            recs.append("• [Secureworks Ransomware Readiness Assessment](https://www.secureworks.com/services/incident-response-readiness): Evaluate your organization's preparedness to defend against, endure, and recover from a targeted ransomware event.")

        if inputs['public_web_apps']:
            recs.append("• [Sophos Web Application Security Assessment](https://www.sophos.com/en-us/services/penetration-testing): Identify coding flaws (e.g., SQLi, XSS) in your public-facing web applications before attackers exploit them to access backend databases.")
            recs.append("• [Sophos External Penetration Testing](https://www.sophos.com/en-us/services/penetration-testing): Manual, tester-driven attempts to breach your internet-facing assets, moving beyond automated vulnerability scanning.")

        if inputs['physical_locations'] > 1:
             recs.append("• [Sophos Wireless Network Penetration Testing](https://www.sophos.com/en-us/services/penetration-testing): Evaluate wireless security across your physical locations, testing for rogue access points and weak encryption.")

        if "Cloud" in inputs['cloud_env'] or inputs['cloud_env'] in ["AWS", "Microsoft Azure", "GCP"]:
            recs.append(f"• [Sophos Cloud Security Assessment](https://www.sophos.com/en-us/services/cloud-security-posture-management): Audit your {inputs['cloud_env']} environment for misconfigurations, overly permissive IAM roles, and compliance violations.")

        if inputs['savviness'] == "Low":
            recs.append("• [Sophos Phish Threat (Social Engineering Simulation)](https://www.sophos.com/en-us/products/phish-threat): Conduct targeted phishing and social engineering exercises to baseline and improve employee security awareness.")

        if "Active Directory" in inputs['identity'] or "Entra ID" in inputs['identity']:
             recs.append("• [Sophos Active Directory Security Assessment](https://www.sophos.com/en-us/services/compromise-assessment): Identify architectural weaknesses, excessive privileges, and misconfigurations in your core identity platform.")

        if inputs['servers'] > 50:
            recs.append("• [Sophos Compromise Assessment](https://www.sophos.com/en-us/services/compromise-assessment): Proactively hunt for existing persistence mechanisms or dormant threats currently hiding in your data center.")

        recs.append("\n⚙️ **RECOMMENDED SOPHOS SOLUTIONS**")
        
        if inputs['m365_license'] != "None / On-Prem Only":
            recs.append(f"• [Sophos MDR for Microsoft 365](https://www.sophos.com/en-us/products/mdr): Maximize your {inputs['m365_license']} investment. Sophos ingests telemetry directly from Microsoft Graph Security, Entra ID, and Defender to correlate Microsoft alerts with cross-domain threat intelligence, stopping attacks that bypass native Microsoft controls.")

        recs.append("• [Sophos Managed Risk](https://www.sophos.com/en-us/products/managed-risk): Implement continuous external attack surface management to discover and prioritize exposed vulnerabilities across your evolving tech stack before they can be weaponized.")

        if inputs['identity'] not in ["None / Local Only", "On-Prem Active Directory"]:
            recs.append(f"• [Sophos ITDR (Identity Threat Detection and Response)](https://www.sophos.com/en-us/products/mdr): Integrate telemetry directly from {inputs['identity']} to detect compromised credentials, anomalous logins, and lateral movement tied to user identities before endpoints are even touched.")

        if inputs['firewall'] != "Sophos" or inputs['servers'] > 20:
            recs.append("• [Sophos NDR (Network Detection and Response)](https://www.sophos.com/en-us/products/network-detection-and-response): Analyze network traffic for rogue devices, unprotected assets, and insider threats. This is critical for monitoring lateral movement across the network in a 'Bring Your Own Tech' environment.")

        if inputs['endpoint'] != "Sophos":
             recs.append(f"• [Sophos Intercept X Advanced with XDR](https://www.sophos.com/en-us/products/endpoint-antivirus): Consolidate your endpoint stack by replacing {inputs['endpoint']}. This provides Sophos MDR analysts with native, deep-level remediation capabilities rather than just third-party telemetry.")
             
        if inputs['email'] != "Sophos":
             recs.append(f"• [Sophos Email Security](https://www.sophos.com/en-us/products/email-security): Integrate advanced phishing protection and post-delivery remediation natively into your MDR ecosystem, reducing the risk of social engineering attacks that bypass {inputs['email']}.")

        return recs

    def call_llm_structured(self, prompt, response_model):
        if not self.client: return None
        try:
            response = self.client.beta.chat.completions.parse(
                model=self.deployment,
                messages=[
                    {"role": "system", "content": SYSTEM_PERSONA},
                    {"role": "user", "content": prompt}
                ],
                response_format=response_model,
                temperature=0.7
            )
            return response.choices[0].message.parsed
        except Exception as e:
            st.error(f"Azure OpenAI Parsing Error: {e}")
            return None

    def call_llm_text(self, prompt):
        if not self.client: return "⚠️ Error: Please enter valid Azure OpenAI credentials."
        try:
            response = self.client.chat.completions.create(
                model=self.deployment,
                messages=[
                    {"role": "system", "content": SYSTEM_PERSONA},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"⚠️ An error occurred: {e}"

# --- HELPER: EXPORT GENERATOR ---
def update_exports():
    """Generates the PDF and PPTX and saves them to session state."""
    if st.session_state.get('scenario_obj'):
        try:
            st.session_state['pdf_bytes'] = create_pdf(
                st.session_state['client_inputs'], 
                st.session_state['scenario_obj'], 
                st.session_state['recs'], 
                st.session_state['mdr_case']
            )
        except Exception as e:
            st.error(f"PDF Generation Failed: {e}")
            st.session_state['pdf_bytes'] = None
            
        try:
            st.session_state['pptx_bytes'] = create_pptx(
                st.session_state['client_inputs'], 
                st.session_state['scenario_obj'], 
                st.session_state['recs'], 
                st.session_state['mdr_case']
            )
        except Exception as e:
            st.error(f"PowerPoint Generation Failed: {e}")
            st.session_state['pptx_bytes'] = None


# --- STREAMLIT FRONTEND ---
st.set_page_config(page_title="MDR & Testing Scenario Generator", page_icon="🛡️", layout="wide")
st.title("🛡️ MDR & Offensive Security Scenario Generator")
st.markdown("Generate highly tailored cyberattack scenarios, complete with mock Sophos Central case logs.")

# Fetch Azure Secrets
try:
    az_key = st.secrets["AZURE_OPENAI_API_KEY"]
    az_endpoint = st.secrets["AZURE_OPENAI_ENDPOINT"]
    az_deployment = st.secrets["AZURE_OPENAI_DEPLOYMENT"]
    az_api_version = st.secrets.get("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
except KeyError:
    st.error("Missing API Credentials! Check your secrets.toml file.")
    az_key, az_endpoint, az_deployment, az_api_version = None, None, None, None

app_engine = CyberScenarioGenerator(
    api_key=az_key, 
    endpoint=az_endpoint, 
    deployment=az_deployment, 
    api_version=az_api_version
)

with st.sidebar:
    st.header("📋 Engagement Details")
    customer_name = st.text_input("Customer Name", "Acme Corp")
    consultant_name = st.text_input("Consultant Name", "Jane Doe")
    
    st.header("🏢 Client Estate Details")
    industry = st.selectbox("Industry Vertical", ["Healthcare", "Finance", "Manufacturing", "Retail", "Technology", "Education"])
    critical_infra = st.text_input("Critical Infrastructure/Crown Jewels", "Patient Records Database")
    
    st.subheader("👥 The Human Element")
    
    # Make sure this line only appears ONCE!
    users = st.number_input("Number of Users", min_value=1, value=500)
    
    savviness_profiles = {
        "Tier 1: High Risk / Unaware": "Users frequently reuse passwords, ignore browser warnings, and are highly susceptible to basic phishing.",
        "Tier 2: Basic Compliance": "Users complete mandatory training but easily fall for targeted spear-phishing, urgency tactics, or MFA fatigue.",
        "Tier 3: Cautious / Conscious": "A strong security culture. Users actively report suspicious emails and question unusual requests.",
        "Tier 4: Highly Technical (IT/Dev)": "Advanced users. Hard to phish, but high risk for Shadow IT, disabling agents, or leaking API keys to get work done."
    }
    
    savviness_label = st.selectbox(
        "User Security Culture", 
        options=list(savviness_profiles.keys()),
        index=1
    )
    
    st.caption(f"*{savviness_profiles[savviness_label]}*")
    savviness = f"{savviness_label} - {savviness_profiles[savviness_label]}"
    
    in_house_team = st.radio("In-House Security Team?", ["No", "Yes (9-to-5)", "Yes (24/7)"])
    
    st.subheader("💻 Technology Stack")
    endpoints = st.number_input("Number of Endpoints", min_value=1, value=600)
    servers = st.number_input("Number of Servers", min_value=1, value=50)
    endpoint = st.selectbox("Endpoint Security", ["Sophos", "Microsoft Defender", "CrowdStrike", "SentinelOne", "Trend Micro", "Symantec", "Trellix", "Blackberry Cylance", "Other"])
    firewall = st.selectbox("Firewall Vendor", ["Fortinet", "Palo Alto", "Cisco", "Check Point", "SonicWall", "WatchGuard", "Juniper", "Barracuda", "Forcepoint", "Sophos", "Other"])
    identity = st.selectbox("Identity Provider", ["Microsoft Entra ID (Azure AD)", "Okta", "Cisco Duo", "Ping Identity", "On-Prem Active Directory", "None / Local Only"])
    m365_license = st.selectbox("Microsoft 365 Licensing", ["None / On-Prem Only", "M365 Business Basic/Standard", "M365 Business Premium", "Office 365 E3 / M365 E3", "Microsoft 365 E5"])
    email = st.selectbox("Email Security", ["Sophos", "Microsoft Defender for Office 365", "Mimecast", "Proofpoint", "Barracuda", "Other"])
    cloud_env = st.selectbox("Cloud Infrastructure", ["AWS", "Microsoft Azure", "GCP", "Multi-Cloud", "None (Fully On-Prem)"])

    st.subheader("🎯 Additional Attack Surfaces")
    physical_locations = st.number_input("Number of Physical Offices/Locations", min_value=1, value=3)
    public_web_apps = st.checkbox("Host Public-Facing Web Applications?")
    
    st.subheader("🛠️ Custom Scenario Override")
    custom_scenario = st.text_area("Specific Threat/Use Case (Optional)", placeholder="e.g., 'How would Sophos MDR detect a BlackBasta deployment?'")
    generate_btn = st.button("Generate Full Scenario", type="primary")

# --- GENERATION LOGIC ---
if generate_btn:
    client_inputs = {
        "customer_name": customer_name, "consultant_name": consultant_name,
        "industry": industry, "users": users, "savviness": savviness, 
        "endpoints": endpoints, "servers": servers, "critical_infra": critical_infra,
        "endpoint": endpoint, "firewall": firewall, "identity": identity, 
        "m365_license": m365_license, "email": email, "cloud_env": cloud_env,
        "in_house_team": in_house_team, "physical_locations": physical_locations, "public_web_apps": public_web_apps
    }
    
    selected_vector = random.choice(ATTACK_VECTORS)
    osint_list = [
        app_engine.fetch_osint(endpoint),
        app_engine.fetch_osint(firewall),
        app_engine.fetch_osint(identity),
        app_engine.fetch_osint(email),
        app_engine.fetch_osint(cloud_env)
    ]
    osint_data = " ".join([x for x in osint_list if x])

    # Save to session state for potential regenerations later
    st.session_state['client_inputs'] = client_inputs
    st.session_state['customer_name'] = customer_name
    st.session_state['selected_vector'] = selected_vector
    st.session_state['osint_data'] = osint_data
    st.session_state['custom_scenario'] = custom_scenario
    
    with st.spinner("Analyzing estate and generating structured narrative with Azure OpenAI GPT-4o..."):
        # 1. Generate Structured Narrative & Timeline
        narrative_prompt = build_scenario_prompt(client_inputs, osint_data, selected_vector, custom_scenario)
        scenario_obj = app_engine.call_llm_structured(narrative_prompt, ScenarioReport)
        
        # 2. Generate Standard Text Log
        if scenario_obj:
            case_prompt = build_mdr_case_prompt(client_inputs, scenario_obj.narrative)
            mdr_case = app_engine.call_llm_text(case_prompt)
        else:
            mdr_case = "Generation failed."
        
        recs = app_engine.generate_recommendations(client_inputs)
        
        st.session_state['scenario_obj'] = scenario_obj
        st.session_state['mdr_case'] = mdr_case
        st.session_state['recs'] = recs
        
        # 3. Build Exports via helper function
        update_exports()

    st.success("Analysis Complete!")

# --- UI RENDERING ---
if 'scenario_obj' in st.session_state and st.session_state['scenario_obj']:
    scenario_obj = st.session_state['scenario_obj']
    mdr_case = st.session_state['mdr_case']
    recs = st.session_state['recs']
    cached_customer_name = st.session_state['customer_name']
    
    tab1, tab2, tab3 = st.tabs(["📝 Threat Narrative", "🛡️ Sophos Central MDR Log", "🎯 Recommendations"])
    
    with tab1:
        st.subheader(f"Threat Narrative & Solutions for {cached_customer_name}")
        st.write(scenario_obj.narrative)
        st.markdown("#### Attack Timeline & Early MDR Intervention")
        for t_event in scenario_obj.timeline:
            st.markdown(f"**{t_event.timestamp}** | {t_event.event_description}")
            
        st.divider()
        if st.button("🔄 Regenerate Narrative & Timeline", use_container_width=True):
            with st.spinner("Regenerating a new narrative path..."):
                # Pull saved variables from session state
                n_prompt = build_scenario_prompt(
                    st.session_state['client_inputs'], 
                    st.session_state['osint_data'], 
                    st.session_state['selected_vector'], 
                    st.session_state['custom_scenario']
                )
                new_scenario = app_engine.call_llm_structured(n_prompt, ScenarioReport)
                if new_scenario:
                    st.session_state['scenario_obj'] = new_scenario
                    update_exports()
                    st.rerun()
            
    with tab2:
        st.subheader("Simulated MDR Investigation")
        st.info("This output mimics the Case Details view a customer would receive in Sophos Central.")
        st.write(mdr_case)
        
        st.divider()
        if st.button("🔄 Regenerate MDR Log", use_container_width=True):
            with st.spinner("Regenerating the MDR case log..."):
                c_prompt = build_mdr_case_prompt(st.session_state['client_inputs'], st.session_state['scenario_obj'].narrative)
                new_mdr = app_engine.call_llm_text(c_prompt)
                st.session_state['mdr_case'] = new_mdr
                update_exports()
                st.rerun()
        
    with tab3:
        st.subheader("Recommended Security Testing & Advisory")
        for rec in recs:
            if rec.startswith("🛡️") or rec.startswith("⚙️"):
                st.markdown(f"#### {rec}")
            else:
                st.markdown(rec)
        
    st.divider()
    
    # Show buttons independently using 'or' instead of 'and'
    if st.session_state.get('pdf_bytes') or st.session_state.get('pptx_bytes'):
        st.subheader("📥 Export Client Deliverables")
        dl_col1, dl_col2 = st.columns(2)
        
        with dl_col1:
            if st.session_state.get('pdf_bytes'):
                st.download_button(
                    label="📄 Download PDF Report",
                    data=st.session_state['pdf_bytes'],
                    file_name=f"{cached_customer_name.replace(' ', '_')}_MDR_Report.pdf",
                    mime="application/pdf"
                )
            
        with dl_col2:
            if st.session_state.get('pptx_bytes'):
                st.download_button(
                    label="📊 Download PowerPoint Deck",
                    data=st.session_state['pptx_bytes'],
                    file_name=f"{cached_customer_name.replace(' ', '_')}_MDR_Deck.pptx",
                    mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
                )