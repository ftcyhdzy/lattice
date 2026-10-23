# Contributing to Lattice

Thanks for your interest in contributing. Lattice is a decentralized audit
network — the more rigorous the analysis, the safer the chain.

## Scope of this repository

This repository is the **reference implementation**. Contributions that
improve the correctness, coverage, or clarity of the audit engine are welcome.

## Ground rules

- Every new detector must cite its source (a paper, CWE, or established
  best-practice document), consistent with `engine/rules.py`.
- Add a regression case under `examples/` and a test in `tests/`.
- Keep the engine dependency-free (standard library only).
- Do not introduce token sales, deployment scripts, or anything that could be
  misread as financial activity — this project is pre-launch.

## Process

1. Open an issue describing the change first.
2. Fork, branch, and implement.
3. Run `python -m unittest discover -s tests` before opening a PR.
4. Keep commits small and messages descriptive.

## Code style

- Python: follow PEP 8; keep lines short and docstrings meaningful.
- Solidity examples: `pragma solidity ^0.8.0`, SPDX header, English comments.
