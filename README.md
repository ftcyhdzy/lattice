# Lattice

**The audit layer for on-chain code.**

Lattice is a decentralized AI-audit network for smart contracts on Robinhood Chain. This repository contains the open-source **reference implementation of the audit engine** — a dependency-free static analyzer for Solidity — together with the protocol whitepaper and project site.

> **Status: pre-launch.** No token has been issued.

## What's here

- `engine/` — the reference audit engine (pure Python, no dependencies)
- `examples/` — a vulnerable contract and its hardened counterpart, used by the tests
- `tests/` — unit tests
- `whitepaper.md` — the protocol whitepaper
- `website/` — the project site (`website/index.html`, hash-routed)

## The audit pipeline

Lattice layers three kinds of verification (whitepaper §3):

1. **AI audit agents** — continuous static, symbolic, and learning-based analysis over every deployed contract.
2. **White-hat bounty layer** — permissionless, on-chain settlement for findings that automation misses.
3. **Post-quantum attestations** — lattice-based signatures (NIST FIPS 203/204) on every audit result.

This repository ships the *static-analysis* slice of layer 1 as a runnable reference. The production network runs a superset of these checks across compiled bytecode.

## Quick start

Requires Python 3.10+. No third-party dependencies.

```bash
# audit a contract
python -m engine examples/vulnerable.sol

# run the test suite
python -m unittest discover -s tests
```

## Detectors

| ID | Name | Severity | CWE |
|----|------|----------|-----|
| LAT-001 | Reentrancy — state change after external call | high | CWE-841 |
| LAT-002 | Unchecked low-level call return value | medium | CWE-252 |
| LAT-003 | Authentication via `tx.origin` | high | CWE-290 |
| LAT-004 | Selfdestruct present | medium | CWE-667 |
| LAT-005 | Delegatecall present | medium | CWE-829 |
| LAT-006 | Sensitive function without access control | high | CWE-284 |
| LAT-007 | Use of `block.timestamp` | low | CWE-682 |
| LAT-008 | Explicit `unchecked` arithmetic block | low | CWE-682 |

Every detector traces to published research — the citation is attached to each rule in `engine/rules.py`.

## Scope

This is a **reference implementation**. It scans Solidity source for signal patterns and is not a substitute for a full formal or bytecode-level audit. The production network runs richer analysis (in the Slither / Securify / ZEUS lineage, plus learning-based models) and staked human review — see the whitepaper for the complete design.

## Whitepaper

Read [`whitepaper.md`](whitepaper.md) for the protocol specification, token economics, roadmap, and risk statement.

## License

MIT — see [`LICENSE`](LICENSE).

## Disclaimer

Lattice is pre-launch. No token has been issued, and nothing in this repository is an offer, a sale, or financial advice.
