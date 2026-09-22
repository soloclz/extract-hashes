"""Command-line interface for extract-hashes."""

from __future__ import annotations

import argparse
import sys
from collections import Counter
from pathlib import Path

from . import __version__
from .extractor import HEX_LENGTHS, extract


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(
        description="Extract and deduplicate common hexadecimal hash candidates."
    )
    result.add_argument("input", help="text/HTML/Markdown input file, or - for stdin")
    result.add_argument("-o", "--output", help="write one hash per line to this file")
    result.add_argument(
        "--version", action="version", version=f"extract-hashes {__version__}"
    )
    return result


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        if args.input == "-":
            text = sys.stdin.read()
        else:
            text = Path(args.input).read_text(encoding="utf-8", errors="replace")
    except OSError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1

    candidates = extract(text)
    rendered = "".join(f"{value}\n" for value in candidates)
    if args.output:
        try:
            Path(args.output).write_text(rendered, encoding="utf-8")
        except OSError as error:
            print(f"error: {error}", file=sys.stderr)
            return 1
    else:
        sys.stdout.write(rendered)

    counts = Counter(map(len, candidates))
    destination = args.output or "stdout"
    print(f"extracted {len(candidates)} unique candidates to {destination}", file=sys.stderr)
    for length in sorted(counts):
        print(
            f"{length}-hex: {counts[length]}; candidates: {HEX_LENGTHS[length]}",
            file=sys.stderr,
        )
    if candidates:
        print(
            "structure identifies candidates only; confirm the algorithm from application "
            "context or a controlled verification",
            file=sys.stderr,
        )
    return 0
