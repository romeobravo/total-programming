"""Hermes plugin for Total Programming.

The skill is the single source of truth. This adapter injects the complete
principles as context before every LLM turn (like the Claude Code session
hook and the Pi extension do), registers the skill as
``total-programming:total-programming``, and adds ``/total-programming``
to turn injection on or off. Runtime state is process-local.
"""

from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Any

DEFAULT_ENABLED = True

ROOT = Path(__file__).resolve().parent
SKILL_PATH = ROOT / "skills" / "total-programming" / "SKILL.md"

_enabled: bool | None = None


def _strip_frontmatter(text: str) -> str:
    return re.sub(r"^---\r?\n[\s\S]*?\r?\n---\r?\n", "", text or "", count=1).strip()


def read_principles() -> str:
    """Return the complete principles with the skill's YAML metadata stripped."""
    return _strip_frontmatter(SKILL_PATH.read_text(encoding="utf-8"))


def _env_enabled() -> bool | None:
    raw = os.environ.get("TOTAL_PROGRAMMING_ENABLED", "").strip().lower()
    if raw in {"1", "true", "yes", "on"}:
        return True
    if raw in {"0", "false", "no", "off"}:
        return False
    return None


def _is_enabled() -> bool:
    if _enabled is not None:
        return _enabled
    env = _env_enabled()
    return DEFAULT_ENABLED if env is None else env


def _pre_llm_call(session_id: str = "", **_: Any) -> dict[str, str] | None:
    if not _is_enabled():
        return None
    try:
        return {"context": read_principles()}
    except OSError:
        return None


def _handle_command(raw_args: str) -> str:
    global _enabled
    arg = (raw_args or "").strip().lower()
    if arg in {"on", "off"}:
        _enabled = arg == "on"
        return f"Total Programming principles injection turned {arg}."
    if arg in {"", "status"}:
        state = "on" if _is_enabled() else "off"
        return f"Total Programming principles injection: {state}. Use `/total-programming on|off`."
    return "Usage: /total-programming [on|off]"


def register(ctx: Any) -> None:
    """Register the hook, skill, and slash command with Hermes."""
    if SKILL_PATH.exists():
        ctx.register_skill("total-programming", SKILL_PATH)
    ctx.register_hook("pre_llm_call", _pre_llm_call)
    ctx.register_command(
        "total-programming",
        _handle_command,
        description="Toggle Total Programming principles injection: on or off.",
        args_hint="[on|off]",
    )
