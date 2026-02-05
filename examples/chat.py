"""Interactive Pentrex session."""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pentrex import Agent, Config


def main():
    config = Config()
    
    if not config.api_key:
        print("Error: API key not found")
        print("Create .env file with: ANTHROPIC_API_KEY=your-key")
        sys.exit(1)

    agent = Agent(config)

    print("""
    ╔═══════════════════════════════════════╗
    ║           P E N T R E X               ║
    ║   Cybersecurity Learning Assistant    ║
    ╚═══════════════════════════════════════╝
    
    Commands:
      quiz [domain]  - Start a quiz (e.g., quiz web_attacks)
      explain [topic] - Explain a concept (e.g., explain sql injection)
      tool [name]    - Tool guide (e.g., tool nmap)
      scenario [name] - Attack walkthrough
      
      reset - Clear conversation
      quit  - Exit
    """)

    while True:
        try:
            query = input("\nyou > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            break

        if not query:
            continue
        if query.lower() in ("quit", "exit", "q"):
            print("Goodbye.")
            break
        if query.lower() == "reset":
            agent.reset()
            print("[conversation cleared]")
            continue

        response = agent.chat(query)
        print(f"\npentrex > {response}")


if __name__ == "__main__":
    main()
