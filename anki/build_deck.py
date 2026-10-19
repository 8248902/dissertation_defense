#!/usr/bin/env python3
"""Build the defense's spoken-recall deck and a portable text fallback."""

from collections import Counter
import csv
from datetime import datetime, timezone
import hashlib
import html
import json
from pathlib import Path
import re
import sqlite3
import tempfile
import zipfile

import chevron
import genanki


HERE = Path(__file__).resolve().parent
DEFENSE = HERE.parent
DECK_NAME = "Defense — Spoken Mathematics"
MODEL_NAME = "Defense — Oral Fluency"
DECK_ID = 1926101901
MODEL_ID = 1926101902
FIELDS = ["ID", "Topic", "Priority", "Question", "Answer", "Anchors", "More", "Sources"]
TOPICS = {
    "foundations": "Foundations",
    "temporal": "Temporal reconstruction",
    "flow": "Optical flow",
    "stereo": "Stereo depth",
    "synthesis": "Connecting the talk",
}
CSS = """
.card { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  font-size: 21px; line-height: 1.55; text-align: left; color: #202c38;
  background: #fafbf9; max-width: 780px; margin: 0 auto; padding: 24px; }
.meta { font-size: 13px; color: #586a72; letter-spacing: .035em; margin-bottom: 16px; }
.question { font-size: 25px; font-weight: 650; line-height: 1.35; }
.cue, .label { font-size: 14px; color: #586a72; }
.cue { margin-top: 24px; }
.answer { margin: 20px 0; }
.anchors { border-left: 3px solid #248979; padding-left: 14px; font-size: 17px; }
details { font-size: 16px; margin: 20px 0 0; }
summary { cursor: pointer; color: #24766c; }
.sources { font-size: 13px; overflow-wrap: anywhere; }
hr { border: 0; border-top: 1px solid #cbd4d0; margin: 24px 0; }
.nightMode, .night_mode { background: #172329; color: #e5eee9; }
.nightMode .meta, .nightMode .cue, .nightMode .label { color: #b3c5c0; }
.nightMode summary { color: #83cfc2; }
"""
FRONT = """<div class="meta">{{Topic}} · {{Priority}} · {{ID}}</div>
<div class="question">{{Question}}</div>
<div class="cue">Answer aloud in your own words, then reveal.</div>"""
BACK = """<div class="meta">{{Topic}} · {{Priority}} · {{ID}}</div>
<div class="question">{{Question}}</div><hr id="answer">
<div class="label">One way to say it</div><div class="answer">{{Answer}}</div>
<div class="anchors"><span class="label">Keep these ideas</span><br>{{Anchors}}</div>
<details><summary>If pressed</summary><p>{{More}}</p></details>
<details class="sources"><summary>Return to the talk / source</summary>{{Sources}}</details>"""


def esc(value):
    return html.escape(value, quote=True)


def read_cards():
    cards = []
    for block in re.split(r"(?m)^@ ", (HERE / "cards.txt").read_text(encoding="utf-8"))[1:]:
        lines = block.strip().splitlines()
        header = [part.strip() for part in lines[0].split("|")]
        if len(header) != 5:
            raise ValueError(f"Malformed card header: {lines[0]}")
        card_id, topic, priority, pages, labels = header
        card = dict(id=card_id, topic=topic, priority=priority,
                    slide_keys=[key.strip() for key in pages.split(",")],
                    labels=[label for label in labels.split(",") if label])
        for line in lines[1:]:
            key, value = line.split(": ", 1)
            if key in card:
                raise ValueError(f"Duplicate field in {card_id}: {key}")
            card[key] = value
        assert {"Q", "A", "Keep", "More"} <= card.keys(), card_id
        assert topic in TOPICS and priority in {"core", "followup"}, card_id
        assert len(card["Keep"].split(";")) == 3, card_id
        assert 15 <= len(card["A"].split()) <= 100, card_id
        cards.append(card)
    assert len({c["id"] for c in cards}) == len(cards)
    assert len({c["Q"] for c in cards}) == len(cards)
    # Present the essential rehearsal path first, retaining talk order within each tier.
    return sorted(cards, key=lambda card: card["priority"] != "core")


