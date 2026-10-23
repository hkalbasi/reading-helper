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
    "ch21": ("data/ch21_source.json", "data/ch21.json"),
    "ch22": ("data/ch22_source.json", "data/ch22.json"),
    "ch23": ("data/ch23_source.json", "data/ch23.json"),
    "ch24": ("data/ch24_source.json", "data/ch24.json"),
    "ch25": ("data/ch25_source.json", "data/ch25.json"),
    "ch26": ("data/ch26_source.json", "data/ch26.json"),
    "ch27": ("data/ch27_source.json", "data/ch27.json"),
    "ch28": ("data/ch28_source.json", "data/ch28.json"),
    "ch29": ("data/ch29_source.json", "data/ch29.json"),
    "ch30": ("data/ch30_source.json", "data/ch30.json"),
    "ch31": ("data/ch31_source.json", "data/ch31.json"),
    "ch32": ("data/ch32_source.json", "data/ch32.json"),
    "ch33": ("data/ch33_source.json", "data/ch33.json"),
    "ch34": ("data/ch34_source.json", "data/ch34.json"),
    "ch35": ("data/ch35_source.json", "data/ch35.json"),
    "ch36": ("data/ch36_source.json", "data/ch36.json"),
    "ch37": ("data/ch37_source.json", "data/ch37.json"),
    "ch38": ("data/ch38_source.json", "data/ch38.json"),
    "ch39": ("data/ch39_source.json", "data/ch39.json"),
    "ch40": ("data/ch40_source.json", "data/ch40.json"),
    "ch41": ("data/ch41_source.json", "data/ch41.json"),
    "ch42": ("data/ch42_source.json", "data/ch42.json"),
    "ch43": ("data/ch43_source.json", "data/ch43.json"),
    "ch44": ("data/ch44_source.json", "data/ch44.json"),
    "ch45": ("data/ch45_source.json", "data/ch45.json"),
    "ch46": ("data/ch46_source.json", "data/ch46.json"),
    "ch47": ("data/ch47_source.json", "data/ch47.json"),
    "ch48": ("data/ch48_source.json", "data/ch48.json"),
    "ch49": ("data/ch49_source.json", "data/ch49.json"),
    "ch50": ("data/ch50_source.json", "data/ch50.json"),
    "ch51": ("data/ch51_source.json", "data/ch51.json"),
    "ch52": ("data/ch52_source.json", "data/ch52.json"),
    "ch53": ("data/ch53_source.json", "data/ch53.json"),
    "ch54": ("data/ch54_source.json", "data/ch54.json"),
    "ch55": ("data/ch55_source.json", "data/ch55.json"),
    "ch56": ("data/ch56_source.json", "data/ch56.json"),
    "ch57": ("data/ch57_source.json", "data/ch57.json"),
    "ch58": ("data/ch58_source.json", "data/ch58.json"),
    "ch59": ("data/ch59_source.json", "data/ch59.json"),
    "ch60": ("data/ch60_source.json", "data/ch60.json"),
    "ch61": ("data/ch61_source.json", "data/ch61.json"),
    "ch62": ("data/ch62_source.json", "data/ch62.json"),
    "ch63": ("data/ch63_source.json", "data/ch63.json"),
    "ch64": ("data/ch64_source.json", "data/ch64.json"),
    "ch65": ("data/ch65_source.json", "data/ch65.json"),
    "ch66": ("data/ch66_source.json", "data/ch66.json"),
    "ch67": ("data/ch67_source.json", "data/ch67.json"),
    "ch68": ("data/ch68_source.json", "data/ch68.json"),
    "ch69": ("data/ch69_source.json", "data/ch69.json"),
    "ch70": ("data/ch70_source.json", "data/ch70.json"),
    "ch71": ("data/ch71_source.json", "data/ch71.json"),
    "ch72": ("data/ch72_source.json", "data/ch72.json"),
    "ch73": ("data/ch73_source.json", "data/ch73.json"),
    "ch74": ("data/ch74_source.json", "data/ch74.json"),
    "ch75": ("data/ch75_source.json", "data/ch75.json"),
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
