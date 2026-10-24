#!/usr/bin/env python3
"""Build chapter76.html and its aligned data from the archived source and annotations."""
import hashlib
import html as htmllib
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
source = json.loads((ROOT / "data" / "ch76_source.json").read_text(encoding="utf-8"))
sections = json.loads((ROOT / "data" / "ch76_sections.json").read_text(encoding="utf-8"))
source_by_num = {item["n"]: item["html"] for item in source}

covered = [number for section in sections for number in section["paras"]]
if len(covered) != len(set(covered)) or sorted(covered) != sorted(source_by_num):
    raise ValueError("chapter 76 sections must cover every source paragraph exactly once")

data = []
for section in sections:
    translation_paras = [part.strip() for part in section["translation_fa"].split("\n\n") if part.strip()]
    if len(translation_paras) != len(section["paras"]):
        raise ValueError(f"section {section['id']}: translation paragraph count does not match source")
    data.append({
        **section,
        "verbatim_html": [source_by_num[number] for number in section["paras"]],
    })

(ROOT / "data" / "ch76.json").write_text(
    json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)

def text_paras(text):
    parts = [part.strip() for part in text.split("\n\n") if part.strip()]
    return "".join(f"<p>{htmllib.escape(part)}</p>" for part in parts)

concat = "".join(item for section in data for item in section["verbatim_html"])
sha = hashlib.sha256(concat.encode("utf-8")).hexdigest()[:16]
paragraph_count = sum(len(section["paras"]) for section in data)
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
<title>Chapter 76: Interlude with the Confessor: Sunk Costs — 4-column parallel summary</title>
<link rel="stylesheet" href="assets/styles.css">
</head>
<body>
<header class="site"><div class="wrap">
<h1>Chapter 76: Interlude with the Confessor: Sunk Costs</h1>
<p class="subtitle">Harry Potter and the Methods of Rationality · {len(data)} sections · {paragraph_count} paragraphs ·
<a href="index.html">← all chapters</a></p>
<span class="badge">✓ verbatim verified · sha {sha} · {paragraph_count}/{paragraph_count} exact</span>
</div></header>
<div class="toolbar"><div class="wrap">
<strong>Columns:</strong> 1. Verbatim English &nbsp;|&nbsp; 2. Summarized English &nbsp;|&nbsp; 3. Persian translation (close to verbatim) &nbsp;|&nbsp; 4. Persian summary
<span style="margin-inline-start:auto">Source: <a href="https://web.archive.org/web/20260603150436/http://hpmor.com/chapter/76">Wayback capture of hpmor.com/chapter/76</a> ·
<a href="data/ch76_source.json">source JSON</a> · run <code>python3 scripts/verify.py</code></span>
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
(ROOT / "chapter76.html").write_text(page, encoding="utf-8")
print(f"wrote chapter76.html: {len(data)} sections, {paragraph_count} paragraphs, sha {sha}")
