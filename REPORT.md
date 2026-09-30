# Отчёт по практике: окружения и зависимости Python

## 1. Окружение

- **ОС:** macOS (Apple Silicon, arm64)
- **Python:** 3.12.10
- **Poetry:** 2.5.1 (установлен через pipx)
- **pip:** 25.0.1

## 2. Пути к интерпретаторам

**pip_project:**
- python --version → Python 3.12.10
- sys.executable → /Users/danielzanyshov/coding/mlops/practice_2_result/pip_project/.venv/bin/python

**poetry_project:**
- poetry env info --path → /Users/danielzanyshov/coding/mlops/practice_2_result/poetry_project/.venv
- poetry env info --executable → .../poetry_project/.venv/bin/python

## 3. Прямые зависимости

| Пакет | Назначение |
|---|---|
| requests | HTTP-запрос к Open-Meteo |
| matplotlib | Построение графика температуры |
| pandas | DataFrame, преобразование и выгрузка в CSV |
| pytest (test-группа) | Запуск автоматических тестов |
| ruff (dev-группа) | Линтер и форматтер |

numpy **не является прямой зависимостью**: plt_temp.py не импортирует numpy и не вызывает его напрямую. Он приходит транзитивно — через pandas и matplotlib.

## 4. Транзитивные зависимости (примеры)

| Прямая | Транзитивная (пример) |
|---|---|
| requests | urllib3, certifi, charset-normalizer, idna |
| pandas | numpy, python-dateutil, tzdata |
| matplotlib | contourpy, cycler, fonttools, kiwisolver, pillow, pyparsing, packaging |

## 5. Восстановление pip-окружения

После rm -rf .venv и python3.12 -m venv .venv зависимости были установлены командой python -m pip install -r requirements.txt.

Скрипт python plt_temp.py отработал успешно: создан temperature_24h.csv (25 строк, столбцы time, temperature_c, 24 строки данных). Воспроизводимость подтверждена.

## 6. Проверка групп Poetry

| Режим | pytest | ruff | plt_temp.py |
|---|---|---|---|
| poetry sync --only main | недоступен | недоступен | работает |
| poetry sync --only test | доступен (9.1.1) | недоступен | падает: ModuleNotFoundError: No module named 'requests' |
| poetry sync (все группы) | доступен | доступен | работает |

Первый режим показывает окружение только с runtime-зависимостями. Второй — что тестовые инструменты не тянут за собой основную программу; запуск скрипта без main-группы ожидаемо падает. Третий режим восстанавливает полное рабочее окружение.

## 7. Точечное обновление зависимости

- poetry show --outdated → пусто, устаревших пакетов нет.
- Для requests зафиксирован диапазон >=2.34.2,<3.0.0 (команда poetry add "requests@^2.34.2").
- poetry update requests → No dependencies to install or update.
- Версия requests осталась 2.34.2; pyproject.toml и poetry.lock не изменились.

**Объяснение:** на момент выполнения работы в PyPI нет версии requests, попадающей в диапазон >=2.34.2,<3.0.0 и одновременно новее установленной. Обновление не выходит за диапазон, потому что Poetry уважает ограничение из pyproject.toml. Отсутствие изменений — допустимый результат.

## 8. Чистое восстановление Poetry-проекта

- .venv удалён, poetry install пересоздал окружение из poetry.lock.
- poetry run pytest -v → 4 passed (без обращения к сети).
- poetry run python plt_temp.py → созданы temperature_24h.csv (25 строк) и temperature_24h.png.
- Один из промежуточных запусков получил HTTP 503 Service Unavailable от Open-Meteo. Благодаря response.raise_for_status() ошибка была явно поднята как HTTPError, а не замаскирована под ошибку разбора JSON. При повторном запуске API ответил корректно.

## 9. Сравнение подходов

| Возможность | venv + pip | Poetry |
|---|---|---|
| Изоляция окружения | venv | встроено |
| Установка пакетов | pip | встроено |
| Описание прямых зависимостей | вручную (requirements.txt) | pyproject.toml |
| Разрешение версий | нет (использует готовый список) | resolver |
| Lock-файл | нет | poetry.lock |
| Группы зависимостей | нет | test, dev и др. |
| Запуск внутри окружения | после активации | poetry run |

**Воспроизводимость в venv + pip** обеспечивается файлом requirements.txt, в котором pip freeze фиксирует точные версии всех установленных пакетов (прямых и транзитивных). Он не объясняет, какие зависимости выбраны разработчиком напрямую, и не поддерживает группы.

**Воспроизводимость в Poetry** обеспечивается двумя файлами: pyproject.toml (намерения: какие зависимости нужны и в каких диапазонах, какие группы) и poetry.lock (точное согласованное решение для всех пакетов). Poetry умеет пересчитывать только изменившиеся части, поддерживает группы и запускает команды внутри своего окружения.
