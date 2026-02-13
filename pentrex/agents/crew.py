"""
Crew mode — multi-agent penetration testing.

Orchestrator breaks down tasks and delegates to specialized worker agents:
- ReconWorker: DNS, subdomain, OSINT gathering
- ScanWorker: Port scanning, service detection
- VulnWorker: Vulnerability identification and analysis
- ExploitWorker: Exploitation attempts and verification

The orchestrator coordinates workers, builds a knowledge graph from
findings, and makes strategic decisions about next steps.
"""

import json
from pentrex.config import Config
from pentrex.llm import LLM
from pentrex.tools import get_all_tools, run_tool
from pentrex.tools.notes import _load_notes
from pentrex.knowledge.prompts import build_crew_prompt


# Worker role definitions
WORKERS = {
    "recon": {
        "name": "ReconWorker",
        "role": "Reconnaissance Specialist",
        "prompt": """You are a reconnaissance specialist. Your job:
- DNS enumeration and subdomain discovery
- WHOIS lookups and IP range identification
- Technology stack fingerprinting
- OSINT gathering (public info, headers, certificates)
- Save ALL findings using save_note with category 'recon'

Be thorough. Every detail matters for later phases.
Target: {target}""",
        "tools": ["terminal", "nmap_scan", "save_note", "read_notes"],
    },
    "scan": {
        "name": "ScanWorker",
        "role": "Scanner",
        "prompt": """You are a network and service scanner. Your job:
- Port scanning (TCP and UDP)
- Service version detection
- OS fingerprinting
- Banner grabbing
- Save ALL findings using save_note with category 'recon'

Use nmap_scan with appropriate profiles. Be systematic.
Target: {target}""",
        "tools": ["terminal", "nmap_scan", "save_note", "read_notes"],
    },
    "vuln": {
        "name": "VulnWorker",
        "role": "Vulnerability Analyst",
        "prompt": """You are a vulnerability analyst. Your job:
- Analyze scan results from previous workers
- Identify potential vulnerabilities based on service versions
- Run vulnerability-specific nmap scripts
- Check for common misconfigurations
- Classify findings by severity (critical, high, medium, low)
- Save ALL findings using save_note with category 'vulnerability'

Read existing notes first to see what recon/scan found.
Target: {target}""",
        "tools": ["terminal", "nmap_scan", "save_note", "read_notes"],
    },
    "exploit": {
        "name": "ExploitWorker",
        "role": "Exploitation Specialist",
        "prompt": """You are an exploitation specialist. Your job:
- Review vulnerabilities found by VulnWorker
- Attempt safe exploitation where authorized
- Verify vulnerabilities are exploitable
- Document proof-of-concept steps
- Save ALL findings using save_note with category 'vulnerability'

IMPORTANT: Only attempt exploitation on authorized targets.
Read existing notes first to see what was found.
Target: {target}""",
        "tools": ["terminal", "nmap_scan", "save_note", "read_notes"],
    },
}

ORCHESTRATOR_PROMPT = """You are the Pentrex Crew Orchestrator. You coordinate a team of specialized security workers.

Available workers:
- recon: Reconnaissance specialist (DNS, OSINT, fingerprinting)
- scan: Network/service scanner (ports, versions, OS detection)
- vuln: Vulnerability analyst (CVE identification, misconfigs)
- exploit: Exploitation specialist (PoC, verification)

Your job:
1. Analyze the task and current findings
2. Decide which worker to deploy next
3. Give specific instructions to the worker
4. Analyze their results and decide next steps
5. Stop when the objective is achieved or all avenues exhausted

Use the delegate_worker tool to assign tasks to workers.
Use read_notes to check what has been found so far.

Task: {task}
Target: {target}

{findings_summary}

Think strategically. Don't repeat work already done. Build on previous findings.
"""


