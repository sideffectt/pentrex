"""Attack playbooks — structured pentest workflows."""

PLAYBOOKS = {
    "web_recon": {
        "name": "Web Reconnaissance",
        "description": "Full web target reconnaissance: DNS, subdomains, tech stack, open ports.",
        "steps": [
            "Run DNS enumeration on {target} to find subdomains and records",
            "Run nmap quick scan on {target} to identify open ports and services",
            "Check HTTP headers and identify web technologies on {target}",
            "Look for common files: robots.txt, sitemap.xml, .well-known on {target}",
            "Save all findings as notes with category 'recon'",
            "Summarize the attack surface found",
        ],
    },
    "network_scan": {
        "name": "Network Scan",
        "description": "Network enumeration: host discovery, port scanning, service identification.",
        "steps": [
            "Run host discovery on {target} network range",
            "For each live host, run service version detection",
            "Identify potential vulnerabilities based on service versions",
            "Check for default credentials on discovered services",
            "Save all findings as notes",
            "Generate summary of network topology and findings",
        ],
    },
    "vuln_scan": {
        "name": "Vulnerability Scan",
        "description": "Identify vulnerabilities on target using nmap scripts and analysis.",
        "steps": [
            "Run nmap vulnerability scan (vuln profile) on {target}",
            "Analyze results for known CVEs",
            "Check service versions against known vulnerable versions",
            "Save vulnerabilities found with severity ratings",
            "Suggest exploitation paths based on findings",
        ],
    },
    "web_vuln": {
        "name": "Web Vulnerability Assessment",
        "description": "Test web application for common vulnerabilities.",
        "steps": [
            "Identify web technologies and frameworks on {target}",
            "Check for common misconfigurations (directory listing, default creds)",
            "Test for information disclosure (error pages, headers, comments)",
            "Check SSL/TLS configuration",
            "Save all findings as vulnerability notes",
            "Provide remediation suggestions",
        ],
    },
}


def get_playbook(name: str) -> dict | None:
    return PLAYBOOKS.get(name)


def list_playbooks() -> list:
    return [
        {"name": k, "description": v["description"]}
        for k, v in PLAYBOOKS.items()
    ]


def build_playbook_task(name: str, target: str) -> str:
    """Build an agent task from a playbook."""
    pb = PLAYBOOKS.get(name)
    if not pb:
        return ""

    steps = [s.replace("{target}", target) for s in pb["steps"]]
    numbered = "\n".join(f"{i+1}. {s}" for i, s in enumerate(steps))

    return f"""Execute this playbook: {pb['name']}
Target: {target}

Steps:
{numbered}

Execute each step sequentially. Save findings along the way. Adapt if something fails."""
