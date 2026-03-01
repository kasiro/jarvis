# Python Command Execute Function Return Value Fix PRD

## HR Eng

| Python Command Execute Function Return Value Fix PRD |  | Fix Python command scripts that don't return proper JSON response to Rust, causing "Failed to parse response" errors |
| :---- | :---- | :---- |
| **Author**: Pickle Rick **Contributors**: [Names] **Intended audience**: Engineering, PM, Design | **Status**: Draft **Created**: 2026-02-27 | **Self Link**: [Link] **Context**: [Link] 

## Introduction

Jarvis voice assistant uses Python scripts for command execution. The Rust core executes Python scripts via `jarvis_server.py` which uses MessagePack for RPC communication. When Python scripts don't return proper response objects, the Rust side fails to parse the response, causing command execution errors.

## Problem Statement

**Current Process:** Python command scripts execute but don't return explicit success/failure responses
**Primary Users:** Jarvis users executing voice commands
**Pain Points:** Commands fail with "Failed to parse response: expected value at line 1 column 1" error, breaking user experience
**Importance:** Critical - voice commands are core functionality, failures make Jarvis appear broken

### Root Cause Analysis

The issue occurs in the command execution flow:

1. **Rust side** (`jarvis-core/src/commands.rs:605`):
   ```rust
   let response: Value = serde_json::from_slice(&output.stdout)
       .map_err(|e| format!("Failed to parse response: {}", e))?;
   ```
   Expects JSON response: `{"success": true}` or `{"success": false, "error": "..."}`

2. **Python server** (`jarvis_server.py`):
   ```python
   result = await execute_func(context)
   return {
       "id": request_id,
       "type": "result",
       "success": True,
       "result": result
   }
   ```
   Returns `result: None` when execute() doesn't return anything

3. **Python scripts** (e.g., `kid_mode_on.py`):
   ```python
   async def execute(context):
       # ... does stuff ...
       # NO RETURN STATEMENT!
   ```
   Implicitly returns `None`

## Objective & Scope

**Objective:** Ensure all Python command scripts return proper response objects
**Ideal Outcome:** All commands execute successfully without parse errors

### In-scope or Goals
- Fix `kid_mode_on.py` to return proper response
- Fix `kid_mode_off.py` to return proper response  
- Fix `dev_mode_on.py` to return proper response
- Fix `check_mode.py` to return proper response
- Verify all other Python commands in `resources/commands/` return proper responses
- Update documentation if needed

### Not-in-scope or Non-Goals
- Changing Rust-side parsing logic
- Modifying `jarvis_server.py` RPC protocol
- Adding new features to commands

## Product Requirements

### Critical User Journeys (CUJs)

1. **CUJ-1: User activates Kid Mode**
   - User says: "джарвис, детский режим"
   - Jarvis recognizes wake word and command
   - `kid_mode_on.py` executes successfully
   - VPN connects, YouTube Kids opens
   - No errors in logs
   - User hears OK sound and sees notification

2. **CUJ-2: User activates Dev Mode**
   - User says: "джарвис, режим разработчика"
   - Jarvis recognizes wake word and command
   - `dev_mode_on.py` executes successfully
   - Windows maximize for dev workspace
   - No errors in logs
   - User hears OK sound and sees notification

### Functional Requirements

| Priority | Requirement | User Story |
| :---- | :---- | :---- |
| P0 | All Python execute() functions must return a dict | As a user, I want commands to work without errors |
| P1 | Return format must be `{"success": bool}` or `{"success": bool, "result": any}` | As a developer, I need consistent response format |
| P2 | Error cases must return `{"success": false, "error": "message"}` | As a user, I want to know when commands fail |
| P3 | All existing commands must be audited for compliance | As a maintainer, I want to prevent future issues |

## Assumptions

- Python scripts use `jarvis_api` for execution context
- `jarvis_server.py` correctly serializes return values to MessagePack
- Rust side correctly deserializes MessagePack to JSON

## Risks & Mitigations

- **Risk**: Other commands have the same issue -> **Mitigation**: Audit all Python commands in `resources/commands/`
- **Risk**: Return value changes break existing logic -> **Mitigation**: Test all affected commands after fix
- **Risk**: MessagePack serialization issues -> **Mitigation**: Verify with actual execution tests

## Tradeoff

**Option 1: Fix Python scripts only** (CHOSEN)
- Pros: Minimal changes, follows existing pattern
- Cons: Need to audit all scripts

**Option 2: Make Rust more tolerant**
- Pros: More forgiving of missing returns
- Cons: Masks underlying inconsistency, harder to debug

## Business Benefits/Impact/Metrics

**Success Metrics:**

| Metric | Current State (Benchmark) | Future State (Target) | Savings/Impacts |
| :---- | :---- | :---- | :---- |
| Command success rate | <100% (parse errors) | 100% | Improved UX |
| Error log frequency | Multiple per session | Zero | Easier debugging |
| User satisfaction | Degraded by failures | Restored | Trust in system |

## Stakeholders / Owners

| Name | Team/Org | Role | Note |
| :---- | :---- | :---- | :---- |
| Pickle Rick | Engineering | Fixer | Making it Solenya-tight |
