#!/usr/bin/env python3
"""Mechanical verification: column-1 verbatim text must exactly match source (ch7 + ch8)."""
import json, hashlib, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]

CHAPTERS = {
    "ch7": ("data/ch7_source.json", "data/ch7.json"),
    "ch8": ("data/ch8_source.json", "data/ch8.json"),
    "ch9": ("data/ch9_source.json", "data/ch9.json"),
    "ch10": ("data/ch10_source.json", "data/ch10.json"),
    "ch11": ("data/ch11_source.json", "data/ch11.json"),
    "ch12": ("data/ch12_source.json", "data/ch12.json"),
    "ch13": ("data/ch13_source.json", "data/ch13.json"),
    "ch14": ("data/ch14_source.json", "data/ch14.json"),
    "ch15": ("data/ch15_source.json", "data/ch15.json"),
    "ch16": ("data/ch16_source.json", "data/ch16.json"),
    "ch17": ("data/ch17_source.json", "data/ch17.json"),
    "ch18": ("data/ch18_source.json", "data/ch18.json"),
    "ch19": ("data/ch19_source.json", "data/ch19.json"),
    "ch20": ("data/ch20_source.json", "data/ch20.json"),
}

failed = False
for name, (src_file, data_file) in CHAPTERS.items():
    src = json.loads((ROOT / src_file).read_text(encoding="utf-8"))
    data = json.loads((ROOT / data_file).read_text(encoding="utf-8"))

    srcmap = {r["n"]: r["html"] for r in src}
    total = 0
    bad = []
    for sec in data:
        for pn, vh in zip(sec["paras"], sec["verbatim_html"]):
            total += 1
            if srcmap.get(pn) != vh:
                bad.append((sec["id"], pn))

    covered = sorted(p for s in data for p in s["paras"])
    missing = [n for n in srcmap if n not in covered]
    extra = [n for n in covered if n not in srcmap]

    concat = "".join(vh for s in sorted(data, key=lambda x: x["id"]) for vh in s["verbatim_html"])
    sha = hashlib.sha256(concat.encode("utf-8")).hexdigest()

    print(f"[{name}] sections: {len(data)}, table_paragraphs: {total}, source_paragraphs: {len(srcmap)}")
    print(f"[{name}] sha256(verbatim_concat): {sha}")
    if bad or missing or extra or total != len(srcmap):
        print(f"[{name}] FAIL: bad={bad[:5]} missing={missing[:10]} extra={extra[:10]}")
        failed = True
    else:
        print(f"[{name}] OK: {total}/{len(srcmap)} paragraphs exact match")

sys.exit(1 if failed else 0)