class CrewWorker:
    """A specialized worker agent that executes a focused subtask."""

    def __init__(self, config: Config, role: str):
        self.config = config
        self.llm = LLM(config)
        self.role_key = role
        self.role_info = WORKERS[role]

    def execute(self, task: str, target: str, on_step=None) -> str:
        """Execute a subtask and return results."""
        system = self.role_info["prompt"].format(target=target)
        history = [{"role": "user", "content": task}]
        tools = get_all_tools()
        output_parts = []

        for step in range(15):  # Max 15 steps per worker
            response = self.llm.chat(messages=history, system=system, tools=tools)

            has_tool_use = any(b.type == "tool_use" for b in response.content)

            for b in response.content:
                if b.type == "text" and b.text.strip():
                    output_parts.append(b.text)
                    if on_step:
                        on_step(f"[{self.role_info['name']}] {b.text[:100]}...")

            if not has_tool_use:
                break

            serialized = []
            for b in response.content:
                if b.type == "text":
                    serialized.append({"type": "text", "text": b.text})
                elif b.type == "tool_use":
                    serialized.append({"type": "tool_use", "id": b.id, "name": b.name, "input": b.input})
            history.append({"role": "assistant", "content": serialized})

            tool_results = []
            for b in response.content:
                if b.type == "tool_use":
                    if on_step:
                        on_step(f"[{self.role_info['name']}:tool] {b.name}")
                    result = run_tool(b.name, b.input)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": b.id,
                        "content": json.dumps(result, default=str),
                    })
            history.append({"role": "user", "content": tool_results})

        return "\n\n".join(output_parts) if output_parts else "Worker completed with no text output."


class Crew:
    """
    Multi-agent crew. Orchestrator delegates tasks to specialized workers.
    """

    def __init__(self, config: Config):
        self.config = config
        self.llm = LLM(config)
        self.target = config.target
        self._stopped = False
        self.worker_results = {}

    def stop(self):
        self._stopped = True

    def run(self, task: str, on_step=None) -> str:
        """Run crew on a task. Orchestrator decides worker order."""
        self._stopped = False
        self.worker_results = {}

        # Build delegate tool for orchestrator
        delegate_tool = {
            "name": "delegate_worker",
            "description": "Delegate a subtask to a specialized worker. Workers: recon, scan, vuln, exploit. Give specific instructions.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "worker": {
                        "type": "string",
                        "description": "Worker to delegate to: recon, scan, vuln, exploit"
                    },
                    "instructions": {
                        "type": "string",
                        "description": "Specific instructions for the worker"
                    },
                },
                "required": ["worker", "instructions"],
            },
        }

        notes_tool = None
        for t in get_all_tools():
            if t["name"] == "read_notes":
                notes_tool = t
                break

        tools = [delegate_tool]
        if notes_tool:
            tools.append(notes_tool)

        # Build findings summary
        notes = _load_notes()
        findings_summary = ""
        if notes:
            findings_text = "\n".join([f"- [{n['category']}] {n['content'][:100]}" for n in notes[-15:]])
            findings_summary = f"Current findings:\n{findings_text}"

        system = ORCHESTRATOR_PROMPT.format(
            task=task, target=self.target, findings_summary=findings_summary,
        )

        history = [{"role": "user", "content": f"Execute this crew task: {task}"}]
        final_output = []

        for step in range(self.config.max_agent_iterations):
            if self._stopped:
                final_output.append("[Crew stopped by user]")
                break

            response = self.llm.chat(messages=history, system=system, tools=tools)

            has_tool_use = any(b.type == "tool_use" for b in response.content)

            for b in response.content:
                if b.type == "text" and b.text.strip():
                    final_output.append(b.text)
                    if on_step:
                        on_step(f"[Orchestrator] {b.text[:120]}...")

            if not has_tool_use:
                break

            # Serialize response
            serialized = []
            for b in response.content:
                if b.type == "text":
                    serialized.append({"type": "text", "text": b.text})
                elif b.type == "tool_use":
                    serialized.append({"type": "tool_use", "id": b.id, "name": b.name, "input": b.input})
            history.append({"role": "assistant", "content": serialized})

            # Process tool calls
            tool_results = []
            for b in response.content:
                if b.type == "tool_use":
                    if b.name == "delegate_worker":
                        worker_key = b.input.get("worker", "")
                        instructions = b.input.get("instructions", "")

                        if worker_key not in WORKERS:
                            result = {"error": f"Unknown worker: {worker_key}. Use: recon, scan, vuln, exploit"}
                        else:
                            if on_step:
                                on_step(f"[Crew] Delegating to {WORKERS[worker_key]['name']}...")

                            worker = CrewWorker(self.config, worker_key)
                            worker_output = worker.execute(instructions, self.target, on_step=on_step)
                            self.worker_results[worker_key] = worker_output

                            result = {
                                "worker": worker_key,
                                "status": "completed",
                                "output": worker_output[:3000],  # Truncate for context
                            }

                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": b.id,
                            "content": json.dumps(result, default=str),
                        })

                    elif b.name == "read_notes":
                        result = run_tool("read_notes", b.input)
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": b.id,
                            "content": json.dumps(result, default=str),
                        })

            history.append({"role": "user", "content": tool_results})

        return "\n\n".join(final_output) if final_output else "Crew task completed."
