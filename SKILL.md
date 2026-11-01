---
name: sacred-numerology
description: Сакральная нумерология — полный разбор по дате рождения и имени (пифагорейская система, кириллица и латиница) с ведическими соответствиями Наваграх и славянскими акцентами. Расчёт через scripts/calculate.py.
---

# Сакральная нумерология

## Workflow
1. Собрать данные: дата рождения (обязательно), полное имя при рождении (для чисел имени), дата для личных циклов (по умолчанию сегодня).
2. Запустить: `python3 scripts/calculate.py --date ДД.ММ.ГГГГ --name "Имя Фамилия" [--on ГГГГ-ММ-ДД] [--y-vowel] [--format json|text]`.
3. Цитировать числа только из вывода скрипта (поле `value` и `chain`). Не пересчитывать «в уме».
4. Интерпретировать по references: methods.md (формулы), numbers.md (значения), karmic.md (долги/уроки), vedic-navagraha.md, slavic-accents.md.
5. Структура ответа — шаблон в `examples/ivan-ivanov-1990-08-15.md`.
6. Всегда добавлять оговорку: эзотерическая традиция, научных доказательств нет. Без медицинских, финансовых, фатальных прогнозов. Язык ответа — язык пользователя.

## Поля вывода
input, life_path, expression, soul_urge, personality, hidden_passion, balance, birthday, attitude, personal_year, personal_month, personal_day, karmic_debts, karmic_lessons, birthday_number, name_karmic_debts, vedic (moolank_psychic, bhagyank_destiny, namank_name, life_path_graha), slavic_accents, disclaimer.

## Файлы
- scripts/calculate.py — калькулятор (zero-dependency, Python 3.8+)
- references/methods.md, numbers.md, karmic.md, vedic-navagraha.md, slavic-accents.md
- references/number-meanings.md, vedic-slavic.md, birth-date.md, full-chart.md — сводные/алиасные файлы (канон — файлы выше)
- examples/ivan-ivanov-1990-08-15.{json,txt,md}
- evals/cases.json + scripts/run_evals.py
- platform-adaptations/ — версии для Gemini, ChatGPT, Claude
