---
id: ticket-002
title: "Fix kid_mode_off.py - Add return statement to execute()"
status: Todo
priority: High
order: 20
created: 2026-02-27
updated: 2026-02-27
links:
  - url: ../parent/linear_ticket_parent.md
    title: Parent Ticket
---

# Description

## Problem to solve
`kid_mode_off.py` execute() function doesn't return a value, causing Rust to fail parsing the response.

## Solution
Add `return {"success": True}` at the end of successful execution and `return {"success": False, "error": "..."}` on failure.

## Implementation Details
- File: `resources/commands/modes/kid_mode_off.py`
- Add return statement after successful mode deactivation
- Add return statement in error handling branch
- Test command execution: "джарвис, обычный режим"
