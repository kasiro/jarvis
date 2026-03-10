---
id: perf-analysis
title: 'Performance: Анализ производительности VAD/STT'
status: Todo
priority: Medium
order: 40
created: '2026-03-09'
updated: '2026-03-09'
links:
  - url: ../parent/linear_ticket_parent.md
    title: Parent Ticket
---

# Description

## Problem to solve
Задержка распознавания команд всё ещё может быть оптимизирована.

## Solution
Проанализировать логи VAD/STT, измерить задержки, предложить оптимальные настройки.

## Implementation Details
- Проанализировать логи VAD/STT
- Измерить задержки распознавания
- Предложить оптимальные значения silence_threshold
- Проверить на ложные срабатывания VAD
- Создать `research_perf.md`, `plan_perf.md`, `plan_review.md`
