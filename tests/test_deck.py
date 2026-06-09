"""End-to-end tests for deck.py — drive the CLI exactly as an agent would.

No binary fixtures: every test builds its deck with python-pptx, then talks to
deck.py only through its command line and JSON patches.
"""
import json
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

import pytest
from PIL import Image
from pptx import Presentation
from pptx.util import Inches, Pt

SCRIPTS = Path(__file__).resolve().parents[1] / "skills" / "deckhand" / "scripts"
DECK = SCRIPTS / "deck.py"


def run(*args):
    return subprocess.run(
        [sys.executable, str(DECK), *map(str, args)], capture_output=True, text=True
    )


def inspect(path, *args):
    r = run(path, "inspect", *args)
    assert r.returncode == 0, r.stderr
    return json.loads(r.stdout)


def apply_patch(deck_path, ops, out, *extra):
    patch = deck_path.parent / "patch.json"
    patch.write_text(json.dumps({"ops": ops}))
    return run(deck_path, "apply", patch, "-o", out, *extra)


@pytest.fixture
def img(tmp_path):
    p = tmp_path / "pic.png"
    Image.new("RGB", (200, 120), (40, 90, 100)).save(p)
    return p


@pytest.fixture
def deck(tmp_path, img):
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(13.33), Inches(7.5)
    blank = prs.slide_layouts[6]

    s0 = prs.slides.add_slide(blank)
    tb = s0.shapes.add_textbox(Inches(1), Inches(1), Inches(6), Inches(1))
    run0 = tb.text_frame.paragraphs[0].add_run()
    run0.text = "Hello World"
    run0.font.size, run0.font.bold = Pt(30), True
    foot = s0.shapes.add_textbox(Inches(1), Inches(6.5), Inches(4), Inches(0.5))
    foot.text_frame.paragraphs[0].add_run().text = "Globex Corp confidential"

    s1 = prs.slides.add_slide(blank)
    s1.shapes.add_picture(str(img), Inches(1), Inches(1), width=Inches(3))
    t = s1.shapes.add_table(2, 2, Inches(5), Inches(1), Inches(6), Inches(2)).table
    for ri in range(2):
        for ci in range(2):
            t.cell(ri, ci).text = "r%dc%d" % (ri, ci)

    s2 = prs.slides.add_slide(blank)
    tb2 = s2.shapes.add_textbox(Inches(1), Inches(1), Inches(6), Inches(1))
    tb2.text_frame.paragraphs[0].add_run().text = "Globex Corp roadmap"

    p = tmp_path / "deck.pptx"
    prs.save(p)
    return p


def shapes_of(data, idx):
    return {k: v for k, v in data["slides"][str(idx)].items() if not k.startswith("_")}


def find_sid(data, idx, **want):
    for sid, e in shapes_of(data, idx).items():
        if all(str(want[k]) in json.dumps(e.get(k, "")) for k in want):
            return sid
    raise AssertionError("no shape matching %s on slide %d" % (want, idx))


# ---------------------------------------------------------------------------


def test_docs_needs_no_file():
    r = run("docs")
    assert r.returncode == 0
    for section in ("GOLDEN RULES", "CREATE OPS", "TABLE STRUCTURE", "OUT OF SCOPE"):
        assert section in r.stdout


def test_inspect_reports_shapes_and_text(deck):
    data = inspect(deck, "--slide", "0")
    sid = find_sid(data, 0, paragraphs="Hello World")
    entry = shapes_of(data, 0)[sid]
    assert sid.startswith("s")
    assert entry["paragraphs"][0]["font_size"] == 30.0
    assert entry["paragraphs"][0]["bold"] is True


def test_set_text_inherits_formatting(deck, tmp_path):
    data = inspect(deck, "--slide", "0")
    sid = find_sid(data, 0, paragraphs="Hello World")
    out = tmp_path / "out.pptx"
    r = apply_patch(deck, [{"op": "set-text", "slide": 0, "shape": sid, "text": ["Replaced"]}], out)
    assert r.returncode == 0, r.stdout + r.stderr
    para = shapes_of(inspect(out, "--slide", "0"), 0)[sid]["paragraphs"][0]
    assert para["text"] == "Replaced"
    assert para["font_size"] == 30.0 and para["bold"] is True  # inherited


