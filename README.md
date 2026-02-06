# Pentrex

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Claude API](https://img.shields.io/badge/Claude-API-orange.svg)](https://anthropic.com)
[![CEH](https://img.shields.io/badge/CEH-v12-red.svg)](https://www.eccouncil.org/train-certify/certified-ethical-hacker-ceh/)
[![Contributions Welcome](https://img.shields.io/badge/Contributions-Welcome-brightgreen.svg)](https://github.com/sideffect0/pentrex/issues)

AI-powered cybersecurity learning assistant. Quiz yourself, explore attack techniques, and master penetration testing concepts through an interactive agent.

<p align="center">
  <img src="https://img.shields.io/badge/🔐_Security-Learning-purple?style=for-the-badge" />
  <img src="https://img.shields.io/badge/🎯_CEH-Prep-red?style=for-the-badge" />
  <img src="https://img.shields.io/badge/🤖_AI-Powered-blue?style=for-the-badge" />
</p>

---

## 🚀 Features

| Feature | Description |
|---------|-------------|
| 🧠 **Quiz Mode** | Test your knowledge across 7 CEH domains |
| 📚 **Explain Mode** | Deep-dive into security concepts (SQLi, XSS, Buffer Overflow...) |
| 🛠️ **Tool Guide** | Learn Nmap, Metasploit, Burp Suite, Wireshark and more |
| 🎮 **Scenario Mode** | Practice with realistic attack walkthroughs |

## 📦 Quick Start

```bash
git clone https://github.com/sideffectt/pentrex.git
cd pentrex

pip install -r requirements.txt
```

### 🔑 Getting an API Key

This project uses Claude API. Two options:

**Option 1:** Get your own key at [console.anthropic.com](https://console.anthropic.com)

**Option 2:** Request a shared key for testing — [open an issue](https://github.com/sideffect0/pentrex/issues/new)

Once you have a key:

```bash
echo "ANTHROPIC_API_KEY=your-key-here" > .env
python3 examples/chat.py
```

### 💻 CLI Mode (No API Key Needed)

You can use the quiz, tools, and scenarios without an API key:

```bash
python3 -m pentrex.cli
```

---

## 🎯 CEH Domains Covered

- 🔍 Reconnaissance & Footprinting
- 📡 Scanning & Enumeration
- 💻 System Hacking
- 🌐 Web Application Attacks
- 🔌 Network Attacks
- 📶 Wireless Security
- 🔐 Cryptography

## 🛠️ Tools Included

| Tool | Category |
|------|----------|
| Nmap | Scanning |
| Metasploit | Exploitation |
| Burp Suite | Web Testing |
| Wireshark | Network Analysis |
| SQLmap | SQL Injection |
| Hydra | Password Cracking |
| Aircrack-ng | Wireless |
| John the Ripper | Hash Cracking |

## 💬 Example

```
you > explain sql injection

pentrex > SQL Injection is a code injection technique that exploits 
vulnerabilities in data-driven applications. When user input isn't 
properly sanitized, attackers can inject malicious SQL statements...

you > quiz me on network attacks

pentrex > What protocol does ARP Spoofing target?
A) TCP
B) UDP  
C) ARP
D) ICMP

you > c

pentrex > Correct! ARP operates at Layer 2 and has no built-in 
authentication, making it vulnerable to spoofing attacks...
```

## 📁 Project Structure

```
pentrex/
├── pentrex/
│   ├── loop.py           # AI Agent loop
│   ├── config.py         # Configuration
│   └── tools/
│       ├── quiz.py       # 21+ quiz questions
│       ├── explain.py    # 6 security concepts
│       ├── toolguide.py  # 8 pentest tools
│       └── scenario.py   # 4 attack scenarios
├── examples/
│   └── chat.py           # Interactive session
└── tests/
    └── test_tools.py
```

## 🤝 Contributing

Pull requests welcome! Areas that need help:

- 📝 More quiz questions
- 🔧 Additional tool guides (Nikto, Gobuster, Dirb...)
- 🎯 New attack scenarios
- 🌍 Translations
- 🐛 Bug fixes

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## ⭐ Star History

If this helped you learn, consider giving it a star!

## 📄 License

MIT — use it, learn from it, improve it.

---

<p align="center">
  Made with ❤️ for the cybersecurity community
</p>
