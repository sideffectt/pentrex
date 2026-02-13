"""Report generator — creates pentest reports from saved notes."""

import os
from datetime import datetime, timezone
from pentrex.tools.notes import _load_notes


def generate_report(target: str = "") -> str:
    """Generate a markdown report from saved notes."""
    notes = _load_notes()
    if not notes:
        return "No findings to report. Use save_note to record findings first."

    if target:
        notes = [n for n in notes if target in n.get("target", "") or not n.get("target")]

    # Group by category
    grouped = {}
    for note in notes:
        cat = note.get("category", "other")
        grouped.setdefault(cat, []).append(note)

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    lines = [
        f"# Penetration Test Report",
        f"",
        f"**Target:** {target or 'Multiple targets'}",
        f"**Date:** {timestamp}",
        f"**Tool:** Pentrex v2.0",
        f"",
        f"---",
        f"",
        f"## Executive Summary",
        f"",
        f"Total findings: {len(notes)}",
        f"",
    ]

    # Category summary
    for cat, items in grouped.items():
        lines.append(f"- **{cat.title()}**: {len(items)} finding(s)")

    lines.extend(["", "---", ""])

    # Category order
    order = ["vulnerability", "credential", "recon", "finding", "artifact"]
    for cat in order:
        if cat not in grouped:
            continue
        lines.append(f"## {cat.title()}")
        lines.append("")
        for note in grouped[cat]:
            ts = note.get("timestamp", "")[:16]
            tgt = note.get("target", "")
            lines.append(f"### [{ts}] {tgt}")
            lines.append(f"")
            lines.append(note["content"])
            lines.append("")

    # Remaining categories
    for cat, items in grouped.items():
        if cat in order:
            continue
        lines.append(f"## {cat.title()}")
        lines.append("")
        for note in items:
            lines.append(f"- {note['content']}")
        lines.append("")

    return "\n".join(lines)


def save_report(target: str = "", output_dir: str = "loot") -> str:
    """Save report to file."""
    report = generate_report(target)
    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M")
    filename = f"report_{timestamp}.md"
    path = os.path.join(output_dir, filename)

    with open(path, "w") as f:
        f.write(report)

    return path
