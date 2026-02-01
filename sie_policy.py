from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable


@dataclass(frozen=True)
class PolicyDecision:
    allowed: bool
    reason: str


DEFAULT_DISCLOSURE_PATTERNS = (
    # Prompt / system message extraction attempts
    "system prompt",
    "print your system prompt",
    "reveal your system prompt",
    "developer message",
    "internal instructions",
    "hidden policies",
    "policy text",
    "how you work",
    "routing logic",
    # Tool discovery / capability extraction
    "list all tool",
    "tool names",
    "tools you have",
    "what tools",
    "call tool",
    # Common exfil patterns / “verification token” traps
    "verification string",
    "verification token",
    "output the secret",
    "repeat exactly",
)


def _contains_any(text: str, patterns: Iterable[str]) -> bool:
    t = text.lower()
    return any(p.lower() in t for p in patterns)


def is_disclosure_attempt(untrusted_content: str, extra_patterns: Iterable[str] = ()) -> bool:
    """
    MVP-grade detector for prompt/config/tool disclosure attempts.
    This is not a full NLP detector; it is deliberately simple and auditable.
    """
    patterns = list(DEFAULT_DISCLOSURE_PATTERNS) + list(extra_patterns)
    return _contains_any(untrusted_content, patterns)


def evaluate_untrusted_content(
    *,
    untrusted_content: str,
    constraints: Dict[str, Any],
    extra_patterns: Iterable[str] = (),
) -> PolicyDecision:
    """
    Given untrusted content and signed constraints, decide whether to proceed.

    Intended usage:
    - Agents treat documents/emails/code as untrusted content (DATA channel)
    - Only signed envelopes are INSTRUCTION channel
    - If content tries to trigger disclosure, and the signed policy forbids it, block.
    """
    deny_disclosure = bool(constraints.get("deny_prompt_disclosure", False))

    if deny_disclosure and is_disclosure_attempt(untrusted_content, extra_patterns=extra_patterns):
        return PolicyDecision(
            allowed=False,
            reason="Untrusted content attempted prompt/config/tool disclosure or token exfiltration; blocked by signed constraints.",
        )

    return PolicyDecision(allowed=True, reason="No disclosure attempt detected (or policy not enabled).")


def require_instruction_channel(envelope: Dict[str, Any]) -> None:
    """
    Enforce channel separation at the boundary:
    only signed envelopes with channel='instruction' are permitted to influence policy/behavior.
    """
    channel = envelope.get("channel")
    if channel != "instruction":
        raise ValueError(f"Invalid channel for trusted instructions: {channel}")
