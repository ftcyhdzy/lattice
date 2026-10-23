"""Command-line entry point."""

import argparse

from .analyzer import scan
from .report import render


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="lattice-audit",
        description="Reference audit engine for Solidity source.",
    )
    parser.add_argument(
        "files",
        nargs="+",
        help="one or more .sol files to analyze",
    )
    args = parser.parse_args(argv)

    for path in args.files:
        with open(path, encoding="utf-8") as fh:
            source = fh.read()
        print(render(scan(source), path))
        print()

    return 0
