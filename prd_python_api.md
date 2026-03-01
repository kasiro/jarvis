# Python API & Mode Manager PRD

## HR Eng

| Python API & Mode Manager PRD |  | **Summary:** Complete migration from Lua to Python for command scripting, implementing a Python API layer in Rust that mirrors the existing Lua API, and enhancing the Mode Manager system for commands.modes. |
| :---- | :---- | :---- |
| **Author**: Pickle Rick **Contributors**: AI Assistant **Intended audience**: Engineering, PM | **Status**: Draft **Created**: 2026-02-26 | **Self Link**: `prd_python_api.md` **Context**: Jarvis Core |

## Introduction

Jarvis currently uses Lua as its primary scripting language for voice commands. This PRD defines the requirements for:
1. Creating a **Python API** layer in Rust (mirroring Lua API)
2. Migrating existing Lua commands to Python
3. Implementing a robust **Mode Manager** system for `commands.modes`

## Problem Statement

**Current Process:** Commands are written in Lua with a Rust-based API layer (`jarvis-core/src/lua/`)

**Primary Users:** 
- End users who trigger voice commands
- Developers who write/maintain commands

**Pain Points:**
- Lua has limited ecosystem compared to Python
- Python offers better ML/AI library support
- Users want to leverage Python's extensive ecosystem
- Mode management is fragmented across Lua scripts

**Importance:** 
- Python is more widely known and easier to maintain
- Better integration with ML/AI features (Qwen API, etc.)
- Unified mode management system

## Objective & Scope

**Objective:** Replace Lua with Python as the primary command scripting language while maintaining backward compatibility during migration.

**Ideal Outcome:**
- All Lua commands migrated to Python
- Python API feature-complete with Lua API
- Mode Manager centralized and working across all modes

### In-scope or Goals
- ✅ Create `jarvis-core/src/python/` directory structure
- ✅ Implement Python API modules (core, state, system, http, audio, context, modes)
- ✅ Create Python engine in Rust (using `pyo3` or similar)
- ✅ Migrate `resources/commands/modes/*.lua` to Python
- ✅ Implement Mode Manager with event bus integration
- ✅ Support sandbox levels (minimal, standard, full)
- ✅ Maintain backward compatibility with Lua during migration

### Not-in-scope or Non-Goals
- ❌ Remove Lua support entirely (phase 2)
- ❌ Rewrite core Rust functionality
- ❌ Change existing command structure/phrases
- ❌ Modify Tauri GUI layer

## Product Requirements

### Critical User Journeys (CUJs)

1. **CUJ-1: User enables Kid Mode**
   - User says: "детский режим" or "kid mode"
   - System activates kid mode
   - Mode Manager publishes `mode_changed` event
   - All subscribers (commands, filters) receive notification
   - Sound plays: `ok1.mp3` or `ok2.mp3`
   - State persisted: `mode = "kid"`

2. **CUJ-2: User checks current mode**
   - User says: "какой режим" or "current mode"
   - System reads mode from state
   - Returns mode name via notification or TTS
   - No state change

3. **CUJ-3: Developer enables Dev Mode**
   - User says: "режим разработчика" or "dev mode"
   - System activates dev mode with full sandbox
   - Enhanced logging enabled
   - Dev-specific commands become available

4. **CUJ-4: Python command executes with sandbox**
   - User triggers any Python command
   - Python engine loads script
   - Sandbox level enforced (minimal/standard/full)
   - API calls restricted based on sandbox
   - Command executes within timeout
   - Result returned to core

### Functional Requirements

| Priority | Requirement | User Story |
| :---- | :---- | :---- |
| P0 | Python Engine | As a developer, I need a Python execution engine in Rust so that I can run Python scripts |
| P0 | Python API - Core | As a command developer, I need `jarvis.log()`, `jarvis.sleep()` so that I can log and control execution |
| P0 | Python API - State | As a command developer, I need `jarvis.state.get/set()` so that I can persist command state |
| P0 | Python API - System | As a command developer, I need `jarvis.system.notify()`, `jarvis.system.open()` so that I can interact with the OS |
| P0 | Python API - Context | As a command developer, I need `jarvis.context.phrase`, `jarvis.context.language` so that I can access command context |
| P0 | Python API - Audio | As a command developer, I need `jarvis.audio.play()` so that I can play sounds |
| P0 | Python API - HTTP | As a command developer, I need `jarvis.http.get()` so that I can make API calls |
| P0 | Python API - Modes | As a command developer, I need `jarvis.modes.get_current()`, `jarvis.modes.set_mode()` so that I can manage modes |
| P0 | Sandbox Levels | As a security engineer, I need sandbox enforcement (minimal/standard/full) so that commands can't access restricted APIs |
| P1 | Mode Manager | As a user, I need centralized mode management so that modes work consistently across all commands |
| P1 | Event Bus Integration | As a system, I need event publishing so that mode changes propagate to all subscribers |
| P1 | Migrate Modes Commands | As a user, I need kid/dev/normal modes to work in Python so that I can use them after migration |
| P2 | Lua Backward Compatibility | As a legacy user, I need existing Lua commands to still work so that migration doesn't break functionality |
| P2 | Python API - FS | As a command developer, I need `jarvis.fs.read()`, `jarvis.fs.write()` so that I can access files (full sandbox only) |

## Assumptions

- `pyo3` or similar Rust-Python FFI library is available and compatible with project
- Python 3.8+ is installed on target systems
- Existing Lua commands will be migrated incrementally
- Mode state is stored in `.state.json` per command or globally

## Risks & Mitigations

- **Risk**: Python embedding adds complexity to build process
  - **Mitigation**: Use `pyo3` with proper feature flags, document Python version requirements

- **Risk**: Sandbox enforcement in Python is harder than Lua
  - **Mitigation**: Use Python's `restrictedpython` or custom AST analysis, enforce at Rust level

- **Risk**: Performance degradation vs Lua
  - **Mitigation**: Benchmark critical paths, optimize hot paths, use PyO3's async features

- **Risk**: Mode state conflicts between concurrent commands
  - **Mitigation**: Use async locks in EventBus, ensure atomic state updates

## Tradeoff

**Options Considered:**
1. **Full Python migration (chosen)**: Best long-term, higher initial cost
2. **Lua + Python coexistence**: Lower initial cost, technical debt
3. **Stay with Lua only**: Lowest cost, limited ecosystem

**Why Python:**
- Larger ecosystem (ML, AI, data processing)
- Easier to find developers
- Better integration with Qwen AI and modern tools
- Future-proof for advanced features

## Business Benefits/Impact/Metrics

**Success Metrics:**

| Metric | Current State (Benchmark) | Future State (Target) | Savings/Impacts |
| :---- | :---- | :---- | :---- |
| Commands in Python | 0 | 100% of modes commands | Maintainability |
| Mode switch latency | ~100ms (Lua) | <150ms (Python) | Acceptable overhead |
| Developer onboarding | Medium (Lua knowledge) | High (Python knowledge) | Faster development |
| Code reuse | Low (Lua-only) | High (Python ecosystem) | Reduced development time |

## Stakeholders / Owners

| Name | Team/Org | Role | Note |
| :---- | :---- | :---- | :---- |
| Pickle Rick | Jarvis Core | Author/Engineer | God Mode implementation |
| Morty | User Testing | QA | Breaks things |
| AI Assistant | Development | Implementation | Does the actual work |
