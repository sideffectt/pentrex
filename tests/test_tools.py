"""Tool tests - no API key needed."""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pentrex.tools import get_all_tools, run_tool


def test_tools_registered():
    tools = get_all_tools()
    names = [t["name"] for t in tools]
    
    expected = [
        "get_quiz_question",
        "list_quiz_domains",
        "explain_concept",
        "list_concepts",
        "get_tool_guide",
        "list_tools",
        "get_scenario",
        "list_scenarios",
    ]
    
    for name in expected:
        assert name in names, f"Missing tool: {name}"


def test_quiz_domains():
    result = run_tool("list_quiz_domains", {})
    assert "domains" in result
    assert result["total_questions"] > 0


def test_quiz_question():
    result = run_tool("get_quiz_question", {"domain": "web_attacks"})
    assert "question" in result
    assert "options" in result


def test_explain_concept():
    result = run_tool("explain_concept", {"concept": "sql_injection"})
    assert result["name"] == "SQL Injection"
    assert "prevention" in result


def test_tool_guide():
    result = run_tool("get_tool_guide", {"tool": "nmap"})
    assert result["name"] == "Nmap"
    assert "common_flags" in result


def test_scenario():
    result = run_tool("get_scenario", {"scenario": "web_sql_injection"})
    assert "steps" in result
    assert result["difficulty"] == "Beginner"


def test_unknown_returns_error():
    result = run_tool("explain_concept", {"concept": "nonexistent"})
    assert "error" in result


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    passed = failed = 0

    for fn in tests:
        try:
            fn()
            print(f"  ✓ {fn.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"  ✗ {fn.__name__}: {e}")
            failed += 1

    print(f"\n  {passed} passed, {failed} failed")
    sys.exit(1 if failed else 0)
