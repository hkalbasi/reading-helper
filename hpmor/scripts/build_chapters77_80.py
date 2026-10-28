#!/usr/bin/env python3
"""Build chapter pages from archived sources and annotated batches."""
import hashlib
import html as htmllib
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
CHAPTERS = {
    77: ("SA, Aftermaths: Surface Appearances", "20261003224352"),
    78: ("Taboo Tradeoffs Prelude: Cheating", "20261003224403"),
    79: ("Taboo Tradeoffs, Pt 1", "20260605011850"),
    80: ("Taboo Tradeoffs, Pt 2, The Horns Effect", "20260605011850"),
    81: ("Taboo Tradeoffs, Pt 3", "20260330103949"),
    82: ("Taboo Tradeoffs, Final", "20261003224410"),
    83: ("Taboo Tradeoffs, Aftermath 1", "20261003224359"),
    84: ("Taboo Tradeoffs, Aftermath 2", "20261003224410"),
    85: ("Taboo Tradeoffs, Aftermath 3, Distance", "20260718152904"),
    86: ("Multiple Hypothesis Testing", "20260926164735"),
    87: ("Hedonic Awareness", "20260420221213"),
    88: ("Time Pressure, Pt 1", "20260330213751"),
    89: ("Time Pressure, Pt 2", "20261003224425"),
    90: ("Roles, Pt 1", "20261003224441"),
}


def build(chapter):
    title, capture = CHAPTERS[chapter]
    source_path = ROOT / "data" / f"ch{chapter}_source.json"
    source = json.loads(source_path.read_text(encoding="utf-8"))
    source_by_num = {item["n"]: item["html"] for item in source}

    pattern = re.compile(rf"ch{chapter}_part(\d+)_sections\.json$")
    batches = sorted(
        (path for path in (ROOT / "data").glob(f"ch{chapter}_part*_sections.json")
         if pattern.fullmatch(path.name)),
        key=lambda path: int(pattern.fullmatch(path.name).group(1)),
    )
    if not batches:
        raise FileNotFoundError(f"no annotated batches found for chapter {chapter}")

    sections = []
    for path in batches:
        sections.extend(json.loads(path.read_text(encoding="utf-8")))
    sections = [{**section, "id": index} for index, section in enumerate(sections, 1)]

    covered = [number for section in sections for number in section["paras"]]
    expected = list(range(1, len(source_by_num) + 1))
    if covered != expected:
        raise ValueError(f"chapter {chapter} batches must cover source paragraphs 1–{len(expected)} in order")

    data = []
    for section in sections:
        translated = [part.strip() for part in section["translation_fa"].split("\n\n") if part.strip()]
        if len(translated) != len(section["paras"]):
            raise ValueError(f"chapter {chapter} section {section['id']}: translation paragraph count mismatch")
        data.append({
            **section,
            "verbatim_html": [source_by_num[number] for number in section["paras"]],
        })

    (ROOT / "data" / f"ch{chapter}_sections.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (ROOT / "data" / f"ch{chapter}.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    def text_paras(text):
        parts = [part.strip() for part in text.split("\n\n") if part.strip()]
        return "".join(f"<p>{htmllib.escape(part)}</p>" for part in parts)

    concat = "".join(item for section in data for item in section["verbatim_html"])
    sha = hashlib.sha256(concat.encode("utf-8")).hexdigest()[:16]
    paragraph_count = len(covered)
    rows = []
    for section in data:
        verbatim = "".join(f"<p>{item}</p>" for item in section["verbatim_html"])
        summary_en = f"<p>{htmllib.escape(section['summary_en'])}</p>"
        translated = text_paras(section["translation_fa"])
        summary_fa = text_paras(section["summary_fa"])
        para_numbers = ",".join(map(str, section["paras"]))
        rows.append(
            f'<tr id="sec-{section["id"]}">'
            f'<td data-label="Section"><span class="sec-id">§{section["id"]}</span><br>'
            f'<span class="para-nums">¶{para_numbers}</span></td>'
            f'<td data-label="1. Verbatim English" class="verbatim" dir="ltr" lang="en">{verbatim}</td>'
            f'<td data-label="2. Summarized English" dir="ltr" lang="en">{summary_en}</td>'
            f'<td data-label="3. Persian translation (verbatim)" class="trans" dir="rtl" lang="fa">{translated}</td>'
            f'<td data-label="4. Persian summary" dir="rtl" lang="fa">{summary_fa}</td>'
            "</tr>"
        )

    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Chapter {chapter}: {title} — 4-column parallel summary</title>
<link rel="stylesheet" href="assets/styles.css">
</head>
<body>
<header class="site"><div class="wrap">
<h1>Chapter {chapter}: {title}</h1>
<p class="subtitle">Harry Potter and the Methods of Rationality · {len(data)} sections · {paragraph_count} paragraphs ·
<a href="index.html">← all chapters</a></p>
<span class="badge">✓ verbatim verified · sha {sha} · {paragraph_count}/{paragraph_count} exact</span>
</div></header>
<div class="toolbar"><div class="wrap">
<strong>Columns:</strong> 1. Verbatim English &nbsp;|&nbsp; 2. Summarized English &nbsp;|&nbsp; 3. Persian translation (close to verbatim) &nbsp;|&nbsp; 4. Persian summary
<span style="margin-inline-start:auto">Source: <a href="https://web.archive.org/web/{capture}/http://hpmor.com/chapter/{chapter}">Wayback capture of hpmor.com/chapter/{chapter}</a> ·
<a href="data/ch{chapter}_source.json">source JSON</a> · run <code>python3 scripts/verify.py</code></span>
</div></div>
<main class="wrap">
<table class="parallel">
<colgroup><col class="c-sec"><col class="c-en"><col class="c-sum"><col class="c-fa"><col class="c-fasum"></colgroup>
<thead><tr>
<th>§</th><th>1. Verbatim English content</th><th>2. Summarized English content</th>
<th dir="rtl" lang="fa">۳. ترجمهٔ فارسی (نزدیک به متن)</th><th dir="rtl" lang="fa">۴. خلاصهٔ فارسی</th>
</tr></thead>
<tbody>
{''.join(rows)}
</tbody>
</table>
</main>
<footer><div class="wrap">Verbatim English © Eliezer Yudkowsky / J.K. Rowling-derived fanfiction, reproduced for study with summaries &amp; translations. Verify: <code>python3 scripts/verify.py</code></div></footer>
</body>
</html>
"""
    (ROOT / f"chapter{chapter}.html").write_text(page, encoding="utf-8")
    print(f"wrote chapter{chapter}.html: {len(data)} sections, {paragraph_count} paragraphs, sha {sha}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python3 scripts/build_chapters77_80.py CHAPTER")
    build(int(sys.argv[1]))
