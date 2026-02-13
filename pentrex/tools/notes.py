"""Notes system - save findings across sessions."""

import json
import os
from datetime import datetime, timezone
from pentrex.tools.registry import register

NOTES_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "loot", "notes.json")


def _load_notes() -> list:
    path = os.path.abspath(NOTES_PATH)
    if not os.path.exists(path):
        return []
    with open(path, "r") as f:
        return json.load(f)


def _save_notes(notes: list):
    path = os.path.abspath(NOTES_PATH)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(notes, f, indent=2)


@register(
    name="save_note",
    description="Save a finding or note. Categories: credential, vulnerability, finding, artifact, recon.",
    parameters={
        "content": {
            "type": "string",
            "description": "The finding or note content"
        },
        "category": {
            "type": "string",
            "description": "Category: credential, vulnerability, finding, artifact, recon"
        },
        "target": {
            "type": "string",
            "description": "Related target host/IP"
        },
    },
    required=["content", "category"],
)
def save_note(content: str, category: str, target: str = "") -> dict:
    notes = _load_notes()
    note = {
        "id": len(notes) + 1,
        "content": content,
        "category": category,
        "target": target,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    notes.append(note)
    _save_notes(notes)
    return {"saved": True, "id": note["id"], "category": category}


@register(
    name="read_notes",
    description="Read saved findings. Optionally filter by category or target.",
    parameters={
        "category": {
            "type": "string",
            "description": "Filter by category (optional)"
        },
        "target": {
            "type": "string",
            "description": "Filter by target (optional)"
        },
    },
    required=[],
)
def read_notes(category: str = "", target: str = "") -> dict:
    notes = _load_notes()

    if category:
        notes = [n for n in notes if n.get("category") == category]
    if target:
        notes = [n for n in notes if target in n.get("target", "")]

    return {"count": len(notes), "notes": notes[-20:]}  # Last 20
