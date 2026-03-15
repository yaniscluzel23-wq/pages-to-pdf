#!/usr/bin/env python3
"""Convert a single .pages file to PDF using Apple Pages via AppleScript."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


APPLESCRIPT = r'''
on run argv
    set inputPath to item 1 of argv
    set outputPath to item 2 of argv

    tell application "Pages"
        activate
        set docRef to open POSIX file inputPath
        export docRef to POSIX file outputPath as PDF
        close docRef saving no
    end tell
end run
'''


def convert_pages_to_pdf(input_path: Path) -> Path:
    output_path = input_path.with_suffix(".pdf")

    subprocess.run(
        ["osascript", "-e", APPLESCRIPT, str(input_path), str(output_path)],
        check=True,
        capture_output=True,
        text=True,
    )

    return output_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert a single .pages document to PDF using Apple Pages."
    )
    parser.add_argument("pages_file", help="Path to the .pages file to convert")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    input_path = Path(args.pages_file).expanduser().resolve()

    if not input_path.exists():
        print(f"Erreur : fichier introuvable -> {input_path}")
        return 1

    if input_path.suffix.lower() != ".pages":
        print("Erreur : le fichier doit avoir l'extension .pages")
        return 1

    try:
        output_path = convert_pages_to_pdf(input_path)
    except subprocess.CalledProcessError as exc:
        error_message = (exc.stderr or exc.stdout or str(exc)).strip()
        print(f"Erreur lors de la conversion : {error_message}")
        return 1
    except Exception as exc:
        print(f"Erreur inattendue : {exc}")
        return 1

    print(f"Conversion terminée : {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
