#!/usr/bin/env python3
"""Run evals/cases.json against calculate.py. Exit 1 on any mismatch."""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from calculate import calculate, parse_date
base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
fails = 0
for c in json.load(open(os.path.join(base, "evals", "cases.json"), encoding="utf-8")):
    r = calculate(parse_date(c["date"]), c["name"], parse_date(c["on"]))
    got = {k: r[k]["value"] for k in ("life_path", "expression", "soul_urge", "personality", "balance",
                                      "birthday", "attitude", "personal_year", "personal_month", "personal_day")}
    got.update(hidden_passion=r["hidden_passion"]["values"], karmic_lessons=r["karmic_lessons"],
               karmic_debts=[d["number"] for d in r["karmic_debts"]],
               moolank=r["vedic"]["moolank_psychic"]["number"], bhagyank=r["vedic"]["bhagyank_destiny"]["number"],
               namank=r["vedic"]["namank_name"]["number"])
    for k, v in c["expect"].items():
        ok = got[k] == v
        fails += not ok
        print(("PASS" if ok else "FAIL"), c["name"], k, "expected", v, "got", got[k])
print("FAILS:", fails)
sys.exit(1 if fails else 0)
