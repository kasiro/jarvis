# Rebuild GUI Flag PRD

## HR Eng

| Rebuild GUI Flag PRD |  | [Summary: Modify rebuild.sh to only build GUI when --gui flag is explicitly passed, making GUI building opt-in instead of opt-out.] |
| :---- | :---- | :---- |
| **Author**: Pickle Rick **Contributors**: kasiro **Intended audience**: Engineering, PM, Design | **Status**: Draft **Created**: 2026-02-27 | **Self Link**: [Link] **Context**: [Link] 

## Introduction

The `rebuild.sh` script currently builds both `jarvis-app` and `jarvis-gui` by default. The user must explicitly pass `--skip-gui` to avoid building the GUI. This is inefficient for development workflows where GUI is rarely needed.

## Problem Statement

**Current Process:** Full build (app + GUI) runs by default. User must pass `--skip-gui` to skip GUI.
**Primary Users:** Developers working on Jarvis CLI/GUI
**Pain Points:** 
- Wasted time building GUI when only CLI is needed
- Unnecessary resource consumption during development
- GUI build takes significant time (Tauri timeout: 600s)
**Importance:** Improves developer productivity and reduces build times for CLI-focused work.

## Objective & Scope

**Objective:** Make GUI building opt-in via `--gui` flag instead of opt-out.
**Ideal Outcome:** Running `./rebuild.sh` without flags only builds `jarvis-app`. GUI builds only when `--gui` is explicitly passed.

### In-scope or Goals
- Modify argument parsing to add `--gui` flag
- Change default behavior: no GUI build by default
- Update help text and logic flow
- Maintain backward compatibility with existing flags

### Not-in-scope or Non-Goals
- Changing build profiles (dev-fast, release)
- Modifying post_build.sh behavior
- Changing jarvis-app build logic

## Product Requirements

### Critical User Journeys (CUJs)
1. **Default Build (No Flags)**: User runs `./rebuild.sh` → Only `jarvis-app` builds, GUI is skipped.
2. **GUI Build**: User runs `./rebuild.sh --gui` → Both `jarvis-app` and `jarvis-gui` build.
3. **Fast Build**: User runs `./rebuild.sh --fast` → Only `jarvis-app` builds in dev-fast profile.
4. **Fast + GUI**: User runs `./rebuild.sh --fast --gui` → Both build with GUI in release mode.

### Functional Requirements

| Priority | Requirement | User Story |
| :---- | :---- | :---- |
| P0 | Add `--gui` flag to argument parser | As a developer, I want to explicitly enable GUI building so I can control build time. |
| P0 | Change default behavior to skip GUI | As a developer, I want default builds to skip GUI so I can iterate faster on CLI. |
| P0 | Update help text | As a user, I want clear documentation of the new behavior. |
| P1 | Maintain `--skip-gui` for backward compatibility (deprecated) | As a legacy user, I want old scripts to still work. |

## Assumptions

- Developers primarily work on CLI and only occasionally need GUI
- GUI build takes significantly longer than app build
- `--gui` flag should work with all other flags (--fast, --clean, --rustpotter)

## Risks & Mitigations

- **Risk**: Existing automation scripts expect GUI to build by default → **Mitigation**: Keep `--skip-gui` as deprecated alias (logs warning but does nothing)
- **Risk**: Users forget to add `--gui` when they need it → **Mitigation**: Clear help text and warning message when GUI is skipped

## Tradeoff

- **Option 1**: Breaking change - remove `--skip-gui`, make `--gui` required
  - Pros: Clean API, no confusion
  - Cons: Breaks existing scripts
- **Option 2**: Keep `--skip-gui` as deprecated no-op
  - Pros: Backward compatible
  - Cons: Slightly confusing API
- **Chosen**: Option 2 - Keep `--skip-gui` as deprecated no-op for backward compatibility

## Business Benefits/Impact/Metrics

**Success Metrics:**

| Metric | Current State (Benchmark) | Future State (Target) | Savings/Impacts |
| :---- | :---- | :---- | :---- |
| Default build time | ~10-15 minutes (with GUI) | ~3-5 minutes (app only) | 60-70% time savings |
| Developer iterations/hour | 4-6 | 10-15 | 2.5x productivity |

## Stakeholders / Owners

| Name | Team/Org | Role | Note |
| :---- | :---- | :---- | :---- |
| kasiro | Jarvis Core | User/Requester | Primary stakeholder |
| Pickle Rick | AI Engineering | Implementer | God Mode implementation |
