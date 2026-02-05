#!/usr/bin/env python3
"""
Pentrex CLI - No API key needed.
Direct access to quiz, explanations, tools, and scenarios.
"""

import sys
import os
import json
import random

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pentrex.tools import run_tool


def print_header():
    print("""
    ╔═══════════════════════════════════════╗
    ║           P E N T R E X               ║
    ║   Cybersecurity Learning Assistant    ║
    ╚═══════════════════════════════════════╝
    """)


def print_help():
    print("""
    Commands:
    
      quiz [domain]     Quiz from domain (or 'random')
                        Domains: reconnaissance, scanning, system_hacking,
                                 web_attacks, network_attacks, wireless, cryptography
      
      explain [topic]   Explain a security concept
                        Topics: sql_injection, xss, arp_spoofing, 
                                buffer_overflow, phishing, mitm
      
      tool [name]       Show tool guide
                        Tools: nmap, metasploit, burp_suite, wireshark,
                               sqlmap, hydra, aircrack, john
      
      scenario [name]   Attack walkthrough
                        Scenarios: web_sql_injection, network_arp_spoofing,
                                   wireless_wpa_crack, system_privilege_escalation
      
      list              Show all available content
      help              Show this message
      quit              Exit
    """)


def cmd_quiz(args):
    domain = args[0] if args else "random"
    
    result = run_tool("get_quiz_question", {"domain": domain})
    
    if "error" in result:
        print(f"\n  Error: {result['error']}")
        print(f"  Available: {', '.join(result['available'])}")
        return
    
    print(f"\n  [{result['domain'].upper()}]")
    print(f"\n  {result['question']}\n")
    
    for letter, option in result['options'].items():
        print(f"    {letter}) {option}")
    
    answer = input("\n  Your answer (A/B/C/D): ").strip().upper()
    
    correct_letter = ['A', 'B', 'C', 'D'][result['correct_index']]
    
    if answer == correct_letter:
        print("\n  ✓ Correct!")
    else:
        print(f"\n  ✗ Wrong. Correct answer: {correct_letter}")
    
    print(f"\n  Explanation: {result['explanation']}")


def cmd_explain(args):
    if not args:
        result = run_tool("list_concepts", {})
        print("\n  Available concepts:")
        for c in result['concepts']:
            print(f"    - {c['key']}: {c['name']} ({c['category']})")
        return
    
    concept = args[0]
    result = run_tool("explain_concept", {"concept": concept})
    
    if "error" in result:
        print(f"\n  Error: {result['error']}")
        print(f"  Available: {', '.join(result['available'])}")
        return
    
    print(f"\n  {result['name']}")
    print(f"  Category: {result['category']}")
    print(f"\n  {result['description']}")
    
    if "how_it_works" in result:
        print("\n  How it works:")
        for i, step in enumerate(result['how_it_works'], 1):
            print(f"    {i}. {step}")
    
    if "prevention" in result:
        print("\n  Prevention:")
        for p in result['prevention']:
            print(f"    • {p}")
    
    if "tools" in result:
        print(f"\n  Tools: {', '.join(result['tools'])}")


def cmd_tool(args):
    if not args:
        result = run_tool("list_tools", {})
        print("\n  Available tools:")
        for t in result['tools']:
            print(f"    - {t['key']}: {t['name']} ({t['category']})")
        return
    
    tool = args[0]
    result = run_tool("get_tool_guide", {"tool": tool})
    
    if "error" in result:
        print(f"\n  Error: {result['error']}")
        print(f"  Available: {', '.join(result['available'])}")
        return
    
    print(f"\n  {result['name']}")
    print(f"  Category: {result['category']}")
    print(f"\n  {result['description']}")
    
    if "common_flags" in result:
        print("\n  Common flags:")
        for flag, desc in result['common_flags'].items():
            print(f"    {flag}: {desc}")
    
    if "key_commands" in result:
        print("\n  Key commands:")
        for cmd, desc in result['key_commands'].items():
            print(f"    {cmd}: {desc}")
    
    if "examples" in result:
        print("\n  Examples:")
        for ex in result['examples'][:4]:
            print(f"    # {ex['desc']}")
            print(f"    {ex['cmd']}\n")


def cmd_scenario(args):
    if not args:
        result = run_tool("list_scenarios", {})
        print("\n  Available scenarios:")
        for s in result['scenarios']:
            print(f"    - {s['key']}: {s['title']} [{s['difficulty']}]")
        return
    
    scenario = args[0]
    result = run_tool("get_scenario", {"scenario": scenario})
    
    if "error" in result:
        print(f"\n  Error: {result['error']}")
        print(f"  Available: {', '.join(result['available'])}")
        return
    
    print(f"\n  {result['title']}")
    print(f"  Difficulty: {result['difficulty']}")
    print(f"  Category: {result['category']}")
    
    setup = result['setup']
    print(f"\n  Target: {setup['target']}")
    print(f"  Objective: {setup['objective']}")
    print(f"  Tools: {', '.join(setup['tools_needed'])}")
    
    print("\n  Steps:")
    for step in result['steps']:
        print(f"\n  [{step['step']}] {step['task']}")
        if 'command' in step:
            print(f"      $ {step['command']}")
        if 'commands' in step:
            for cmd in step['commands']:
                print(f"      $ {cmd}")
        if 'hint' in step:
            print(f"      Hint: {step['hint']}")
    
    print("\n  Lessons learned:")
    for lesson in result['lessons']:
        print(f"    • {lesson}")


def cmd_list(_):
    print("\n  === Quiz Domains ===")
    result = run_tool("list_quiz_domains", {})
    for domain, count in result['domains'].items():
        print(f"    {domain}: {count} questions")
    
    print("\n  === Concepts ===")
    result = run_tool("list_concepts", {})
    for c in result['concepts']:
        print(f"    {c['key']}: {c['name']}")
    
    print("\n  === Tools ===")
    result = run_tool("list_tools", {})
    for t in result['tools']:
        print(f"    {t['key']}: {t['name']}")
    
    print("\n  === Scenarios ===")
    result = run_tool("list_scenarios", {})
    for s in result['scenarios']:
        print(f"    {s['key']}: {s['title']}")


def main():
    print_header()
    print("  Type 'help' for commands, 'quit' to exit.\n")
    
    commands = {
        'quiz': cmd_quiz,
        'explain': cmd_explain,
        'tool': cmd_tool,
        'scenario': cmd_scenario,
        'list': cmd_list,
        'help': lambda _: print_help(),
    }
    
    while True:
        try:
            line = input("  pentrex > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n  Goodbye.")
            break
        
        if not line:
            continue
        
        parts = line.split()
        cmd = parts[0].lower()
        args = parts[1:]
        
        if cmd in ('quit', 'exit', 'q'):
            print("  Goodbye.")
            break
        
        if cmd in commands:
            commands[cmd](args)
        else:
            print(f"  Unknown command: {cmd}")
            print("  Type 'help' for available commands.")


if __name__ == "__main__":
    main()
