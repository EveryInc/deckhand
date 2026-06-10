#!/usr/bin/env python3
"""Blind two eval arms' renders for judging.

setup: randomly assigns the two arms to deck-A / deck-B, copies each arm's slide
images under neutral names (01.jpg, 02.jpg, ...), and records the assignment in a
dotfile the judges are never shown. Originals (for edit evals) follow the same
assignment into orig-A / orig-B.

    python blind.py setup JUDGING_DIR --arm deckhand=/run/deckhand/img --arm pptx-skill=/run/pptx/img
    python blind.py setup JUDGING_DIR --arm deckhand=... --arm pptx-skill=... \
        --orig deckhand=/run/deckhand/orig-img --orig pptx-skill=/run/pptx/orig-img
    python blind.py reveal JUDGING_DIR        # after ALL verdicts are in

The orchestrator must not echo the assignment anywhere a judge could read it.
"""

import argparse
import random
import re
import shutil
import sys
from pathlib import Path

IMG_EXTS = (".jpg", ".jpeg", ".png")


def natural_key(p: Path):
    return [int(t) if t.isdigit() else t for t in re.split(r"(\d+)", p.name.lower())]


def collect_images(d: str) -> list:
    path = Path(d)
    if not path.is_dir():
        sys.exit(f"blind.py: not a directory: {d}")
    imgs = sorted((p for p in path.iterdir() if p.suffix.lower() in IMG_EXTS), key=natural_key)
    if not imgs:
        sys.exit(f"blind.py: no images in {d}")
    return imgs


def place(imgs: list, dest: Path) -> None:
    dest.mkdir(parents=True, exist_ok=True)
    for i, src in enumerate(imgs, 1):
        shutil.copy2(src, dest / f"{i:02d}{src.suffix.lower()}")


def parse_pairs(pairs: list, flag: str) -> dict:
    out = {}
    for spec in pairs:
        name, sep, d = spec.partition("=")
        if not sep or not name or not d:
            sys.exit(f"blind.py: {flag} expects name=dir, got: {spec}")
        out[name] = d
    return out


def cmd_setup(args):
    arms = parse_pairs(args.arm, "--arm")
    if len(arms) != 2:
        sys.exit(f"blind.py: exactly two --arm required, got {len(arms)}")
    origs = parse_pairs(args.orig or [], "--orig")
    if origs and set(origs) != set(arms):
        sys.exit("blind.py: --orig names must match the --arm names")

    out = Path(args.judging_dir)
    if (out / ".assignment").exists():
        sys.exit(f"blind.py: {out} already has an assignment — use a fresh directory per round")

    names = sorted(arms)
    random.shuffle(names)
    assignment = dict(zip("AB", names))

    for letter, name in assignment.items():
        imgs = collect_images(arms[name])
        place(imgs, out / f"deck-{letter}")
        print(f"deck-{letter}: {len(imgs)} slides")
        if origs:
            oimgs = collect_images(origs[name])
            place(oimgs, out / f"orig-{letter}")
            print(f"orig-{letter}: {len(oimgs)} slides")

    (out / ".assignment").write_text(
        " ".join(f"{l}={assignment[l]}" for l in "AB") + "\n"
    )
    print(f"blinded into {out} — do NOT read {out}/.assignment until all verdicts are in")


def cmd_reveal(args):
    f = Path(args.judging_dir) / ".assignment"
    if not f.exists():
        sys.exit(f"blind.py: no assignment in {args.judging_dir}")
    print(f.read_text().strip())


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("setup", help="anonymize two arms into deck-A/deck-B")
    s.add_argument("judging_dir")
    s.add_argument("--arm", action="append", required=True, metavar="NAME=RENDER_DIR")
    s.add_argument("--orig", action="append", metavar="NAME=RENDER_DIR",
                   help="pre-edit renders for edit evals; same names as --arm")
    s.set_defaults(fn=cmd_setup)
    r = sub.add_parser("reveal", help="print the assignment (only after all verdicts)")
    r.add_argument("judging_dir")
    r.set_defaults(fn=cmd_reveal)
    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
