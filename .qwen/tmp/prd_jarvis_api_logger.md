# Jarvis API Python Logger Dual Output PRD

## HR Eng

| Jarvis API Python Logger Dual Output PRD |  | Modify the Python jarvis_api logger to simultaneously write logs to both console and file. |
| :---- | :---- | :---- |
| **Author**: Pickle Rick **Contributors**: N/A **Intended audience**: Engineering | **Status**: Draft **Created**: 2026-03-27 | **Self Link**: [Link] **Context**: [Link] 

## Introduction

The Jarvis Python API (`resources/commands/jarvis_api/`) provides logging functionality via `log()` function in `core.py`. Currently, the logger uses Python's `logging` module but lacks proper handler configuration for dual output (console + file).

## Problem Statement

**Current Process:** The `jarvis_server.py` has basic `logging.basicConfig()` with only stderr stream handler. The `jarvis_api/core.py` uses `logging.getLogger(__name__)` without dedicated handlers.
**Primary Users:** Python command developers, users debugging command execution.
**Pain Points:** Logs are only visible in stderr stream, no persistent file logging for post-mortem analysis.
**Importance:** Developers need real-time console output AND persistent file logs for debugging.

## Objective & Scope

**Objective:** Configure Python logger in `jarvis_api` to output logs to both console (stderr) and file simultaneously.
**Ideal Outcome:** All `jarvis.log()` calls write to stderr (for real-time monitoring) AND to a log file (for persistence).

### In-scope or Goals
- Add FileHandler to `jarvis_api/core.py` logger configuration
- Ensure logs go to both console (stderr) and file
- Use existing log directory structure (`APP_LOG_DIR` from Rust core)
- Maintain backward compatibility with existing commands

### Not-in-scope or Non-Goals
- Changing `jarvis_server.py` logging (separate concern)
- Modifying log levels or formats in other modules
- Changes to Rust logging system

## Product Requirements

### Critical User Journeys (CUJs)
1. **Command Execution**: User runs a Python command that calls `jarvis.log("info", "test")`. Log appears in stderr console.
2. **File Persistence**: After command execution, user finds log file in `~/.local/share/jarvis/logs/` (or similar).
3. **Debug Session**: Developer monitors stderr in real-time while also having persistent file logs for later analysis.

### Functional Requirements

| Priority | Requirement | User Story |
| :---- | :---- | :---- |
| P0 | Logger must output to stderr (console) | As a developer, I want to see logs in stderr so I can monitor in real-time. |
| P0 | Logger must output to file | As a user, I want logs saved to file so I can review later. |
| P1 | Both outputs must receive same messages | As a developer, I want consistency between outputs. |
| P1 | Log file should be in standard location | As a user, I want logs in a predictable directory. |
| P2 | Log rotation (optional) | As a user, I want old logs to be rotated to prevent disk fill. |

## Assumptions

- Python's `logging` module supports multiple handlers (StreamHandler + FileHandler).
- Log directory is accessible and writable by the Python process.
- The `APP_LOG_DIR` or similar path can be passed from Rust to Python via context.

## Risks & Mitigations

- **Risk**: FileHandler may fail if directory doesn't exist. -> **Mitigation**: Create directory if needed, or fallback to stderr-only.
- **Risk**: Duplicate log messages if handlers not configured properly. -> **Mitigation**: Set `propagate=False` on logger.
- **Risk**: Performance impact from file I/O. -> **Mitigation**: Use buffered FileHandler.

## Tradeoff

- **Option 1**: Configure handlers in `core.py` directly.
  - **Pros**: Self-contained, no external dependencies.
  - **Cons**: Hardcoded log path or requires context passing.
- **Option 2**: Centralized logging config in `jarvis_server.py`.
  - **Pros**: Single point of configuration.
  - **Cons**: Requires passing log path from Rust.

**Chosen**: Option 1 with lazy initialization - configure handlers on first `log()` call, using log path from context or default.

## Business Benefits/Impact/Metrics

**Success Metrics:**

| Metric | Current State (Benchmark) | Future State (Target) | Savings/Impacts |
| :---- | :---- | :---- | :---- |
| Log visibility | stderr only | stderr + file | Improved debugging |
| Debug time | High (no persistence) | Low (file available) | Developer productivity |
| Log retention | None | File-based | Post-mortem analysis |

## Stakeholders / Owners

| Name | Team/Org | Role | Note |
| :---- | :---- | :---- | :---- |
| User | N/A | Requester | Needs dual logging |