def enrich(cards):
    with (DEFENSE / "source-map.csv").open(encoding="utf-8", newline="") as handle:
        slide_rows = list(csv.DictReader(handle))
    slides = {row["slide_title"]: row for row in slide_rows}
    assert len(slides) == len(slide_rows), "Slide titles must be unique to resolve anchors."
    slide_anchors = json.loads((HERE / "slide_titles.json").read_text(encoding="utf-8"))
    references = json.loads((DEFENSE / "thesis-references.json").read_text())["labels"]
    script = (DEFENSE / "defense-script.md").read_text(encoding="utf-8")
    proof_reference = DEFENSE.parent / "dissertation_proof_reference_2026-10-10" / "chapter_3_4_proof_reference.tex"
    proof_text = proof_reference.read_text(encoding="utf-8")
    for card in cards:
        source_parts = []
        for key in card["slide_keys"]:
            slide = slides[slide_anchors[key]]
            page = int(slide["pdf_slide"])
            script_title = slide["slide_title"].replace("$H^1$", "H¹")
            assert script_title in script, (card["id"], page)
            source_parts.append(f"Deck p. {page}: {esc(script_title)}")
        for label in card["labels"]:
            ref = references[label]  # Fail immediately on a missing dissertation reference.
            title = ref["title"] or label
            title = title.replace("$L^1$", "L¹").replace("$\\mathbf {M}$", "M")
            title = re.sub(r"~\\ref\s*\{([^}]+)\}",
                           lambda match: " " + references[match[1]]["number"], title)
            prefix = {"thm": "Theorem", "lem": "Lemma", "prop": "Proposition", "cor": "Corollary"}.get(label.split(":")[0])
            name = f"{prefix} {ref['number']}: {title}" if prefix else title
            if label.startswith("eq:"):
                name = f"Equation ({ref['number']})"
            source_parts.append(f"Dissertation p. {esc(str(ref['page']))}: {esc(name)}")
        if any("proofref:" + label in proof_text for label in card["labels"]):
            source_parts.append("Proof companion: Chapters 3–4 claim–justification tables (10 October 2026), corresponding result.")
        card["fields"] = [
            esc(card["id"]), esc(TOPICS[card["topic"]]),
            "Core rehearsal" if card["priority"] == "core" else "Deeper follow-up",
            esc(card["Q"]), esc(card["A"]),
            " · ".join(esc(item.strip()) for item in card["Keep"].split(";")),
            esc(card["More"]), "<br><br>".join(source_parts),
        ]
        card["tags"] = ["defense", f"priority::{card['priority']}", f"topic::{card['topic']}"]
        context = dict(zip(FIELDS, card["fields"]))
        # Fields are already escaped or intentionally contain generated HTML.
        # Anki's field substitutions do not HTML-escape a second time.
        card["front"] = chevron.render(FRONT.replace("{{", "{{{").replace("}}", "}}}"), context)
        card["back"] = chevron.render(BACK.replace("{{", "{{{").replace("}}", "}}}"), context)
    return proof_reference


def build_package(cards, filename):
    model = genanki.Model(
        MODEL_ID, MODEL_NAME, fields=[{"name": field} for field in FIELDS],
        templates=[{"name": "Speak the answer", "qfmt": FRONT, "afmt": BACK}],
        css=CSS, sort_field_index=0,
    )
    deck = genanki.Deck(DECK_ID, DECK_NAME, description=(
        "Spoken recall for Daniel Blauvelt's defense. Core rehearsal cards come first; "
        "follow-ups deepen the same talk. Explain the result, its role, and its limits "
        "in your own words. Source edition: 19 October 2026."
    ))
    for index, card in enumerate(cards):
        note = genanki.Note(model=model, fields=card["fields"], tags=card["tags"],
                            guid=genanki.guid_for("blauvelt-defense-oral-v1", card["id"]),
                            due=index + 1)
        deck.add_note(note)
    output = HERE / filename
    genanki.Package(deck).write_to_file(str(output))
    return output


def write_fallback(cards):
    with (HERE / "defense-oral.tsv").open("w", encoding="utf-8", newline="") as handle:
        handle.write("#separator:tab\n#html:true\n#notetype:Basic\n")
        handle.write(f"#deck:{DECK_NAME}\n#tags column:3\n#columns:Front\tBack\tTags\n")
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        for card in cards:
            writer.writerow([card["front"].replace("\n", ""),
                             card["back"].replace("\n", ""), " ".join(card["tags"])])


def write_preview(cards):
    core = sum(c["priority"] == "core" for c in cards)
    parts = ["<!doctype html><html lang='en'><meta charset='utf-8'>",
             "<meta name='viewport' content='width=device-width,initial-scale=1'>",
             "<title>Defense oral-recall deck</title><style>", CSS,
             "body { max-width: 850px; margin: auto; padding: 20px; background: #fafbf9; font-family: sans-serif; }",
             "article { padding: 22px 0; border-bottom: 1px solid #cbd4d0; } article > details > summary { font-size: 21px; }",
             "h2 { margin-top: 45px; } p { line-height: 1.6; }",
             "</style><h1>Defense: spoken mathematics</h1>",
             f"<p>{len(cards)} cards: {core} core rehearsal, {len(cards)-core} deeper follow-ups. "
             "Say your answer before opening a card. The wording is a model, not a script.</p>",
             "<p><a href='#core'>Core rehearsal</a> · <a href='#followup'>Deeper follow-ups</a></p>"]
    last_priority = None
    for card in cards:
        if card["priority"] != last_priority:
            last_priority = card["priority"]
            parts.append(f"<h2 id='{last_priority}'>{'Core rehearsal' if last_priority == 'core' else 'Deeper follow-ups'}</h2>")
        parts.append(f"<article id='{card['id']}'><div class='meta'>{esc(card['id'])} · {esc(TOPICS[card['topic']])}</div>")
        parts.append(f"<details><summary>{esc(card['Q'])}</summary><div class='card'>{card['back']}</div></details></article>")
    parts.append("</html>")
    (HERE / "preview.html").write_text("\n".join(parts), encoding="utf-8")