def test_replace_text_deck_wide_and_zero_hit_errors(deck, tmp_path):
    out = tmp_path / "out.pptx"
    r = apply_patch(deck, [{"op": "replace-text", "scope": "deck", "from": "Globex Corp", "to": "Acme"}], out)
    assert r.returncode == 0 and "2 occurrence(s)" in r.stdout
    r = apply_patch(deck, [{"op": "replace-text", "scope": "deck", "from": "Nonexistent", "to": "x"}], tmp_path / "o2.pptx")
    assert r.returncode != 0 and "not found" in r.stdout


def test_rejection_is_atomic_and_reports_all_errors(deck, tmp_path):
    before = deck.read_bytes()
    out = tmp_path / "never.pptx"
    r = apply_patch(deck, [
        {"op": "set-txt", "slide": 0, "shape": "s1", "text": ["x"]},
        {"op": "add-shape", "slide": 0, "kind": "blob", "at": [1, 1], "size": [2, 1]},
        {"op": "set-text", "slide": 0, "shape": "s9999", "text": ["x"]},
        {"op": "add-row", "slide": 99, "shape": "s1", "cells": ["a"]},
    ], out)
    assert r.returncode == 1
    assert "4 validation error(s)" in r.stdout
    assert "unknown op" in r.stdout
    assert "unknown shape kind" in r.stdout
    assert "shapes on slide 0" in r.stdout  # self-correcting: real inventory included
    assert "0-BASED" in r.stdout
    assert not out.exists()
    assert deck.read_bytes() == before


def test_runtime_failure_saves_nothing(deck, tmp_path):
    data = inspect(deck, "--slide", "1")
    table_sid = find_sid(data, 1, type="TABLE")
    out = tmp_path / "never.pptx"
    r = apply_patch(deck, [
        {"op": "set-text", "slide": 2, "shape": find_sid(data := inspect(deck, "--slide", "2"), 2, paragraphs="roadmap"), "text": ["changed"]},
        {"op": "add-row", "slide": 1, "shape": table_sid, "cells": ["only-one"]},
    ], out)
    assert r.returncode == 1 and "Nothing was saved" in r.stdout
    assert not out.exists()


def test_create_ops_and_style_by_name(deck, tmp_path, img):
    out = tmp_path / "out.pptx"
    r = apply_patch(deck, [
        {"op": "add-slide"},
        {"op": "add-shape", "slide": 3, "kind": "rect", "at": [0, 0], "size": [13.33, 7.5],
         "fill": "0F2B2E", "line": "none", "name": "bg"},
        {"op": "add-shape", "slide": 3, "kind": "textbox", "at": [1, 1], "size": [6, 1],
         "text": [{"text": "Built by an agent", "font_size": 32, "bold": True}], "name": "title"},
        {"op": "add-shape", "slide": 3, "kind": "CHEVRON", "at": [8, 1], "size": [2, 0.8], "fill": "4999A0"},
        {"op": "add-shape", "slide": 3, "kind": "line", "from": [1, 2.2], "to": [12, 2.2], "line_color": "C3DCDE"},
        {"op": "add-picture", "slide": 3, "image": str(img), "at": [9, 3], "width": 3},
        {"op": "add-table", "slide": 3, "at": [1, 3], "size": [7, 2], "rows": [["A", "B"], ["1", "2"]]},
        {"op": "set-style", "slide": 3, "shape": "title", "rotation": 6},  # created earlier in THIS patch
    ], out)
    assert r.returncode == 0, r.stdout + r.stderr
    data = inspect(out, "--slide", "3")
    entries = shapes_of(data, 3)
    assert len(entries) == 6  # bg, title, chevron, line, picture, table
    title = entries[find_sid(data, 3, paragraphs="Built by an agent")]
    assert title["rotation"] == 6.0
    pic = entries[find_sid(data, 3, type="PICTURE")]
    assert pic["size"][0] == 3.0 and abs(pic["size"][1] - 1.8) < 0.05  # aspect preserved
    assert entries[find_sid(data, 3, type="TABLE")]["rows"] == [["A", "B"], ["1", "2"]]


def test_table_structure_ops(deck, tmp_path):
    sid = find_sid(inspect(deck, "--slide", "1"), 1, type="TABLE")
    out = tmp_path / "out.pptx"
    r = apply_patch(deck, [
        {"op": "add-row", "slide": 1, "shape": sid, "cells": ["r2c0", "r2c1"]},
        {"op": "add-col", "slide": 1, "shape": sid, "cells": ["c2r0", "c2r1", "c2r2"]},
        {"op": "delete-row", "slide": 1, "shape": sid, "row": 1},
    ], out)
    assert r.returncode == 0, r.stdout + r.stderr
    rows = shapes_of(inspect(out, "--slide", "1"), 1)[sid]["rows"]
    assert rows == [["r0c0", "r0c1", "c2r0"], ["r2c0", "r2c1", "c2r2"]]


