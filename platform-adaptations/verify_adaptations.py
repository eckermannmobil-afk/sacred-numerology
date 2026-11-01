#!/usr/bin/env python3
"""Check that each platform adaptation reflects all script fields, references, concepts and example numbers."""
import json, os, re, sys
base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(base, "scripts"))
from calculate import FIELDS, NAVAGRAHA, calculate, parse_date
ex = calculate(parse_date("15.08.1990"), "Иван Иванов", parse_date("2026-11-01"))
assert set(ex) == set(FIELDS), "FIELDS out of sync with output"
refs = sorted(os.listdir(os.path.join(base, "references")))
concepts = {
 "Life Path": r"Life Path", "Expression": r"Expression", "Soul Urge": r"Soul Urge", "Personality": r"Personality",
 "Hidden Passion": r"Hidden Passion", "Balance": r"Balance", "Birthday": r"Birthday", "Attitude": r"Attitude",
 "Personal Year": r"Personal Year", "Personal Month": r"Personal Month", "Personal Day": r"Personal Day",
 "debt 13": r"13\s*(/|→)\s*4|13→4|13/4", "debt 14": r"14\s*(/|→)\s*5", "debt 16": r"16\s*(/|→)\s*7", "debt 19": r"19\s*(/|→)\s*1",
 "karmic lessons": r"(?i)кармическ\w* урок|Karmic Lessons", "Navagraha": r"(?i)Наваграх|Navagraha",
 "Slavic": r"(?i)славянск", "Moolank": "Moolank", "Bhagyank": "Bhagyank", "Namank": "Namank",
 "Chaldean note": r"(?i)халдейск|Chaldean", "master numbers": r"11/22/33|11, 22, 33",
 "disclaimer": r"эзотерическая традиция, научных доказательств нет",
 "script": r"calculate\.py --date", "flag --on": r"--on", "flag --y-vowel": r"--y-vowel", "flag --format": r"--format",
 "example date": r"15\.08\.1990", "example name": r"Иван Иванов",
 "cyrillic table": r"А1 Б2 В3|\| А \| Б \| В", "latin table": r"A J S\s*=\s*1|A J S=1",
}
for n, (g, p) in NAVAGRAHA.items():
    concepts[f"graha {n} {g}"] = re.escape(g.split("/")[0])
expected_nums = {  # (label, regex) from the live script output for the reference example
 "LP 6": r"Life Path[^\n]{0,40}\b6\b", "Expr 5": r"Expression[^\n]{0,40}\b5\b|14→5",
 "Soul 11": r"Soul Urge[^\n]{0,40}\b11\b", "Pers 3": r"Personality[^\n]{0,40}\b3\b|12→3",
 "HP 1": r"Hidden Passion[^\n]{0,20}\b1\b", "Bal 2": r"Balance[^\n]{0,20}\b2\b",
 "Bday 6": r"Birthday[^\n]{0,20}\b6\b", "Att 5": r"Attitude[^\n]{0,20}\b5\b|23→5",
 "PY 6": r"(PY|Personal Year)[^\n]{0,30}\b6\b", "PM 8": r"(PM|Month)[^\n]{0,30}\b8\b|17→8",
 "PD 9": r"(PD|Day)[^\n]{0,30}\b9\b", "debt 14 source": r"14[^\n]{0,30}expression",
 "lessons": r"2,\s*4,\s*5,\s*8,\s*9", "bhagyank 33→6": r"33→6", "namank 5 Будха": r"Будха",
}
assert ex["life_path"]["value"] == 6 and ex["expression"]["value"] == 5 and ex["soul_urge"]["value"] == 11
assert ex["personal_month"]["value"] == 8 and ex["karmic_lessons"] == [2, 4, 5, 8, 9]
total_fail = 0
for fn in ("gemini-instructions.md", "chatgpt-instructions.md", "claude-instructions.md"):
    t = open(os.path.join(base, "platform-adaptations", fn), encoding="utf-8").read()
    miss = [f for f in FIELDS if f not in t] + [r for r in refs if r not in t]
    miss += [k for k, p in concepts.items() if not re.search(p, t)]
    miss += [k for k, p in expected_nums.items() if not re.search(p, t)]
    total_fail += len(miss)
    checks = len(FIELDS) + len(refs) + len(concepts) + len(expected_nums)
    print(f"{fn}: {checks - len(miss)}/{checks} OK" + (f"  MISSING: {miss}" if miss else ""))
print("TOTAL MISSING:", total_fail)
sys.exit(1 if total_fail else 0)