def verify_package(output, cards, check_fallback=True):
    with zipfile.ZipFile(output) as archive:
        assert archive.testzip() is None
        assert set(archive.namelist()) == {"collection.anki2", "media"}
        assert json.loads(archive.read("media")) == {}
        with tempfile.TemporaryDirectory(prefix="defense-anki-check-") as scratch:
            db = Path(scratch) / "collection.anki2"
            db.write_bytes(archive.read("collection.anki2"))
            with sqlite3.connect(db) as conn:
                assert conn.execute("pragma integrity_check").fetchone()[0] == "ok"
                assert conn.execute("select count(*) from notes").fetchone()[0] == len(cards)
                assert conn.execute("select count(*) from cards").fetchone()[0] == len(cards)
                assert conn.execute("select count(distinct guid) from notes").fetchone()[0] == len(cards)
                models, decks = conn.execute("select models, decks from col").fetchone()
                assert json.loads(models)[str(MODEL_ID)]["tmpls"][0]["qfmt"] == FRONT
                assert json.loads(decks)[str(DECK_ID)]["name"] == DECK_NAME
                rows = conn.execute("select guid, flds, tags from notes order by id").fetchall()
                for card, (guid, fields, tags) in zip(cards, rows):
                    assert guid == genanki.guid_for("blauvelt-defense-oral-v1", card["id"])
                    assert fields.split("\x1f") == card["fields"], card["id"]
                    assert all(tag in tags.split() for tag in card["tags"]), card["id"]
                    assert "{{" not in card["front"] and "{{" not in card["back"]
                    assert card["Q"] in html.unescape(card["front"])
                    assert card["A"] in html.unescape(card["back"])
                assert [row[0] for row in conn.execute("select due from cards order by id")] == list(range(1, len(cards) + 1))
    if check_fallback:
        with (HERE / "defense-oral.tsv").open(encoding="utf-8", newline="") as handle:
            rows = list(csv.reader((line for line in handle if not line.startswith("#")), delimiter="\t"))
        assert len(rows) == len(cards) and all(len(row) == 3 for row in rows)


def write_manifest(cards, proof_reference):
    inputs = [HERE / "cards.txt", HERE / "build_deck.py", HERE / "README.txt",
              HERE / "slide_titles.json", DEFENSE / "core.tex",
              DEFENSE / "backup.tex", DEFENSE / "defense-script.md", DEFENSE / "source-map.csv",
              DEFENSE / "thesis-references.json", proof_reference]
    inputs.extend(sorted((DEFENSE.parent / "dissertation_thesis" / "shared_bodies").glob("ch[234]*_body.tex")))
    payload = {
        "built_at_utc": datetime.now(timezone.utc).isoformat(),
        "deck_name": DECK_NAME, "notes": len(cards), "cards": len(cards),
        "priorities": dict(Counter(c["priority"] for c in cards)),
        "topics": dict(Counter(c["topic"] for c in cards)),
        "checks": ["stable slide-title anchors resolve to current live defense pages",
                   "all dissertation labels resolve in bundled compiled references",
                   "unique IDs, prompts and stable note GUIDs",
                   "one forward card per note; core cards first",
                   "ZIP CRC, SQLite integrity, model, deck, fields and tags",
                   "front/back field rendering and TSV round-trip"],
        "verification_scope": "Package structure and rendered fields; no desktop Anki GUI import was performed.",
        "source_sha256": {str(path.relative_to(DEFENSE)) if path.is_relative_to(DEFENSE) else str(path):
                          hashlib.sha256(path.read_bytes()).hexdigest() for path in inputs},
        "output_sha256": {name: hashlib.sha256((HERE / name).read_bytes()).hexdigest()
                          for name in ["defense-oral.apkg", "defense-core.apkg", "defense-oral.tsv", "preview.html"]},
    }
    (HERE / "manifest.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return payload


def main():
    cards = read_cards()
    proof_reference = enrich(cards)
    output = build_package(cards, "defense-oral.apkg")
    core_cards = [card for card in cards if card["priority"] == "core"]
    core_output = build_package(core_cards, "defense-core.apkg")
    write_fallback(cards)
    write_preview(cards)
    verify_package(output, cards)
    verify_package(core_output, core_cards, check_fallback=False)
    payload = write_manifest(cards, proof_reference)
    print(json.dumps({key: payload[key] for key in ["notes", "cards", "priorities", "topics"]}, indent=2))
    print(f"Verified package: {output}")


if __name__ == "__main__":
    main()