def test_merged_cell_guard(deck, tmp_path):
    from pptx.oxml.ns import qn
    prs = Presentation(deck)
    tbl = next(sh for sh in prs.slides[1].shapes if sh.has_table).table
    tbl._tbl.findall(qn("a:tr"))[0].findall(qn("a:tc"))[0].set("gridSpan", "2")
    merged = tmp_path / "merged.pptx"
    prs.save(merged)
    sid = find_sid(inspect(merged, "--slide", "1"), 1, type="TABLE")
    r = apply_patch(merged, [{"op": "add-row", "slide": 1, "shape": sid, "cells": ["a", "b"]}], tmp_path / "o.pptx")
    assert r.returncode == 1 and "merged cells" in r.stdout


def test_reorder_z(deck, tmp_path):
    data = inspect(deck, "--slide", "0")
    order = list(shapes_of(data, 0))
    out = tmp_path / "out.pptx"
    r = apply_patch(deck, [{"op": "reorder", "slide": 0, "shape": order[-1], "z": "back"}], out)
    assert r.returncode == 0
    assert list(shapes_of(inspect(out, "--slide", "0"), 0))[0] == order[-1]


def test_swap_image_media_global(deck, tmp_path):
    data = inspect(deck, "--slide", "1")
    media = shapes_of(data, 1)[find_sid(data, 1, type="PICTURE")]["media"]
    new_img = tmp_path / "new.png"
    Image.new("RGB", (200, 120), (200, 30, 30)).save(new_img)
    out = tmp_path / "out.pptx"
    r = apply_patch(deck, [{"op": "swap-image", "media": media, "image": str(new_img)}], out)
    assert r.returncode == 0 and "every reference changes" in r.stdout
    arc = "ppt/media/" + media
    assert zipfile.ZipFile(out).read(arc) != zipfile.ZipFile(deck).read(arc)
    r = apply_patch(deck, [{"op": "swap-image", "media": "nope.png", "image": str(new_img)}], tmp_path / "o2.pptx")
    assert r.returncode == 1 and "Available media" in r.stdout


def test_slides_subcommand_duplicates(deck, tmp_path):
    out = tmp_path / "out.pptx"
    r = run(deck, "slides", "0,2,2", "-o", out)
    assert r.returncode == 0, r.stdout + r.stderr
    assert len(Presentation(out).slides._sldIdLst) == 3


def test_merge_subcommand(deck, tmp_path):
    out = tmp_path / "out.pptx"
    r = run(deck, "merge", deck, "--slides", "0", "--at", "1", "-o", out)
    assert r.returncode == 0, r.stdout + r.stderr
    assert len(Presentation(out).slides._sldIdLst) == 4


def test_fix_repairs_overflowing_text(deck, tmp_path):
    data = inspect(deck, "--slide", "0")
    sid = find_sid(data, 0, paragraphs="Hello World")
    grown = tmp_path / "grown.pptx"
    long_text = "This is a very long line of replacement text. " * 12
    r = apply_patch(deck, [{"op": "set-text", "slide": 0, "shape": sid, "text": [long_text]}], grown)
    assert r.returncode == 0
    r = run(grown, "fix", "--slides", "0", "--in-place")
    assert r.returncode == 0
    assert "fixed" in r.stdout


def test_diff_reports_changes(deck, tmp_path):
    out = tmp_path / "out.pptx"
    data = inspect(deck, "--slide", "0")
    sid = find_sid(data, 0, paragraphs="Hello World")
    apply_patch(deck, [
        {"op": "set-text", "slide": 0, "shape": sid, "text": ["Changed"]},
        {"op": "move", "slide": 0, "shape": sid, "by": [0.5, 0]},
    ], out)
    r = run(deck, "diff", out)
    assert "Hello World -> Changed" in r.stdout and "moved" in r.stdout


@pytest.mark.skipif(shutil.which("soffice") is None, reason="LibreOffice not installed")
def test_render_names_by_zero_based_index(deck, tmp_path):
    imgdir = tmp_path / "img"
    r = run(deck, "render", "-o", imgdir, "--slide", "2")
    assert r.returncode == 0, r.stdout + r.stderr
    assert (imgdir / "slide-2.jpg").exists()
