"""Basic tests for Pentrex tools."""

import pytest
from pentrex.tools.registry import get_all_tools, get_tool_names, run_tool
from pentrex.tools.quiz import quiz
from pentrex.tools.explain import explain
from pentrex.tools.notes import save_note, read_notes, _load_notes, _save_notes, NOTES_PATH
from pentrex.playbooks import list_playbooks, get_playbook, build_playbook_task
from pentrex.config import Config


def test_tools_registered():
    names = get_tool_names()
    assert "terminal" in names
    assert "nmap_scan" in names
    assert "save_note" in names
    assert "quiz" in names
    assert "explain" in names


def test_tool_schemas():
    tools = get_all_tools()
    assert len(tools) >= 5
    for tool in tools:
        assert "name" in tool
        assert "description" in tool
        assert "input_schema" in tool


def test_quiz_random():
    result = quiz()
    assert "questions" in result
    assert len(result["questions"]) >= 1


def test_quiz_domain():
    result = quiz(domain="web_attacks", count=2)
    assert len(result["questions"]) == 2


def test_explain_known():
    result = explain("sql_injection")
    assert "title" in result
    assert result["title"] == "SQL Injection"


def test_explain_fuzzy():
    result = explain("xss")
    assert "title" in result


def test_explain_unknown():
    result = explain("nonexistent_topic_xyz")
    assert "available_topics" in result


def test_playbooks_list():
    pbs = list_playbooks()
    assert len(pbs) >= 3


def test_playbook_build():
    task = build_playbook_task("web_recon", "example.com")
    assert "example.com" in task
    assert "Execute" in task


def test_config_defaults():
    config = Config()
    assert config.max_agent_iterations == 25
    assert "haiku" in config.model


def test_unknown_tool():
    result = run_tool("nonexistent_tool", {})
    assert "error" in result
