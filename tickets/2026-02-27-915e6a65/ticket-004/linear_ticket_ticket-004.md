---
id: ticket-004
title: "Fix check_mode.py - Add return statement to execute()"
status: Todo
priority: High
order: 40
created: 2026-02-27
updated: 2026-02-27
links:
  - url: ../parent/linear_ticket_parent.md
    title: Parent Ticket
---

# Description

## Problem to solve
`check_mode.py` execute() function doesn't return a value, causing Rust to fail parsing the response.

## Solution
Add `return {"success": True}` at the end of successful execution.

## Implementation Details
- File: `resources/commands/modes/check_mode.py`
- Add return statement after successfully displaying mode
- This is a read-only command, no error case needed
- Test command execution: "джарвис, какой режим"
