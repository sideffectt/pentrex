"""Quiz system for CEH domains."""

import random
from pentrex.tools.registry import register

QUESTIONS = {
    "reconnaissance": [
        {
            "q": "Which tool is primarily used for DNS enumeration?",
            "options": ["Nmap", "DNSrecon", "Metasploit", "Burp Suite"],
            "answer": 1,
            "explanation": "DNSrecon is designed for DNS enumeration — discovering subdomains, zone transfers, and DNS records."
        },
        {
            "q": "What is the first phase of ethical hacking?",
            "options": ["Scanning", "Reconnaissance", "Gaining Access", "Enumeration"],
            "answer": 1,
            "explanation": "Reconnaissance (footprinting) is always the first phase — gathering info about the target before active testing."
        },
        {
            "q": "Which Google dork finds login pages?",
            "options": ["site:target.com", "inurl:admin login", "filetype:pdf", "cache:target.com"],
            "answer": 1,
            "explanation": "inurl:admin login searches for URLs containing admin login pages indexed by Google."
        },
        {
            "q": "What does OSINT stand for?",
            "options": ["Open Source Intelligence", "Operating System Interface", "Online Security Integration", "Open System Interconnection"],
            "answer": 0,
            "explanation": "OSINT is intelligence collected from publicly available sources — social media, DNS records, public databases."
        },
    ],
    "network_attacks": [
        {
            "q": "What protocol does ARP Spoofing target?",
            "options": ["TCP", "UDP", "ARP", "ICMP"],
            "answer": 2,
            "explanation": "ARP operates at Layer 2 with no built-in authentication, making it vulnerable to spoofing attacks."
        },
        {
            "q": "Which attack floods a target with SYN packets?",
            "options": ["Ping of Death", "SYN Flood", "Smurf Attack", "Teardrop"],
            "answer": 1,
            "explanation": "SYN Flood exploits TCP handshake by sending many SYN packets without completing the connection."
        },
        {
            "q": "What tool is used for MITM attacks on local networks?",
            "options": ["Nmap", "Wireshark", "Ettercap", "Netcat"],
            "answer": 2,
            "explanation": "Ettercap is specifically designed for man-in-the-middle attacks on LAN, including ARP poisoning."
        },
        {
            "q": "What port does SSH typically use?",
            "options": ["21", "22", "23", "25"],
            "answer": 1,
            "explanation": "SSH uses port 22 by default. FTP is 21, Telnet is 23, SMTP is 25."
        },
    ],
    "web_attacks": [
        {
            "q": "What is the primary defense against SQL Injection?",
            "options": ["Firewalls", "Parameterized queries", "HTTPS", "Rate limiting"],
            "answer": 1,
            "explanation": "Parameterized queries (prepared statements) separate SQL code from data, preventing injection."
        },
        {
            "q": "Which HTTP header prevents clickjacking?",
            "options": ["X-Content-Type", "X-Frame-Options", "Content-Security-Policy", "X-XSS-Protection"],
            "answer": 1,
            "explanation": "X-Frame-Options controls whether a page can be embedded in iframes, preventing clickjacking."
        },
        {
            "q": "What type of XSS is stored on the server?",
            "options": ["Reflected XSS", "Stored XSS", "DOM-based XSS", "Self XSS"],
            "answer": 1,
            "explanation": "Stored (persistent) XSS saves the payload on the server, executing for every user who views the page."
        },
        {
            "q": "What does OWASP stand for?",
            "options": ["Open Web Application Security Project", "Online Web Attack Security Protocol", "Open Wireless Application Standard", "Offensive Web Assessment Platform"],
            "answer": 0,
            "explanation": "OWASP maintains the Top 10 web security risks list and provides free security tools and guides."
        },
    ],
    "system_hacking": [
        {
            "q": "What is privilege escalation?",
            "options": ["Gaining initial access", "Moving from low to high privileges", "Lateral movement", "Data exfiltration"],
            "answer": 1,
            "explanation": "Privilege escalation is gaining higher access levels than originally granted — going from user to root/admin."
        },
        {
            "q": "Which tool is commonly used for password cracking?",
            "options": ["Nmap", "John the Ripper", "Wireshark", "Nikto"],
            "answer": 1,
            "explanation": "John the Ripper supports multiple hash types and cracking methods — dictionary, brute force, rainbow tables."
        },
        {
            "q": "What does a rootkit do?",
            "options": ["Scans for open ports", "Hides malicious activity from detection", "Encrypts files for ransom", "Creates backdoor accounts"],
            "answer": 1,
            "explanation": "Rootkits hide their presence and other malware from system monitoring tools, maintaining persistent access."
        },
    ],
    "wireless": [
        {
            "q": "Which wireless encryption is considered most secure?",
            "options": ["WEP", "WPA", "WPA2", "WPA3"],
            "answer": 3,
            "explanation": "WPA3 uses SAE (Simultaneous Authentication of Equals), providing stronger protection against offline attacks."
        },
        {
            "q": "What tool captures wireless handshakes?",
            "options": ["Nmap", "Aircrack-ng", "Burp Suite", "SQLmap"],
            "answer": 1,
            "explanation": "Aircrack-ng suite (specifically airodump-ng) captures WPA handshakes for offline cracking."
        },
    ],
}

ALL_DOMAINS = list(QUESTIONS.keys())


def _format_question(q: dict, domain: str) -> str:
    """Format a question for display."""
    letters = ["A", "B", "C", "D"]
    lines = [f"[{domain}] {q['q']}\n"]
    for i, opt in enumerate(q["options"]):
        lines.append(f"  {letters[i]}) {opt}")
    lines.append(f"\nAnswer: {letters[q['answer']]})")
    lines.append(f"Explanation: {q['explanation']}")
    return "\n".join(lines)


@register(
    name="quiz",
    description="Get a quiz question from a CEH domain. Domains: reconnaissance, network_attacks, web_attacks, system_hacking, wireless. Use 'random' for any domain.",
    parameters={
        "domain": {
            "type": "string",
            "description": "Quiz domain or 'random'"
        },
        "count": {
            "type": "integer",
            "description": "Number of questions (1-5)"
        },
    },
    required=[],
)
def quiz(domain: str = "random", count: int = 1) -> dict:
    count = min(max(count, 1), 5)

    if domain == "random" or domain not in QUESTIONS:
        pool = []
        for d, qs in QUESTIONS.items():
            for q in qs:
                pool.append((d, q))
    else:
        pool = [(domain, q) for q in QUESTIONS[domain]]

    selected = random.sample(pool, min(count, len(pool)))
    formatted = [_format_question(q, d) for d, q in selected]

    return {
        "questions": formatted,
        "domains_available": ALL_DOMAINS,
        "total_questions": sum(len(v) for v in QUESTIONS.values()),
    }
