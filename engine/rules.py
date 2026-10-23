"""Security rule definitions.

Each rule describes a known smart-contract vulnerability class, how it is
detected, and the published research it traces back to. Severity levels
follow a simple scheme: ``high`` / ``medium`` / ``low``.
"""

import re

# Reusable regex fragments.
_EXTERNAL_CALL = re.compile(r"\.call\s*\{", re.M)
_CALL_VALUE = re.compile(r"\.call\s*\{[^}]*\bvalue\s*:", re.M)
_UNCHECKED_CALL = re.compile(r"\.call\s*\([^)]*\)", re.M)
_TX_ORIGIN = re.compile(r"tx\.origin", re.M)
_SELFDESTRUCT = re.compile(r"\bselfdestruct\s*\(|\bsuicide\s*\(", re.M)
_DELEGATECALL = re.compile(r"\.delegatecall\s*\(", re.M)
_BLOCK_TIMESTAMP = re.compile(r"\bblock\.timestamp\b", re.M)
_UNCHECKED = re.compile(r"\bunchecked\s*\{", re.M)
_SENSITIVE_FN = re.compile(
    r"\bfunction\s+(withdraw|withdrawAll|mint|transfer|burn|claim)\b",
    re.M,
)
_ACCESS_GUARD = re.compile(
    r"\brequire\s*\(|\bif\s*\(|onlyOwner|\bowner\b|msg\.sender\s*==\s*owner",
    re.M,
)

RULES = [
    {
        "id": "LAT-001",
        "name": "Reentrancy — state change after external call",
        "severity": "high",
        "cwe": "CWE-841",
        "ref": "Luu et al., Making Smart Contracts Smarter (CCS 2016)",
        "desc": (
            "A value-bearing external call is made and critical state is "
            "updated only afterwards, allowing re-entrant execution."
        ),
        "pattern": _CALL_VALUE,
    },
    {
        "id": "LAT-002",
        "name": "Unchecked low-level call return value",
        "severity": "medium",
        "cwe": "CWE-252",
        "ref": "Feist et al., Slither (WETSEB 2019) — unchecked-call",
        "desc": (
            "A low-level .call() return value is not checked, so a silent "
            "failure can leave the contract in an inconsistent state."
        ),
        "pattern": _UNCHECKED_CALL,
    },
    {
        "id": "LAT-003",
        "name": "Authentication via tx.origin",
        "severity": "high",
        "cwe": "CWE-290",
        "ref": "ConsenSys Smart Contract Best Practices",
        "desc": (
            "Using tx.origin for authorization is vulnerable to phishing "
            "attacks; prefer msg.sender."
        ),
        "pattern": _TX_ORIGIN,
    },
    {
        "id": "LAT-004",
        "name": "Selfdestruct present",
        "severity": "medium",
        "cwe": "CWE-667",
        "ref": "OpenZeppelin security guidance",
        "desc": (
            "selfdestruct can unexpectedly remove the contract; it should be "
            "guarded and its use justified."
        ),
        "pattern": _SELFDESTRUCT,
    },
    {
        "id": "LAT-005",
        "name": "Delegatecall present",
        "severity": "medium",
        "cwe": "CWE-829",
        "ref": "Kalra et al., ZEUS (NDSS 2018)",
        "desc": (
            "delegatecall runs external code in the caller's storage context "
            "and must be tightly controlled."
        ),
        "pattern": _DELEGATECALL,
    },
    {
        "id": "LAT-006",
        "name": "Sensitive function without access control",
        "severity": "high",
        "cwe": "CWE-284",
        "ref": "OpenZeppelin access-control patterns",
        "desc": (
            "A privileged function (withdraw/mint/transfer/burn/claim) shows "
            "no ownership or authorization check."
        ),
        "pattern": _SENSITIVE_FN,
        "function_level": True,
        "guard": _ACCESS_GUARD,
    },
    {
        "id": "LAT-007",
        "name": "Use of block.timestamp",
        "severity": "low",
        "cwe": "CWE-682",
        "ref": "SWC-116",
        "desc": (
            "block.timestamp can be manipulated by miners and is unsafe for "
            "randomness or tight time windows."
        ),
        "pattern": _BLOCK_TIMESTAMP,
    },
    {
        "id": "LAT-008",
        "name": "Explicit unchecked arithmetic block",
        "severity": "low",
        "cwe": "CWE-682",
        "ref": "SWC-101",
        "desc": (
            "An explicit `unchecked` block disables overflow checks; verify "
            "the arithmetic is provably safe."
        ),
        "pattern": _UNCHECKED,
    },
]


def severity_rank(sev):
    return {"high": 3, "medium": 2, "low": 1}.get(sev, 0)
