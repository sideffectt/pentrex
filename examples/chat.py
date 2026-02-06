"""Interactive Pentrex session with colored output."""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pentrex import Agent, Config


# Terminal colors
class C:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    MAGENTA = '\033[95m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    RESET = '\033[0m'


def banner():
    print(f"""
{C.CYAN}{C.BOLD}
    ██████╗ ███████╗███╗   ██╗████████╗██████╗ ███████╗██╗  ██╗
    ██╔══██╗██╔════╝████╗  ██║╚══██╔══╝██╔══██╗██╔════╝╚██╗██╔╝
    ██████╔╝█████╗  ██╔██╗ ██║   ██║   ██████╔╝█████╗   ╚███╔╝ 
    ██╔═══╝ ██╔══╝  ██║╚██╗██║   ██║   ██╔══██╗██╔══╝   ██╔██╗ 
    ██║     ███████╗██║ ╚████║   ██║   ██║  ██║███████╗██╔╝ ██╗
    ╚═╝     ╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
{C.RESET}
    {C.DIM}Cybersecurity Learning Assistant{C.RESET}
    {C.DIM}{'─' * 45}{C.RESET}
    
    {C.YELLOW}Commands:{C.RESET}
      {C.GREEN}•{C.RESET} quiz [domain]   {C.DIM}- Sınav yap{C.RESET}
      {C.GREEN}•{C.RESET} explain [topic] {C.DIM}- Kavram açıkla{C.RESET}
      {C.GREEN}•{C.RESET} tool [name]     {C.DIM}- Araç rehberi{C.RESET}
      {C.GREEN}•{C.RESET} scenario [name] {C.DIM}- Saldırı senaryosu{C.RESET}
      {C.GREEN}•{C.RESET} reset           {C.DIM}- Sohbeti sıfırla{C.RESET}
      {C.GREEN}•{C.RESET} quit            {C.DIM}- Çıkış{C.RESET}
    
    {C.DIM}{'─' * 45}{C.RESET}
    """)


def format_text(text):
    """Add colors to response text."""
    lines = []
    for line in text.split('\n'):
        stripped = line.strip()
        
        # Headers
        if stripped.startswith('#'):
            lines.append(f"\n    {C.CYAN}{C.BOLD}{stripped.replace('#', '').strip()}{C.RESET}")
        # Bullet points
        elif stripped.startswith(('•', '-', '*', '►')):
            content = stripped[1:].strip()
            lines.append(f"      {C.GREEN}►{C.RESET} {content}")
        # Numbered lists
        elif stripped and stripped[0].isdigit() and len(stripped) > 1 and stripped[1] in '.)':
            lines.append(f"      {C.YELLOW}{stripped}{C.RESET}")
        # Code blocks
        elif stripped.startswith('`') or stripped.startswith('$'):
            lines.append(f"      {C.MAGENTA}{stripped}{C.RESET}")
        # Normal text
        elif stripped:
            lines.append(f"    {stripped}")
        else:
            lines.append("")
    
    return '\n'.join(lines)


def main():
    config = Config()
    
    if not config.api_key:
        print(f"\n  {C.RED}✗ API key bulunamadı{C.RESET}")
        print(f"  {C.DIM}.env dosyası oluştur:{C.RESET} {C.YELLOW}ANTHROPIC_API_KEY=your-key{C.RESET}\n")
        sys.exit(1)

    agent = Agent(config)
    banner()

    while True:
        try:
            query = input(f"  {C.GREEN}{C.BOLD}you ➜{C.RESET}  ").strip()
        except (EOFError, KeyboardInterrupt):
            print(f"\n\n  {C.DIM}Görüşürüz! 👋{C.RESET}\n")
            break

        if not query:
            continue
            
        if query.lower() in ("quit", "exit", "q", "çıkış"):
            print(f"\n  {C.DIM}Görüşürüz! 👋{C.RESET}\n")
            break
            
        if query.lower() in ("reset", "sıfırla"):
            agent.reset()
            print(f"  {C.YELLOW}[sohbet sıfırlandı]{C.RESET}\n")
            continue

        # Show thinking indicator
        print(f"  {C.DIM}düşünüyor...{C.RESET}", end='\r')
        
        response = agent.chat(query)
        
        # Clear thinking line and show response
        print(f"  {' ' * 20}", end='\r')
        print(f"\n  {C.CYAN}{C.BOLD}pentrex ➜{C.RESET}\n")
        print(format_text(response))
        print(f"\n  {C.DIM}{'─' * 45}{C.RESET}\n")


if __name__ == "__main__":
    main()
