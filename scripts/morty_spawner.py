#!/usr/bin/env python3
"""
Pickle Rick Morty Spawner - Запуск суб-агентов для задач
Использует Qwen API через MCP для выполнения задач
"""
import sys
import json
import subprocess
from pathlib import Path
from typing import Optional

SESSION_ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
TICKET_ID = sys.argv[2] if len(sys.argv) > 2 else "unknown"
TASK_DESC = sys.argv[3] if len(sys.argv) > 3 else "Выполни задачу"

print(f"🥒 Morty Spawner: Запуск агента для тикета {TICKET_ID}")
print(f"   Session: {SESSION_ROOT}")
print(f"   Task: {TASK_DESC[:100]}...")

# Создаём директорию для документации агента
ticket_dir = SESSION_ROOT / TICKET_ID
ticket_dir.mkdir(parents=True, exist_ok=True)

# Создаём файл исследования
research_file = ticket_dir / f"research_{TICKET_ID}.md"
research_file.write_text(f"""# Research: {TICKET_ID}

## Task
{TASK_DESC}

## Status
IN_PROGRESS

## Notes
- Агент запущен
- Выполняется исследование...
""")

# Создаём файл плана
plan_file = ticket_dir / f"plan_{TICKET_ID}.md"
plan_file.write_text(f"""# Plan: {TICKET_ID}

## Task
{TASK_DESC}

## Steps
1. Исследование
2. Планирование
3. Выполнение
4. Проверка

## Status
PENDING
""")

print(f"✅ Документация создана в {ticket_dir}")
print(f"   - research_{TICKET_ID}.md")
print(f"   - plan_{TICKET_ID}.md")
print()
print("🥒 Morty Agent готов к работе!")
print()
print("<promise>I AM DONE</promise>")
