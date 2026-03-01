# Track Specification: Linux Port: Core Command System

## Overview

**Track ID**: `linux_port_core_20260223`  
**Type**: Feature Port  
**Status**: New  
**Priority**: P0 (Critical)  
**Created**: 2026-02-23  
**Target Platform**: CachyOS GNOME Wayland

## Problem Statement

The JARVIS project currently has 21 voice commands implemented using AutoHotkey (AHK) scripts for Windows. These commands are completely non-functional on Linux, making the voice assistant unusable for Linux users.

### Current State (Windows)
- 21 AHK scripts for command execution
- WinRT notifications
- PowerShell/cmd system calls
- Windows-specific API calls

### Target State (Linux)
- Bash scripts with xdotool/wmctrl
- notify-send for notifications
- Native Linux system calls
- Wayland-compatible window management

## Scope

### In Scope
1. **Command Migration** (P0 - Critical)
   - `open_browser` - Открыть браузер
   - `open_terminal` - Открыть терминал
   - `close_window` - Закрыть окно
   - `minimize_window` - Минимизировать окно
   - `maximize_window` - Развернуть окно
   - `switch_window` - Переключить окно
   - `copy_to_clipboard` - Копировать в буфер
   - `paste_from_clipboard` - Вставить из буфера
   - `open_file_manager` - Открыть проводник

2. **System Integration** (P1 - High)
   - Notification system (notify-rust)
   - Clipboard management (arboard)
   - Window management (xdotool, wmctrl)

3. **Configuration Updates**
   - Update `command.toml` configs for Linux paths
   - Update Lua API bindings
   - Update build scripts

### Out of Scope
- New command features
- Windows AHK script improvements
- Mobile platform support
- Other Linux distributions (only CachyOS GNOME)

## Technical Requirements

### Dependencies to Add
```toml
# Already in workspace Cargo.toml
arboard = "3"           # Cross-platform clipboard
notify-rust = "4"       # Linux notifications
```

### System Packages
```bash
sudo pacman -S xdotool wmctrl xclip libnotify
```

### File Changes
1. `resources/commands/*/command.toml` - Update script paths
2. `resources/commands/*/*.sh` - New bash scripts (replace `.ahk`)
3. `crates/jarvis-core/src/lua/api/system.rs` - Linux implementations
4. `crates/jarvis-gui/src/tauri_commands/` - Linux adaptations

## Success Criteria

### Functional Requirements
- [ ] All 9 P0 commands work on CachyOS GNOME Wayland
- [ ] Clipboard read/write works
- [ ] Notifications display correctly
- [ ] Window management works (open, close, minimize, maximize, switch)
- [ ] File manager opens Nautilus

### Non-Functional Requirements
- [ ] Command execution time <500ms
- [ ] No memory leaks
- [ ] No panics on errors (graceful degradation)
- [ ] Proper logging via `jarvis.log()`

### Testing Requirements
- [ ] Unit tests for command parser
- [ ] Integration tests for each command
- [ ] Manual testing on CachyOS GNOME Wayland
- [ ] Code coverage >85%

## Risks & Mitigations

| Risk | Impact | Mitigation |
| :---- | :---- | :---- |
| Wayland restricts global hotkeys | High | Use GNOME Extensions or dbus |
| xdotool doesn't work on Wayland | Medium | Use wmctrl as fallback |
| notify-rust incompatible with GNOME | Low | Use notify-send directly via std::process |
| AHK scripts use Windows-specific APIs | High | Complete rewrite in bash |

## Acceptance Criteria

1. **Build Success**
   - `cargo build --workspace` completes without errors on Linux
   - `cargo test --workspace` passes all tests

2. **Runtime Success**
   - `jarvis-app` starts without errors
   - `jarvis-gui` displays correctly in GNOME Wayland
   - Voice commands are recognized and executed

3. **Command Success**
   - All 9 P0 commands execute successfully
   - Error handling works (no panics)
   - Logs are written correctly

---

**Author**: Pickle Rick  
**Last Updated**: 2026-02-23
