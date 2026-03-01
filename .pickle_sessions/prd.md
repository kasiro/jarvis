# Linux Command Execution Fix PRD

## HR Eng

| Linux Command Execution Fix PRD |  | [Summary: The Jarvis voice assistant is incorrectly using Windows-style command execution (`cmd /C`) on Linux systems. This causes commands to fail or behave unexpectedly. We need to fix the command spawning logic to use native Linux shell execution.] |
| :---- | :---- | :---- |
| **Author**: Pickle Rick **Contributors**: [kasiro] **Intended audience**: Engineering, PM | **Status**: Draft **Created**: 2026-02-23 | **Self Link**: `/home/kasiro/Документы/jarvis/.pickle_sessions/prd.md` **Context**: Jarvis Core | 

## Introduction

The Jarvis voice assistant project is a Rust-based voice-controlled desktop assistant. The issue was discovered when executing a voice command to open a browser - the logs show `Spawning: cmd /C bash ["-c", "xdg-open https://www.google.com &"]` which is incorrect for Linux systems.

## Problem Statement

**Current Process:** Commands are being executed using Windows-style `cmd /C` wrapper even on Linux systems.

**Primary Users:** Linux desktop users running Jarvis voice assistant.

**Pain Points:** 
- Commands fail to execute properly on Linux
- Unnecessary process overhead (cmd -> bash -> actual command)
- Potential path and environment variable issues
- Non-native behavior that breaks Linux conventions

**Importance:** Critical bug preventing proper command execution on Linux, which is a supported platform.

## Objective & Scope

**Objective:** Fix command execution to use native Linux shell spawning (`bash -c` or `sh -c`) instead of Windows `cmd /C`.

**Ideal Outcome:** Commands execute natively on Linux without Windows wrapper, matching the platform's conventions.

### In-scope or Goals
- Fix command spawning logic in `jarvis_core::commands` module
- Ensure platform-specific command execution (Windows vs Linux)
- Update any hardcoded `cmd /C` references
- Test command execution on Linux

### Not-in-scope or Non-Goals
- Windows command execution changes (unless broken by this fix)
- macOS specific handling (unless same issue exists)
- New command features or functionality

## Product Requirements

### Critical User Journeys (CUJs)
1. **Voice Command Execution**: User says "запусти браузер" -> Jarvis executes `xdg-open https://www.google.com` natively via `bash -c` on Linux
2. **Cross-Platform Compatibility**: Same command pack works on both Windows and Linux with appropriate shell handling

### Functional Requirements

| Priority | Requirement | User Story |
| :---- | :---- | :---- |
| P0 | Remove hardcoded `cmd /C` from Linux command execution | As a Linux user, I want commands to execute natively without Windows wrappers |
| P0 | Implement platform-specific command spawning | As a cross-platform user, I want Jarvis to use the correct shell for my OS |
| P1 | Preserve Windows compatibility | As a Windows user, I want commands to still work after the fix |
| P2 | Add logging to show actual command being executed | As a developer, I want to debug command execution issues easily |

## Assumptions

- The issue is in `jarvis_core::commands` module based on log output
- Rust's `std::process::Command` is being used for spawning
- The project targets both Windows and Linux platforms
- Command packs use a standard format that doesn't specify shell type

## Risks & Mitigations

- **Risk**: Windows command execution breaks after fix -> **Mitigation**: Implement proper platform detection using `cfg!(target_os = "windows")`
- **Risk**: Some commands rely on `cmd /C` behavior -> **Mitigation**: Audit all existing commands before making changes
- **Risk**: Environment variables behave differently -> **Mitigation**: Test with various command types (file operations, network, GUI apps)

## Tradeoff

**Option 1: Hardcode `bash -c` for all non-Windows**
- Pros: Simple, predictable
- Cons: Assumes bash is available (not true on all Unix systems)

**Option 2: Use `sh -c` for POSIX compliance**
- Pros: More portable across Unix-like systems
- Cons: May lack bash-specific features

**Chosen**: Option 1 with fallback - Use `bash -c` if available, fall back to `sh -c`. This matches the existing pattern in the logs where bash is already being used.

## Business Benefits/Impact/Metrics

**Success Metrics:**

| Metric | Current State (Benchmark) | Future State (Target) | Savings/Impacts |
| :---- | :---- | :---- | :---- |
| Command Success Rate (Linux) | ~0% (commands fail) | 100% | User satisfaction |
| Process Overhead | 3 processes (cmd->bash->cmd) | 1 process (bash) | Performance |
| Cross-Platform Bugs | 1 critical | 0 | Support costs |

## Stakeholders / Owners

| Name | Team/Org | Role | Note |
| :---- | :---- | :---- | :---- |
| kasiro | Jarvis | Developer | Reported the issue |
| Pickle Rick | Engineering | Fix Engineer | Implementing the solution |
