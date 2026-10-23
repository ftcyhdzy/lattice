"""Human-readable report rendering."""

from .rules import severity_rank


def render(findings, path="<source>"):
    lines = ["Lattice Audit Engine v0.1", f"File: {path}"]

    if not findings:
        lines.append("No findings - the source passes all reference rules.")
        return "\n".join(lines)

    findings = sorted(
        findings, key=lambda f: (-severity_rank(f["severity"]), f["line"])
    )
    high = sum(1 for f in findings if f["severity"] == "high")
    med = sum(1 for f in findings if f["severity"] == "medium")
    low = sum(1 for f in findings if f["severity"] == "low")
    score = sum(severity_rank(f["severity"]) for f in findings)

    lines.append(
        f"Findings: {len(findings)} "
        f"({high} high, {med} medium, {low} low) | risk score {score}"
    )
    lines.append("")

    for f in findings:
        lines.append(f"[{f['rule']}] {f['severity'].upper()} - {f['name']}")
        lines.append(f"  line {f['line']}: {f['snippet']}")
        lines.append(f"  {f['note']}  ({f['cwe']})")
        lines.append("")

    return "\n".join(lines)
