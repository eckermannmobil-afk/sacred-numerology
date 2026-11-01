# Отчёт о проверке platform-adaptations — sacred-numerology

Дата: 01.11.2026 (Europe/Berlin). Проверял: Grok Bot (самопроверка + автоматический скрипт; доступа к Claude API нет, поэтому Claude для проверки не использовался).

## Созданные файлы
- /workspace/artifacts/sacred-numerology/platform-adaptations/gemini-instructions.md — Gemini Gem (PERSONA/TASK/CONTEXT/PROCESS/FORMAT, Knowledge из Google Drive, запуск через Colab)
- /workspace/artifacts/sacred-numerology/platform-adaptations/chatgpt-instructions.md — Custom GPT (блок Instructions ≈4 тыс. символов при лимите 8 000; детали — в Knowledge; запуск через Code Interpreter)
- /workspace/artifacts/sacred-numerology/platform-adaptations/claude-instructions.md — Claude Project (длинные XML-инструкции, все 5 references встроены целиком, self-check; заметка про Agent Skills)
- /workspace/artifacts/sacred-numerology/platform-adaptations/verify_adaptations.py — автопроверка
- /workspace/artifacts/sacred-numerology/platform-adaptations/VERIFICATION-REPORT.md — этот отчёт

## ⚠️ Главная находка: исходного skill не было
Папки /workspace/artifacts/sacred-numerology на боксе не существовало; поиск по всему боксу, Google Drive, GitHub и памяти ничего не дал. Поэтому базовый skill **собран заново** в том же формате, что bazhai-master / astrology:
SKILL.md, README.md, CHANGELOG.md, scripts/calculate.py, scripts/run_evals.py, references/{methods,numbers,karmic,vedic-navagraha,slavic-accents}.md, examples/ivan-ivanov-1990-08-15.{md,json,txt}, evals/cases.json.
Если у пользователя есть своя версия (другая таблица букв, другие правила долгов) — её нужно положить в эту папку и перезапустить проверку; адаптации придётся сверить заново.

## Что проверено
1. **Движок calculate.py** — evals/cases.json: 2 кейса (кириллица «Иван Иванов», латиница «Ivan Ivanov»), 24 проверки → `FAILS: 0`. Ожидаемые значения посчитаны вручную независимо от скрипта:
   Иван = И1+В3+А1+Н6 = 11 (мастер), Иванов = 21→3, Expression 14→5 (долг 14); гласные 2+9 = 11; согласные 9+12→3 = 12→3; частоты 1×4, 3×3, 6×2, 7×1 → Hidden Passion 1, уроки 2,4,5,8,9; Balance И+И = 2; Life Path 6+8+1 = 15→6; Attitude 23→5; PY 2026 = 6+8+1 = 15→6, PM ноябрь 17→8, PD 1-е = 9; Bhagyank 33→6, Namank 32→5.
2. **Каждая из 3 адаптаций** (verify_adaptations.py, 78 проверок на файл):
   - все 17 полей вывода скрипта (input … disclaimer);
   - все 5 файлов references/;
   - 32 концепта: 11 чисел (Life Path … Personal Day), долги 13/4, 14/5, 16/7, 19/1, кармические уроки, Наваграхи + Moolank/Bhagyank/Namank + оговорка про халдейскую таблицу, славянские акценты, мастер-числа, обе таблицы букв, оговорка «эзотерическая традиция, научных доказательств нет», команда `calculate.py --date` и флаги --on/--y-vowel/--format, пример 15.08.1990 «Иван Иванов»;
   - 9 грах (Сурья … Мангала);
   - 15 чисел эталонного примера сверены с живым выводом скрипта.
   Результат: **78/78 OK для каждого файла**. Негативный тест (удалил два поля из ChatGPT-версии) — чекер их поймал.
3. **Ручное чтение**: шаблон разбора (8 разделов) есть во всех трёх; формулы совпадают с calculate.py; платформенные особенности соблюдены.

## Что найдено и исправлено
| # | Находка | Исправление |
|---|---|---|
| 1 | Исходный skill отсутствует | Собран базовый skill + evals (см. выше) |
| 2 | В первой версии скрипта долг сырого дня рождения засчитывался в Life Path, а общий список долгов был без источников | `karmic_debts` → `[{number, sources}]`; долг дня — в `birthday` |
| 3 | ChatGPT: в шапке неверная оценка длины Instructions (6,5 тыс.) | Измерено 4 046 символов, текст исправлен |
| 4 | ChatGPT: лишний шаг «скопировать /mnt/data/calculate.py» | Уточнено: Knowledge-файлы лежат в /mnt/data/ |
| 5 | Gemini: слишком категоричное утверждение про автообновление файлов из Drive | Смягчено + запасной вариант «переподключить файл» |
| 6 | Gems не гарантируют исполнение Python | Добавлен путь через Google Colab и ручной расчёт с показом цепочек |

## Известные ограничения (не ошибки)
- Namank считается по пифагорейской таблице (классика — халдейская); это явно помечено в скрипте и во всех версиях.
- Промежуточное 19 при сворачивании года (1990→19→1) не считается кармическим долгом — так задумано (долги берутся из цепочек основных чисел и сырого дня рождения).
- «Славянская нумерология» подана как современная реконструкция фольклорных образов.

## Как перепроверить
```bash
cd /workspace/artifacts/sacred-numerology
python3 scripts/run_evals.py
python3 platform-adaptations/verify_adaptations.py
```

## Повторная проверка 2026-11-01 (v1.0.1)
- Добавлены поля birthday_number, name_karmic_debts; 4 reference-файла. Evals 24/24, адаптации 84/84.
