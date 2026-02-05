# Pentrex

AI-powered cybersecurity learning assistant. Quiz yourself, explore attack techniques, and master penetration testing concepts through an interactive agent.

## What it does

- **Quiz mode**: Test your knowledge across CEH domains
- **Explain mode**: Deep-dive into any security concept
- **Tool guide**: Learn common pentest tools with examples
- **Scenario mode**: Practice with realistic attack scenarios

## Quick Start

```bash
git clone https://github.com/yourusername/pentrex.git
cd pentrex
pip install -r requirements.txt

export ANTHROPIC_API_KEY="your-key"
python -m examples.chat
```

## Example

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

## Project Structure

```
pentrex/
├── pentrex/
│   ├── loop.py           # Agent loop
│   ├── config.py         # Configuration
│   └── tools/
│       ├── quiz.py       # Quiz system
│       ├── explain.py    # Concept explanations
│       ├── toolguide.py  # Pentest tool reference
│       └── scenario.py   # Attack scenarios
├── examples/
│   └── chat.py           # Interactive session
└── tests/
    └── test_tools.py
```

## CEH Domains Covered

1. Information Security and Ethical Hacking
2. Reconnaissance Techniques
3. System Hacking Phases and Techniques
4. Network and Perimeter Hacking
5. Web Application Hacking
6. Wireless Network Hacking
7. Mobile Platform, IoT, and OT Hacking
8. Cloud Computing and Cryptography

## Contributing

Pull requests welcome. Areas that need help:

- More quiz questions
- Additional tool guides
- New attack scenarios
- Translations

## License

MIT
