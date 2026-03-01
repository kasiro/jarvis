# Calculator Intent Recognition Fix PRD

## HR Eng

| Calculator Intent Recognition Fix PRD |  | Fix intent classifier corruption causing wrong command matching |
| :---- | :---- | :---- |
| **Author**: Pickle Rick **Contributors**: kasiro **Intended audience**: Engineering, PM | **Status**: Draft **Created**: 2026-02-25 | **Self Link**: [Link] **Context**: Jarvis Core |

## Introduction

The Jarvis voice command system uses an intent classifier to match spoken phrases to commands. When a user says "запусти калькулятор" (launch calculator), the intent classifier should recognize this phrase and execute the calculator command. However, the intent classifier is currently returning the wrong command (`modes` instead of `calculator`).

## Problem Statement

**Current Process:** 
1. User says "запусти калькулятор" 
2. Intent classifier returns `cli_0` with 100% confidence
3. System executes `modes` command (opens Firefox with YouTube) instead of `gnome-calculator`

**Primary Users:** All Jarvis users trying to launch the calculator

**Pain Points:** 
- Voice commands don't work as expected
- Wrong applications are launched
- User experience is broken

### Root Cause Analysis

Investigation revealed:
1. The `calculator` command exists and is properly configured in `resources/commands/calculator/command.yaml`
2. The command loads successfully (appears in "Loaded 10 command pack(s)" list)
3. **BUT** the intent classifier training cache (`~/.config/com.priler.jarvis/intent_training.json`) contains **CORRUPTED DATA**:
   - Contains irrelevant intents like "data_merge", "data_split", "data_transform"
   - These are NOT Jarvis commands - they appear to be from a different project or bug
   - The training data does NOT include "запусти калькулятор" or any calculator phrases

4. The hash check (`commands_hash.txt`) passes, so the classifier doesn't retrain with correct data

## Objective & Scope

**Objective:** Fix intent classifier to correctly recognize calculator and other Jarvis commands

**Ideal Outcome:** User says "запусти калькулятор" → calculator launches

### In-scope or Goals
- Clear corrupted intent training cache
- Force intent classifier retraining with correct command data
- Verify calculator command works after fix
- Ensure all other commands still work

### Not-in-scope or Non-Goals
- Changing command.yaml structure
- Modifying intent classifier algorithm
- Adding new commands

## Product Requirements

### Critical User Journeys (CUJs)

1. **CUJ 1: Launch Calculator**
   - User says "джарвис, запусти калькулятор"
   - Jarvis recognizes intent as `calculator` command
   - `gnome-calculator` application launches
   - Success sound plays

2. **CUJ 2: Close Calculator**
   - User says "закрой калькулятор"
   - Jarvis recognizes intent as `calculator` close command
   - `gnome-calculator` process is killed
   - Success sound plays

### Functional Requirements

| Priority | Requirement | User Story |
| :---- | :---- | :---- |
| P0 | Clear corrupted training cache | As a user, I need the intent classifier to use correct training data |
| P0 | Retrain intent classifier | As a user, I need my voice commands to be recognized correctly |
| P1 | Verify all commands load | As a user, I need all my commands to work, not just calculator |
| P2 | Add cache validation | As a developer, I want to detect corrupted cache automatically |

## Assumptions

- The `calculator/command.yaml` file is correctly formatted
- The intent classifier code is correct
- The issue is solely in the corrupted training cache
- Deleting cache files will trigger proper retraining

## Risks & Mitigations

- **Risk**: Other commands might break after retraining
  - **Mitigation**: Test all 10 commands after fix
  
- **Risk**: Cache might get corrupted again
  - **Mitigation**: Add validation to detect invalid intents (future enhancement)

## Tradeoff

- **Option 1**: Manually delete cache files (chosen)
  - Pros: Quick, simple, no code changes
  - Cons: User must do manual step
  
- **Option 2**: Add automatic cache validation
  - Pros: Prevents future issues
  - Cons: Requires code changes, testing, time

**Decision**: Start with Option 1, consider Option 2 for future

## Business Benefits/Impact/Metrics

**Success Metrics:**

| Metric | Current State (Benchmark) | Future State (Target) | Savings/Impacts |
| :---- | :---- | :---- | :---- |
| Intent accuracy for calculator | 0% (wrong command) | 100% | User satisfaction |
| Time to launch calculator | N/A (doesn't work) | <2 seconds | UX improvement |
| All commands recognized | Unknown | 100% | Full functionality |

## Stakeholders / Owners

| Name | Team/Org | Role | Note |
| :---- | :---- | :---- | :---- |
| kasiro | User | Reporter | Identified the issue |
| Pickle Rick | AI | Engineer | Fixing the issue |
