# Implementation Plan: Linux Port: Core Command System

## Track Information

**Track ID**: `linux_port_core_20260223`  
**Status**: New  
**Created**: 2026-02-23  
**Estimated Duration**: 3-5 дней

---

## Phase 1: Foundation & Setup

### Goal
Подготовка инфраструктуры для Linux команд.

- [x] Task 1.1: Analyze existing AHK scripts
    - [x] Read all 21 AHK files in `resources/commands/`
    - [x] Document Windows-specific API calls
    - [x] Identify Linux equivalents (xdotool, wmctrl, etc.)
    - [x] Create mapping table: AHK → Linux

- [x] Task 1.2: Setup Linux dependencies
    - [x] Add `arboard` to `crates/jarvis-app/Cargo.toml`
    - [x] Add `notify-rust` to `crates/jarvis-app/Cargo.toml`
    - [x] Update `crates/jarvis-core/Cargo.toml` with platform-specific deps
    - [x] Document system packages in README

- [x] Task 1.3: Create bash script templates
    - [x] Create `resources/commands/template.sh`
    - [x] Define standard error handling pattern
    - [x] Define logging pattern (`jarvis.log()`)
    - [x] Test template on CachyOS

- [x] Task: Conductor - User Manual Verification 'Phase 1: Foundation & Setup' (Protocol in workflow.md)

---

## Phase 2: Core Commands Implementation

### Goal
Портирование 9 критических команд (P0).

- [x] Task 2.1: Window Management Commands
    - [x] Task 2.1.1: `close_window.sh` - Закрыть активное окно
    - [x] Task 2.1.2: `minimize_window.sh` - Минимизировать окно
    - [x] Task 2.1.3: `maximize_window.sh` - Развернуть окно
    - [x] Task 2.1.4: `switch_window.sh` - Переключить окно

- [x] Task 2.2: Application Launch Commands
    - [x] Task 2.2.1: `open_browser.sh` - Открыть браузер
    - [x] Task 2.2.2: `open_terminal.sh` - Открыть терминал
    - [x] Task 2.2.3: `open_file_manager.sh` - Открыть проводник

- [x] Task 2.3: System Commands
    - [x] Task 2.3.1: `copy_to_clipboard.sh` - Копировать в буфер
    - [x] Task 2.3.2: `paste_from_clipboard.sh` - Вставить из буфера

- [x] Task: Conductor - User Manual Verification 'Phase 2: Core Commands Implementation' (Protocol in workflow.md)

---

## Phase 3: Integration & Testing

### Goal
Интеграция команд в ядро и тестирование.

- [x] Task 3.1: Update Lua API
    - [x] Modify `crates/jarvis-core/src/lua/api/system.rs`
    - [x] Add `jarvis.system.exec_linux()` function
    - [x] Update clipboard API
    - [x] Update notification API
    - [x] Add error handling

- [x] Task 3.2: Update Command Executor
    - [x] Modify `crates/jarvis-core/src/commands.rs`
    - [x] Add platform detection logic
    - [x] Update AHK execution to use bash on Linux
    - [x] Add fallback mechanisms

- [x] Task 3.3: Write Integration Tests
    - [x] Create test harness for commands
    - [x] Write tests for each P0 command
    - [x] Add mock system calls
    - [x] Achieve >85% coverage

- [x] Task 3.4: Manual Testing on CachyOS
    - [x] Test all 9 commands manually
    - [x] Verify Wayland compatibility
    - [x] Test error scenarios
    - [x] Document any issues

- [x] Task: Conductor - User Manual Verification 'Phase 3: Integration & Testing' (Protocol in workflow.md)

---

## Phase 4: Documentation & Cleanup

### Goal
Документирование и финальная подготовка.

- [x] Task 4.1: Update Documentation
    - [x] Update `README.md` with Linux commands
    - [x] Add troubleshooting guide
    - [x] Document system dependencies
    - [x] Update `ADD.md` / `FIX.md`

- [x] Task 4.2: Code Cleanup
    - [x] Run `cargo clippy --workspace`
    - [x] Run `cargo fmt --workspace`
    - [x] Remove unused Windows code
    - [x] Add doc comments

- [x] Task 4.3: Build Verification
    - [x] `cargo build --release --workspace`
    - [x] `cargo test --workspace`
    - [x] `./rebuild.sh --clean`
    - [x] Verify binary size

- [x] Task 4.4: Create Release Notes
    - [x] Document changes in CHANGELOG.md
    - [x] List all ported commands
    - [x] Note any breaking changes
    - [x] Add migration guide

- [x] Task: Conductor - User Manual Verification 'Phase 4: Documentation & Cleanup' (Protocol in workflow.md)

---

## Deliverables

1. **Code**
   - 9 bash scripts for P0 commands
   - Updated Lua API bindings
   - Updated command executor
   - Integration tests

2. **Documentation**
   - Updated README.md
   - Command documentation
   - Troubleshooting guide

3. **Testing**
   - Unit tests (>85% coverage)
   - Integration tests
   - Manual test results

---

## Success Metrics

| Metric | Target | Measurement |
| :---- | :---- | :---- |
| Commands Ported | 9/9 P0 | Count of working commands |
| Test Coverage | >85% | `cargo tarpaulin` report |
| Build Success | 100% | `cargo build` on Linux |
| Command Latency | <500ms | Manual timing |
| Panics | 0 | Error logs review |

---

**Author**: Pickle Rick  
**Last Updated**: 2026-02-23
