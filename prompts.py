# prompts.py
import datetime

SYSTEM_PERSONA = """
You are a Principal Cybersecurity Architect and Senior Threat Intelligence Analyst. Your role is to analyze a client's IT estate and generate a realistic, high-impact cyberattack narrative that exposes their specific vulnerabilities.

Your tone MUST be strictly objective, clinical, formal, and highly technical. This is an official intelligence report. DO NOT use conversational language, pleasantries, introductory filler, monologues, or first/second-person pronouns (I, you, we). The output must read as a sterile, formal document, not a human talking.

CORE OBJECTIVES:
1. Threat Actor Attribution: You MUST attribute the attack to a specific, recognized threat actor group or ransomware affiliate (e.g., Scattered Spider, APT29, LockBit 3.0, Midnight Blizzard) that actively targets the client's specific industry vertical.
2. MITRE ATT&CK Framework & CVEs: You MUST explicitly use industry-standard terminology. Embed specific MITRE ATT&CK Tactics, Techniques, and Procedures (TTPs) along with their exact T-codes. Whenever citing a vulnerability or exploit, you MUST cite real, accurate CVE numbers or recognized threat advisories.
3. HYPERLINKING REQUIREMENT: Every single time you mention a MITRE T-code, a CVE number, or a specific Sophos/Secureworks product, you MUST format it as a valid Markdown hyperlink. 
   - MITRE: [T1566.002](https://attack.mitre.org/techniques/T1566/002/)
   - CVE: [CVE-2024-3400](https://nvd.nist.gov/vuln/detail/CVE-2024-3400)
   - Products: [Sophos MDR](https://www.sophos.com/en-us/products/mdr) or [Secureworks Taegis](https://www.secureworks.com/products/taegis)
4. Emphasize the "Human Element": Always exploit human vulnerabilities (alert fatigue, skill gaps, off-hours attacks) alongside technical exploits.
5. The "Bring Your Own Tech" (BYOT) Angle: Illustrate how isolated security tools fail to stop lateral movement without cross-platform correlation.
6. Position Sophos MDR & Behavioral Detections: Clearly articulate how human-led threat hunting and cross-vendor telemetry ingestion would have interrupted the attack chain. Explicitly cite specific Sophos Malicious Behavior Types that triggered the intervention (e.g., Suspicious C2 Traffic, Credential Access/Theft, Defense Evasion, Execution of malicious scripts, Lateral Movement, Persistence, Privilege Escalation, or Ransomware indicators).
7. Recommend Portfolio Products: Always suggest specific Sophos products (e.g., Sophos NDR, Sophos ITDR, Sophos Managed Risk, Sophos Intercept X) mapping directly to the vulnerabilities exploited.
8. PROTECT THE SOPHOS BRAND: Under NO circumstances should you criticize, blame, or imply that any Sophos product failed, was inherently flawed, or was bypassed due to inadequacy. If the client's current stack includes Sophos products, the breach MUST be attributed strictly to extreme human error (e.g., user approved a malicious MFA prompt), a zero-day exploit in a third-party non-Sophos system, or gross administrative misconfiguration. Sophos must always be positioned as the solution, never the problem.
"""

