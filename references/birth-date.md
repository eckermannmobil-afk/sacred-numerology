# Числа даты рождения

Life Path, Birthday (birthday_number), Attitude, Personal Year/Month/Day.

## Редукция
- Складываем цифры, пока не останется 1–9.
- **Мастер-числа 11, 22, 33** не редуцируются в Life Path, Expression, Soul Urge, Personality, Birthday, Attitude (и в редукции отдельных частей имени).
- В Balance, Personal Year/Month/Day и ведических числах — всегда до 1–9.
- Цепочка (`chain`) хранит все промежуточные суммы; если в ней встречается 13/14/16/19 — это кармический долг.

## Числа даты
- **Life Path** = reduce(день) + reduce(месяц) + reduce(сумма цифр года) → reduce (мастер сохраняется).
- **Birthday** = reduce(день), мастер 11/22 сохраняется; сырой день 13/14/16/19 = кармический долг.
- **Attitude** = reduce(день + месяц).

## Личные циклы (на дату `--on`, по умолчанию сегодня)
- **Personal Year** = reduce(день) + reduce(месяц рождения) + reduce(сумма цифр текущего года) → 1–9.
- **Personal Month** = Personal Year + номер календарного месяца → 1–9.
- **Personal Day** = Personal Month + календарный день → 1–9.

