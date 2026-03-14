# Tickets for: RustPotter + Wake Word Fix

## Ticket 1: Enable RustPotter Feature
**ID:** TKT-001
**Status:** Todo
**Priority:** Critical

**Task:** Add `rustpotter_wake` feature to `jarvis-app/Cargo.toml`

**Files to modify:**
- `crates/jarvis-app/Cargo.toml`

**Expected result:**
```toml
jarvis-core = { path = "../jarvis-core", features = ["intent", "rustpotter_wake"] }
```

---

## Ticket 2: Create Universal Launch Command
**ID:** TKT-002
**Status:** Todo
**Priority:** High

**Task:** Create new command `launch` that accepts app name as slot

**Files to create:**
- `resources/commands/launch/command.toml`
- `resources/commands/launch/launch_app.lua` or `launch_app.py`

**Expected behavior:**
- Phrases: "запусти [app]", "открой [app]", "включи [app]"
- Slot: `app_name` - извлекается из фразы
- Action: Launch application using `jarvis.environment.launch_app()`

**Supported apps (examples):**
- firefox
- calculator (gnome-calculator)
- console (kgx)
- zeditor (zed)
- steam

---

## Ticket 3: Add Wake Word Protocol Documentation
**ID:** TKT-003
**Status:** Todo
**Priority:** Medium

**Task:** Update documentation to explain wake word configuration

**Files to update:**
- `resources/commands/WAKE_WORD_PROTOCOL.md`
- Add section about RustPotter vs Vosk
