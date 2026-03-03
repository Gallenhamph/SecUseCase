# data.py

ATTACK_VECTORS = [
    # Phishing / Social Engineering
    "Highly targeted spear-phishing campaign using a malicious PDF attachment (T1566.001)",
    "Adversary-in-the-Middle (AiTM) proxy attack defeating standard MFA via a fake login page (T1556)",
    "Voice Phishing (Vishing) the IT Helpdesk to fraudulently reset a user's MFA device (T1566.004)",
    "Social engineering via LinkedIn/Slack delivering a malicious payload disguised as a resume (T1566.003)",
    "Spear-phishing utilizing HTML Smuggling to deliver a malicious ISO archive bypassing email attachment filters (T1027.006)",
    "QR Code Phishing (Quishing) evading URL inspection by routing mobile devices to a credential harvesting proxy (T1566)",
    "Drive-by compromise via SEO poisoning (Malvertising) directing a user to a trojanized software installer (T1189)",
    
    # Perimeter / Edge Exploitation
    "Exploitation of a zero-day vulnerability in a public-facing web application (T1190)",
    "Exploitation of an unpatched, legacy VPN appliance leading to internal access (T1133)",
    "Password spraying attack against legacy authentication protocols lacking MFA enforcement (T1110.003)",
    "Default credentials left active on an internet-facing IoT or edge network device (T1078.001)",
    "Brute-force dictionary attack against an unintentionally exposed RDP jump server (T1110.001)",
    
    # Supply Chain / Third Party
    "Compromised third-party IT contractor / Supply Chain Compromise via remote access tools (T1195)",
    "Malicious update pushed through a compromised third-party software vendor (T1195.002)",
    "Lateral pivot into the network originating from a compromised trusted vendor's environment (T1199)",
    "Abuse of compromised Managed Service Provider (MSP) remote monitoring and management (RMM) tools (T1195)",
    "Supply chain compromise via malicious code injected into a trusted open-source NPM/PyPI library used by the internal dev team (T1195.001)",
    
    # Identity / Cloud
    "Compromised Cloud Infrastructure via hardcoded API keys accidentally leaked on GitHub (T1078.004)",
    "Session hijacking via stolen browser cookies purchased on the dark web, bypassing MFA entirely (T1539)",
    "MFA Fatigue (Push Bombing) attack against a senior executive's compromised credentials (T1621)",
    "Illicit consent grant via a malicious Microsoft 365 / Google Workspace OAuth application (T1528)",
    "Exploitation of a publicly exposed, misconfigured cloud storage bucket containing administrative credentials (T1078.004)",
    
    # Physical / Insider / BYOD
    "Malicious insider abusing legitimate administrative privileges to disable security tooling (T1078.003)",
    "Physical 'USB Drop' attack in the company parking lot leading to a reverse shell beacon (T1200)",
    "Initial access originating from a user's malware-infected personal BYOD device connecting to the corporate network (T1133)",
    "Physical intrusion deploying a rogue hidden network implant (e.g., LAN Turtle) in a remote branch office (T1200)"
]

