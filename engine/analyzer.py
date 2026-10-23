"""Function-level static analysis over Solidity source.

The analyzer splits a source file into functions, then runs each security
rule against every function body. Line numbers are reported against the
original source.
"""

import re

from .rules import RULES

_FUNC = re.compile(r"\bfunction\s+(\w+)\s*\([^)]*\)")
_SENSITIVE_NAMES = {"withdraw", "withdrawAll", "mint", "transfer", "burn", "claim"}


def _extract_functions(source):
    """Return a list of {name, body, start_line} for every function."""
    funcs = []
    for m in _FUNC.finditer(source):
        name = m.group(1)
        brace = source.find("{", m.end())
        if brace == -1:
            continue
        depth = 0
        end = None
        for j in range(brace, len(source)):
            if source[j] == "{":
                depth += 1
            elif source[j] == "}":
                depth -= 1
                if depth == 0:
                    end = j
                    break
        if end is None:
            continue
        body = source[brace + 1 : end]
        start_line = source[:brace].count("\n") + 1
        funcs.append({"name": name, "body": body, "start_line": start_line})
    return funcs


def scan(source):
    """Run all rules against the source and return a list of findings."""
    lines = source.split("\n")
    funcs = _extract_functions(source)
    findings = []

    for rule in RULES:
        # Function-level rules evaluate a whole function body.
        if rule.get("function_level"):
            guard = rule["guard"]
            for f in funcs:
                if f["name"] in _SENSITIVE_NAMES and not guard.search(f["body"]):
                    findings.append(
                        {
                            "rule": rule["id"],
                            "name": rule["name"],
                            "severity": rule["severity"],
                            "cwe": rule["cwe"],
                            "ref": rule["ref"],
                            "line": f["start_line"],
                            "snippet": f["name"],
                            "note": rule["desc"],
                        }
                    )
            continue

        # Pattern rules match lines inside each function body.
        pat = rule["pattern"]
        for f in funcs:
            for m in pat.finditer(f["body"]):
                line = f["start_line"] + f["body"][: m.start()].count("\n")
                snippet = lines[line - 1].strip() if 0 < line <= len(lines) else ""
                findings.append(
                    {
                        "rule": rule["id"],
                        "name": rule["name"],
                        "severity": rule["severity"],
                        "cwe": rule["cwe"],
                        "ref": rule["ref"],
                        "line": line,
                        "snippet": snippet,
                        "note": rule["desc"],
                    }
                )

    return findings