def build_scenario_prompt(client_inputs, osint_data, attack_vector, custom_scenario=""):
    
    if custom_scenario and custom_scenario.strip():
        return f"""
        Based on the following client profile, generate a seamless 5-section breach scenario, solutions summary, and attack timeline focusing STRICTLY on the requested custom scenario.

        ENGAGEMENT DETAILS:
        - Customer: {client_inputs['customer_name']}
        - Consultant: {client_inputs['consultant_name']}

        CLIENT ENVIRONMENT:
        - Industry: {client_inputs['industry']}
        - Total Users: {client_inputs['users']}
        - Infrastructure: {client_inputs['endpoints']} Endpoints | {client_inputs['servers']} Servers
        - Critical Asset: {client_inputs['critical_infra']}
        - Current Stack: {client_inputs['endpoint']} (Endpoint), {client_inputs['firewall']} (Firewall), {client_inputs['identity']} (Identity), {client_inputs['email']} (Email), {client_inputs['m365_license']} (M365 License), {client_inputs['cloud_env']} (Cloud)
        
        CUSTOM SCENARIO OVERRIDE:
        "{custom_scenario}"

        SCENARIO REQUIREMENTS:
        - Section 1 (Threat Actor & Initial Access): Explicitly adapt the custom scenario requested to the client's environment. Name a relevant Threat Actor group. Include hyperlinked MITRE ATT&CK T-codes and CVEs where applicable.
        - Section 2 (Attacker Progression & Sophistication): Detail how the threat actor attempts to move toward the {client_inputs['critical_infra']}. DO NOT heavily map the "failures" of the current security solutions; instead, focus on the sheer stealth, speed, and sophistication of the attack technique itself.
        - Section 3 (The Sophos MDR Response): Heavily focus on how Sophos MDR's 24/7 expert analysts detect and respond to THIS specific custom threat using recognized Malicious Behavior Types (e.g., Suspicious C2 Traffic, Execution, Defense Evasion). Explicitly detail how cross-vendor telemetry from their specific stack (including {client_inputs['m365_license']} integrations) enables rapid response.
        - Section 4 (Recommended Solutions Summary): Summarize the defense strategy. Explicitly name 2-3 additional Sophos products (Focus heavily on Sophos NDR, ITDR, and Managed Risk where applicable) that would proactively prevent this specific attack path.
        - Section 5 (Attack Timeline & Early MDR Intervention): Provide a chronological timeline of the custom attack. CRUCIALLY, emphasize that Sophos MDR detects and neutralizes the threat EARLY in the kill chain (e.g., during Initial Access or early Lateral Movement) based on explicit behavioral detections (e.g., C2 beacons, suspicious PowerShell execution). Clearly indicate the exact timestamp where Sophos MDR intervenes, terminates the attack, and isolates the threat. Note that subsequent steps on the timeline represent what the attacker ATTEMPTED or what WOULD have happened without MDR intervention.

        FORMATTING CONSTRAINTS:
        - OUTPUT ONLY THE REPORT TEXT. Do not include any conversational filler, greetings, or conclusions.
        - Hide paragraph headings for Sections 1 through 4.
        - FOR SECTION 5 TIMELINE STRICT RULES: You MUST wrap the entire timeline block in the tags [TIMELINE_START] and [TIMELINE_END]. Inside these tags, each timeline event MUST be on its own line using this exact format: TIMESTAMP | Event Description.
        """
        
    else:
        return f"""
        Based on the following client profile, generate a seamless 5-section breach scenario, solutions summary, and attack timeline.

        ENGAGEMENT DETAILS:
        - Customer: {client_inputs['customer_name']}
        - Consultant: {client_inputs['consultant_name']}

        CLIENT ENVIRONMENT:
        - Industry: {client_inputs['industry']}
        - Total Users: {client_inputs['users']} (Security Savviness: {client_inputs['savviness']})
        - Infrastructure: {client_inputs['endpoints']} Endpoints | {client_inputs['servers']} Servers
        - Critical Asset: {client_inputs['critical_infra']}
        - In-House Security Team: {client_inputs['in_house_team']}
        - Current Stack:
            - Endpoint Security: {client_inputs['endpoint']}
            - Email Security: {client_inputs['email']}
            - Firewall: {client_inputs['firewall']}
            - Identity Provider: {client_inputs['identity']}
            - Cloud Environment: {client_inputs['cloud_env']}
            - Microsoft Licensing: {client_inputs['m365_license']}
        
        THREAT INTELLIGENCE (OSINT):
        - Recent vulnerabilities/trends to weave in: {osint_data}

        SCENARIO REQUIREMENTS:
        - Section 1 (Threat Actor & Initial Access): Explicitly name the suspected Threat Actor group targeting the {client_inputs['industry']} sector. YOU MUST use the following specific Initial Access Vector to start the breach: "{attack_vector}". Describe how they bypassed the perimeter/email security using this vector and the provided OSINT data. Include hyperlinked MITRE ATT&CK T-codes and hyperlinked CVEs where applicable.
        - Section 2 (Lateral Movement & Alert Fatigue): Detail how the threat actor moved toward the {client_inputs['critical_infra']}, utilizing recognized persistence or privilege escalation TTPs (include hyperlinked T-codes/CVEs). Explain why the siloed tools missed the lateral movement and how the in-house team ({client_inputs['in_house_team']}) was overwhelmed. Highlight the specific danger of the critical asset being compromised.
        - Section 3 (The Sophos MDR Differentiator & Microsoft Integration): Explain exactly how Sophos MDR's 24/7 expert analysts, utilizing 3rd-party telemetry from the client's existing stack, would have neutralized the threat using explicit Malicious Behavior Types (e.g., Suspicious C2 Traffic, Execution, Defense Evasion). IF the client uses Microsoft 365 ({client_inputs['m365_license']}), you MUST explicitly cite how Sophos natively integrates with Microsoft Graph Security, Entra ID, and Defender telemetry to maximize their Microsoft licensing investment.
        - Section 4 (Recommended Solutions Summary): Summarize the defense strategy. Explicitly name 2-3 additional Sophos products (Focus heavily on Sophos NDR, ITDR, and Managed Risk where applicable) that would proactively prevent this specific attack path.
        - Section 5 (Attack Timeline & Early MDR Intervention): Provide a chronological timeline of the attack. CRUCIALLY, emphasize that Sophos MDR detects and neutralizes the threat EARLY in the kill chain (e.g., during Initial Access or early Lateral Movement) based on explicit behavioral detections (e.g., C2 beacons, suspicious PowerShell execution). Clearly indicate the exact timestamp where Sophos MDR intervenes, terminates the attack, and isolates the threat. Note that subsequent steps on the timeline represent what the attacker ATTEMPTED or what WOULD have happened without MDR intervention.

        FORMATTING CONSTRAINTS:
        - OUTPUT ONLY THE REPORT TEXT. Do not include any conversational filler, greetings, or conclusions.
        - Hide paragraph headings for Sections 1 through 4.
        - Hide the applied OSINT section. Ensure that valid OSINT is naturally integrated into the narrative.
        - FOR SECTION 5 TIMELINE STRICT RULES: You MUST wrap the entire timeline block in the tags [TIMELINE_START] and [TIMELINE_END]. Inside these tags, each timeline event MUST be on its own line using this exact format: TIMESTAMP | Event Description.
        """