SIMULATED_OSINT = {
    # --- FIREWALLS ---
    "Fortinet": [
        "Active exploitation of FortiOS SSL-VPN vulnerabilities (e.g., CVE-2023-27997, CVE-2024-21762) by state-sponsored actors to deploy custom implants and bypass pre-authentication filters.",
        "Threat actors leveraging unpatched FortiGate devices (e.g., CVE-2022-42475) to establish persistent access via malicious firmware images.",
        "Widespread automated scanning and exploitation of FortiClient EMS SQL injection flaws (e.g., CVE-2023-48788) for remote code execution."
    ],
    "Palo Alto": [
        "Rising trend of threat actors exploiting unpatched PAN-OS GlobalProtect interfaces (e.g., CVE-2024-3400) to achieve unauthenticated remote code execution and establish persistent reverse shells.",
        "Targeted attacks abusing Palo Alto Expedition vulnerabilities (e.g., CVE-2024-5910) to extract administrative credentials and pivot internally.",
        "Exploitation of PAN-OS configuration vulnerabilities by APT groups to bypass authentication mechanisms and silently modify edge routing rules."
    ],
    "Cisco": [
        "Exploitation of AnyConnect and IOS XE zero-days (e.g., CVE-2023-20198), leading to privilege escalation and the deployment of malicious Lua-based web shells on edge appliances.",
        "Targeting of legacy Cisco ASA firewalls (e.g., CVE-2020-3259) to extract memory contents and valid VPN user credentials.",
        "Abuse of Cisco Secure Client vulnerabilities allowing attackers to bypass client-side posture checks and establish rogue VPN tunnels."
    ],
    "Check Point": [
        "Targeted attacks exploiting Check Point Security Gateway vulnerabilities (e.g., CVE-2024-24919) to extract Active Directory hashes and establish persistent VPN sessions.",
        "Ransomware affiliates exploiting legacy Mobile Access software blades to drop web shells into the DMZ.",
        "Privilege escalation attacks targeting Check Point Gaia OS to achieve root-level persistence prior to internal network pivoting."
    ],
    "SonicWall": [
        "Continued exploitation of SMA 100 series appliances (e.g., CVE-2021-20038) using credential stuffing and unpatched firmware to deploy ransomware directly into the DMZ.",
        "Exploitation of SonicOS access control vulnerabilities (e.g., CVE-2024-40766) allowing unauthorized users to modify firewall policies."
    ],
    "WatchGuard": [
        "Historical targeting by botnets exploiting unpatched privilege escalation flaws (e.g., CVE-2022-26318) to maintain long-term, stealthy persistence on edge devices.",
        "Exploitation of authentication bypass vulnerabilities in WatchGuard Firebox appliances to hijack active administrative sessions."
    ],
    "Barracuda": [
        "Sophisticated threat actors exploiting Email Security Gateway (ESG) zero-days (e.g., CVE-2023-2868) to deploy data exfiltration malware and backdoors.",
        "Attacks abusing misconfigured Barracuda Web Application Firewalls to tunnel C2 traffic directly through port 443."
    ],
    "Juniper": [
        "Exploitation of Junos OS J-Web vulnerabilities (e.g., CVE-2023-36844) allowing unauthenticated attackers to upload arbitrary files and execute code as root.",
        "Exploitation of SRX Series authentication bypass vulnerabilities (e.g., CVE-2024-21591) to gain full administrative control of the edge device."
    ],
    "Forcepoint": [
        "Adversaries leveraging unpatched Forcepoint VPN client vulnerabilities to escalate privileges to SYSTEM on compromised endpoints.",
        "Abuse of Forcepoint Web Security configurations to bypass DLP controls and exfiltrate compressed archives to unauthorized cloud storage."
    ],
    
    # --- ENDPOINTS ---
    "CrowdStrike": [
        "Advanced adversaries increasingly utilizing custom bootloaders and kernel-level drivers (BYOVD - Bring Your Own Vulnerable Driver) to blind Falcon sensors (Reference: Elastic Security Labs BYOVD research).",
        "Threat actors utilizing unmanaged devices on the local network to laterally move and disable Falcon services via stolen local admin credentials.",
        "Process hollowing and direct syscalls specifically crafted to bypass user-mode API hooking used by the Falcon agent."
    ],
    "Microsoft Defender": [
        "High reliance on 'Living off the Land' (LotL) techniques and obfuscated PowerShell scripts to evade standard Defender ASR rules and execute fileless malware.",
        "Threat actors actively targeting and modifying Defender exclusion paths (e.g., via Add-MpPreference) using stolen administrative privileges.",
        "Token theft techniques designed to bypass local LSA protections and extract credentials before Defender can intervene."
    ],
    "SentinelOne": [
        "Threat actors utilizing highly obfuscated, fragmented shellcode and direct syscalls to evade SentinelOne's behavioral AI engines.",
        "EDR blinding techniques involving forced safe mode reboots or manipulation of the boot configuration data to prevent the SentinelOne agent from loading."
    ],
    "Trend Micro": [
        "Exploitation of legacy Apex One vulnerabilities (e.g., CVE-2022-40139) and exploitation of exclusion lists to deploy ransomware payloads undetected.",
        "Targeting of unpatched Trend Micro endpoint agents to cause denial-of-service conditions prior to lateral movement."
    ],
    "Symantec": [
        "Bypass of legacy signature-based protections using polymorphic malware families and living-off-the-land binaries (LOLBins)."
    ],
    "Trellix": [
        "Evasion of Trellix Endpoint Security via complex process injection techniques and manipulation of trusted parent-child execution trees."
    ],
    "Blackberry Cylance": [
        "AI engine evasion via artificial payload padding and the inclusion of benign code segments to artificially lower the malicious confidence score."
    ],
    
    # --- IDENTITY ---
    "Okta": [
        "Surge in highly sophisticated Adversary-in-the-Middle (AiTM) phishing kits (e.g., Evilginx2) capturing Okta session cookies and bypassing multi-factor authentication entirely (Reference: CISA Advisory AA23-320A).",
        "Social engineering of IT Helpdesks (commonly used by Scattered Spider) to forcibly reset Okta MFA devices for targeted high-privilege users."
    ],
    "Microsoft Entra ID (Azure AD)": [
        "Widespread MFA fatigue (push bombing) attacks combined with localized brute-forcing to gain initial access to Entra ID.",
        "Illicit consent grants involving malicious OAuth applications designed to maintain persistent, hidden access to Microsoft 365 environments and mailboxes."
    ],
    "Cisco Duo": [
        "Targeting of telephony-based authentication (SMS/Voice) via SIM swapping, successfully bypassing Duo's secondary validation.",
        "Localized push-notification fatigue campaigns deployed during off-hours (1:00 AM - 4:00 AM) to wear down user defenses."
    ],
    "Ping Identity": [
        "Exploitation of historic PingFederate vulnerabilities (e.g., CVE-2021-28111) to bypass multi-factor authentication."
    ],
    
    # --- EMAIL ---
    "Mimecast": [
        "Massive increase in Quishing (QR Code Phishing) and HTML smuggling campaigns that successfully bypass Mimecast's URL rewriting and attachment sandboxing (Reference: IBM X-Force Quishing Trends).",
        "Weaponization of internal, trusted domains (Business Email Compromise) to distribute secondary payloads past Mimecast filtering."
    ],
    "Proofpoint": [
        "Threat actors leveraging highly customized, evasive PDF documents containing embedded malicious links that bypass TAP (Targeted Attack Protection) analysis.",
        "Phishing campaigns utilizing embedded CAPTCHAs inside attachments to prevent Proofpoint sandboxes from executing and analyzing the malicious code."
    ],
    "Microsoft Defender for Office 365": [
        "Bypass of SafeLinks and SafeAttachments using highly sophisticated open-redirect vulnerabilities hosted on legitimate services (e.g., Google, Adobe).",
        "Use of homoglyph domain spoofing and hijacked internal accounts to bypass standard Microsoft anti-spoofing and DMARC checks."
    ],
    
    # --- CLOUD ---
    "AWS": [
        "Exploitation of overly permissive IAM roles via SSRF vulnerabilities on public-facing EC2 instances, leading to environment-wide administrative compromise.",
        "Discovery and abuse of long-lived AWS Access Keys accidentally pushed to public GitHub repositories or left inside compromised developer environments."
    ],
    "Microsoft Azure": [
        "Abuse of Azure Automation Runbooks and extraction of Managed Identity tokens to pivot laterally across the Azure environment.",
        "Privilege escalation to Global Administrator via compromised on-premises AD Connect servers synchronizing hybrid identities."
    ],
    "GCP": [
        "Targeting of exposed service account keys embedded in developer repositories to access Google Cloud Storage buckets and BigQuery datasets.",
        "Abuse of the Google Compute Engine metadata API from compromised container workloads to extract lateral movement credentials."
    ]
}