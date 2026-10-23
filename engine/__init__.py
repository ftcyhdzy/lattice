"""Lattice audit engine — a reference implementation of the on-chain
verification pipeline described in the whitepaper.

This package ships a small, dependency-free static analyzer for Solidity
source code. It is intentionally a *reference implementation*: the production
network runs a superset of these checks across compiled bytecode, with
learning-based models and staked human review on top.
"""

from .analyzer import scan
from .report import render

__all__ = ["scan", "render"]
__version__ = "0.1.0"
