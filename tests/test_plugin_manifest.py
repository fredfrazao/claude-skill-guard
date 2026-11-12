import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent


def load(rel: str) -> dict:
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def test_marketplace_lists_this_plugin() -> None:
    plugin = load(".claude-plugin/plugin.json")
    entry = load(".claude-plugin/marketplace.json")["plugins"][0]
    assert entry["name"] == plugin["name"]
    assert entry["source"] == "./"


def test_plugin_hooks_cover_both_events() -> None:
    hooks = load("hooks/hooks.json")["hooks"]
    assert hooks["PostToolUse"][0]["matcher"] == "Skill"
    for event in ("PostToolUse", "UserPromptExpansion"):
        hook = hooks[event][0]["hooks"][0]
        assert hook["command"] == "python3"
        assert hook["args"] == ["${CLAUDE_PLUGIN_ROOT}/check_skill_concealment.py"]
    assert (ROOT / "check_skill_concealment.py").is_file()