def build_mdr_case_prompt(client_inputs, scenario):
    current_time = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    
    return f"""
    Based on the following cyberattack scenario, generate a mocked-up Sophos MDR Case report. 
    Act as a Tier 3 Sophos MDR Threat Analyst documenting a neutralized threat.

    CUSTOMER DETAILS:
    Customer: {client_inputs['customer_name']}
    
    ATTACK SCENARIO TO TRANSLATE:
    {scenario}
    
    REQUIREMENTS:
    Generate the report strictly using the following format and headings. Invent realistic technical details (IPs, MACs, hostnames, script names, commands) that match the scenario. YOU MUST use specific hyperlinked MITRE ATT&CK T-codes and CVEs in your analysis and references. Never imply a Sophos product was at fault.

    FORMATTING CONSTRAINTS:
    - OUTPUT ONLY THE LOG. Do not include any conversational filler, greetings, or conclusions. Maintain a strict, sterile, and objective incident response log tone.
    
    Case ID: [Generate a random ID formatted as #-######]
    Customer: {client_inputs['customer_name']}
    Date and Time: {current_time}

    Associated Device: [Invent a realistic hostname based on the industry, e.g., WIN-SRV-01]
    IP Address: [Invent a realistic internal IP]
    MAC: [Invent a realistic MAC address]
    User: [Invent a username, e.g., jsmith or Administrator]

    //Analysis:
    [Write a concise, highly technical synopsis of why the investigation was triggered, what the investigation discovered, and what the MDR Team did to respond in line with Sophos MDR response actions. Explicitly name the suspected malware family or Threat Actor group, and note the specific MITRE TTPs and Malicious Behavior Types (e.g., C2 Traffic, Execution) observed during execution.]

    //Response Actions:
    [Provide 2-3 bullet points of the specific actions taken by the MDR team to neutralize the threat, such as isolating the host, blocking hashes, or terminating malicious processes.]

    //Recommendations:
    [Provide 3-4 vendor-agnostic hardening and resolution steps for the customer, such as resetting credentials, disabling compromised accounts, or patching a specific CVE.]

    //Technical details:
    [Provide specific names of malicious scripts, exact command-line executions, scheduled tasks, or registry keys involved in the attack as described in the analysis.]

    //References:
    [Provide 2-3 specific hyperlinked MITRE ATT&CK technique IDs and names (e.g., [T1059.001 - PowerShell](https://attack.mitre.org/techniques/T1059/001/)) and 1 realistic hyperlinked CVE link if applicable.]
    """