#!/usr/bin/env python3
"""Sacred numerology calculator (Pythagorean system, Cyrillic + Latin).

Zero-dependency. Usage:
  python3 scripts/calculate.py --date 15.08.1990 --name "Иван Иванов"
  python3 scripts/calculate.py --date 1990-08-15 --name "Ivan Ivanov" --on 2026-11-01 --format text

Output (JSON, default): see FIELDS below. Esoteric tradition, not science.
"""
import argparse, datetime as dt, json, re, sys
from collections import Counter

MASTER = {11, 22, 33}
KARMIC_DEBT = {13, 14, 16, 19}

LATIN = {c: (i % 9) + 1 for i, c in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ")}
CYRILLIC = {c: (i % 9) + 1 for i, c in enumerate("АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ")}
VOWELS = set("AEIOU") | set("АЕЁИОУЫЭЮЯ")

NAVAGRAHA = {
    1: ("Сурья", "Солнце"), 2: ("Чандра", "Луна"), 3: ("Гуру/Брихаспати", "Юпитер"),
    4: ("Раху", "северный лунный узел"), 5: ("Будха", "Меркурий"), 6: ("Шукра", "Венера"),
    7: ("Кету", "южный лунный узел"), 8: ("Шани", "Сатурн"), 9: ("Мангала", "Марс"),
}

FIELDS = ["input", "life_path", "expression", "soul_urge", "personality", "hidden_passion",
          "balance", "birthday", "attitude", "personal_year", "personal_month", "personal_day",
          "karmic_debts", "karmic_lessons", "birthday_number", "name_karmic_debts", "vedic", "slavic_accents", "disclaimer"]


def digits_sum(n):
    return sum(int(d) for d in str(n))


def reduce(n, keep_master=True):
    """Reduce to 1-9, keeping 11/22/33 if keep_master. Returns (value, chain)."""
    chain = [n]
    while n > 9 and not (keep_master and n in MASTER):
        n = digits_sum(n)
        chain.append(n)
    return n, chain


def debt_in(chain):
    return sorted({x for x in chain if x in KARMIC_DEBT})


def parse_date(s):
    for fmt in ("%d.%m.%Y", "%Y-%m-%d", "%d/%m/%Y"):
        try:
            return dt.datetime.strptime(s, fmt).date()
        except ValueError:
            pass
    raise SystemExit(f"Не удалось разобрать дату: {s} (форматы ДД.ММ.ГГГГ или ГГГГ-ММ-ДД)")


def letter_value(ch, y_vowel=False):
    ch = ch.upper()
    v = LATIN.get(ch) or CYRILLIC.get(ch)
    if v is None:
        return None
    is_vowel = ch in VOWELS or (y_vowel and ch == "Y")
    return v, is_vowel


def name_parts(name):
    return [p for p in re.split(r"[\s\-]+", name.strip()) if p]


def name_number(parts, which, y_vowel):
    """which: all | vowels | consonants. Pythagorean: reduce each name part, then sum."""
    part_vals, raw_total = [], 0
    for p in parts:
        s = 0
        for ch in p:
            lv = letter_value(ch, y_vowel)
            if not lv:
                continue
            v, vow = lv
            if which == "all" or (which == "vowels" and vow) or (which == "consonants" and not vow):
                s += v
        raw_total += s
        pv, pchain = reduce(s)
        part_vals.append({"part": p, "sum": s, "reduced": pv, "chain": pchain})
    compound = sum(x["reduced"] for x in part_vals)
    value, chain = reduce(compound)
    debts = sorted(set(debt_in(chain)) | {d for x in part_vals for d in debt_in(x["chain"])})
    return {"value": value, "compound": compound, "raw_letter_sum": raw_total,
            "chain": chain, "parts": part_vals, "karmic_debt": debts}


def calculate(date, name, on, y_vowel=False):
    d, m, y = date.day, date.month, date.year
    rd, rm, ry = reduce(d)[0], reduce(m)[0], reduce(digits_sum(y))[0]
    lp_compound = rd + rm + ry
    lp, lp_chain = reduce(lp_compound)
    lp_debts = debt_in(lp_chain)
    full_digits = digits_sum(int(date.strftime("%d%m%Y")))

    parts = name_parts(name)
    expr = name_number(parts, "all", y_vowel)
    soul = name_number(parts, "vowels", y_vowel)
    pers = name_number(parts, "consonants", y_vowel)

    letter_vals = [letter_value(ch, y_vowel)[0] for ch in "".join(parts) if letter_value(ch, y_vowel)]
    cnt = Counter(letter_vals)
    top = max(cnt.values()) if cnt else 0
    hidden = sorted(k for k, v in cnt.items() if v == top)
    lessons = [n for n in range(1, 10) if n not in cnt]

    initials = [letter_value(p[0], y_vowel)[0] for p in parts if letter_value(p[0], y_vowel)]
    bal, bal_chain = reduce(sum(initials), keep_master=False)

    bday, bday_chain = reduce(d)
    att, att_chain = reduce(d + m)

    py_compound = rd + rm + reduce(digits_sum(on.year))[0]
    py, py_chain = reduce(py_compound, keep_master=False)
    pm, pm_chain = reduce(py + on.month, keep_master=False)
    pd_, pd_chain = reduce(pm + on.day, keep_master=False)

    debt_sources = {"life_path": lp_debts, "birthday": debt_in([d]),
                    "expression": expr["karmic_debt"], "soul_urge": soul["karmic_debt"],
                    "personality": pers["karmic_debt"]}
    all_debts = [{"number": n, "sources": [k for k, v in debt_sources.items() if n in v]}
                 for n in sorted({n for v in debt_sources.values() for n in v})]

    moolank = reduce(d, keep_master=False)[0]
    bhagyank = reduce(full_digits, keep_master=False)[0]
    namank = reduce(expr["raw_letter_sum"], keep_master=False)[0]

    def graha(n):
        g = NAVAGRAHA[reduce(n, keep_master=False)[0]]
        return {"number": reduce(n, keep_master=False)[0], "graha": g[0], "planet": g[1]}

    return {
        "input": {"date": date.isoformat(), "name": name, "on": on.isoformat(),
                  "system": "pythagorean", "y_as_vowel": y_vowel},
        "life_path": {"value": lp, "compound": lp_compound, "chain": lp_chain,
                      "components": {"day": rd, "month": rm, "year": ry}, "karmic_debt": lp_debts},
        "expression": expr, "soul_urge": soul, "personality": pers,
        "hidden_passion": {"values": hidden, "count": top, "frequencies": dict(sorted(cnt.items()))},
        "balance": {"value": bal, "initials": initials, "chain": bal_chain},
        "birthday": {"value": bday, "day": d, "chain": bday_chain,
                     "karmic_debt": debt_in([d])},
        "attitude": {"value": att, "compound": d + m, "chain": att_chain},
        "personal_year": {"value": py, "year": on.year, "chain": py_chain},
        "personal_month": {"value": pm, "month": on.month, "chain": pm_chain},
        "personal_day": {"value": pd_, "day": on.day, "chain": pd_chain},
        "karmic_debts": all_debts,
        "karmic_lessons": lessons,
        "birthday_number": bday,
        "name_karmic_debts": [x for x in all_debts if set(x["sources"]) & {"expression", "soul_urge", "personality"}],
        "vedic": {"moolank_psychic": graha(moolank), "bhagyank_destiny": graha(bhagyank),
                  "namank_name": graha(namank), "life_path_graha": graha(lp),
                  "note": "Ведическая традиция обычно считает имя по халдейской таблице; здесь Namank — по пифагорейской, как ориентир."},
        "slavic_accents": {"life_path": reduce(lp, keep_master=False)[0],
                           "birthday": moolank, "personal_year": py,
                           "see": "references/slavic-accents.md"},
        "disclaimer": "Нумерология — эзотерическая традиция, научных доказательств нет.",
    }


def to_text(r):
    L = [f"Дата: {r['input']['date']} | Имя: {r['input']['name']} | На дату: {r['input']['on']}"]
    for k, label in [("life_path", "Life Path"), ("expression", "Expression"), ("soul_urge", "Soul Urge"),
                     ("personality", "Personality"), ("balance", "Balance"), ("birthday", "Birthday"),
                     ("attitude", "Attitude"), ("personal_year", "Personal Year"),
                     ("personal_month", "Personal Month"), ("personal_day", "Personal Day")]:
        L.append(f"{label}: {r[k]['value']}  (цепочка {r[k]['chain']})")
    L.append(f"Hidden Passion: {r['hidden_passion']['values']} (x{r['hidden_passion']['count']})")
    debts = ", ".join(f"{x['number']} ({'/'.join(x['sources'])})" for x in r["karmic_debts"])
    L.append(f"Кармические долги: {debts or 'нет'}")
    L.append(f"Кармические уроки: {r['karmic_lessons'] or 'нет'}")
    v = r["vedic"]
    for k in ("moolank_psychic", "bhagyank_destiny", "namank_name", "life_path_graha"):
        L.append(f"Веда {k}: {v[k]['number']} → {v[k]['graha']} ({v[k]['planet']})")
    L.append(r["disclaimer"])
    return "\n".join(L)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--date", required=True, help="Дата рождения ДД.ММ.ГГГГ или ГГГГ-ММ-ДД")
    ap.add_argument("--name", required=True, help="Полное имя при рождении (кириллица или латиница)")
    ap.add_argument("--on", default=None, help="Дата для Personal Year/Month/Day (по умолчанию сегодня)")
    ap.add_argument("--y-vowel", action="store_true", help="Считать латинскую Y гласной")
    ap.add_argument("--format", choices=["json", "text"], default="json")
    a = ap.parse_args(argv)
    on = parse_date(a.on) if a.on else dt.date.today()
    r = calculate(parse_date(a.date), a.name, on, a.y_vowel)
    print(json.dumps(r, ensure_ascii=False, indent=2) if a.format == "json" else to_text(r))


if __name__ == "__main__":
    main()
