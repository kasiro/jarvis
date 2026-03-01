# Development Workflow

## Overview

This document defines the development workflow for the JARVIS project. All contributors must follow these guidelines to ensure code quality and consistency.

## Core Principles

1. **Test-Driven Development (TDD)**: Write tests before implementation
2. **Small Commits**: Each commit represents a logical unit of work
3. **Code Review**: All changes require review
4. **Continuous Integration**: Automated testing on every PR

## Test Coverage Requirements

### Minimum Coverage
- **Overall Project**: >80%
- **Core Modules** (`jarvis-core`): >85%
- **Command System**: >90%
- **Public APIs**: 100%

### Coverage Measurement
```bash
# Install cargo-tarpaulin
cargo install cargo-tarpaulin

# Run coverage
cargo tarpaulin --workspace --out Html --out Lcov

# View report
xdg-open tarpaulin-report.html
```

### Exclusions
The following are excluded from coverage requirements:
- Generated code
- Benchmark code
- Integration test utilities
- Platform-specific code (`#[cfg(target_os = "...")]`)

## Commit Frequency

### Strategy: Per Task
Each completed task results in one commit. This ensures:
- Clear git history
- Easy rollback
- Atomic changes

### Commit Message Format
```
type(scope): description

[optional body]

[optional footer]
```

#### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Code style (formatting, semicolons, etc.)
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Build/config changes

#### Examples
```
feat(stt): Add support for Ukrainian language model

- Download and cache Ukrainian Vosk model
- Add language selection in config
- Update documentation

Closes #42

---

fix(commands): Fix browser command on Wayland

- Replace xdotool with wmctrl for Wayland compatibility
- Add fallback for X11

Fixes #38

---

test(core): Add unit tests for command parser

- Test simple commands
- Test commands with slots
- Test error cases

Coverage: 95%
```

## Task Summary Storage

### Method: Git Notes + Commit Messages
Task summaries are stored in both:
1. **Git Notes**: Metadata attached to commits
2. **Commit Message Body**: Detailed description

### Example
```bash
# Commit with detailed message
git commit -m "feat(stt): Add Ukrainian language support

- Added vosk-model-uk-small model download
- Implemented language switching logic
- Updated config schema
- Added tests for language detection

Task: UKRAINIAN_STT_SUPPORT
Time: 4h
Coverage: 87%"

# Add git note
git notes add -m "Task completed by: Pickle Rick
Reviewed by: TBD
Tested on: CachyOS GNOME Wayland"
```

## Development Cycle

### 1. Plan Phase
```markdown
- [ ] Read track specification
- [ ] Understand requirements
- [ ] Identify dependencies
- [ ] Create implementation plan
```

### 2. Test Phase (TDD)
```markdown
- [ ] Write failing tests
- [ ] Verify tests fail (red)
- [ ] Add test coverage for edge cases
```

### 3. Implement Phase
```markdown
- [ ] Write minimal code to pass tests
- [ ] Refactor for clarity
- [ ] Ensure no warnings (`cargo clippy`)
- [ ] Format code (`cargo fmt`)
```

### 4. Verify Phase
```markdown
- [ ] Run all tests: `cargo test --workspace`
- [ ] Check coverage: `cargo tarpaulin`
- [ ] Build release: `cargo build --release`
- [ ] Manual testing on target platform
```

### 5. Review Phase
```markdown
- [ ] Self-review: `cargo review` (if available)
- [ ] Check diff: `git diff HEAD`
- [ ] Verify commit message
- [ ] Create PR (if applicable)
```

## Phase Completion Verification and Checkpointing Protocol

### Purpose
Ensure each development phase is complete before proceeding to the next.

### Protocol

#### After Each Phase
1. **Run Verification Checklist**
   ```bash
   # Check for compilation errors
   cargo check --workspace
   
   # Check for clippy warnings
   cargo clippy --workspace -- -D warnings
   
   # Run tests
   cargo test --workspace
   ```

2. **Create Checkpoint**
   ```bash
   # Tag the commit
   git tag -a "checkpoint/<phase-name>-$(date +%Y%m%d)" -m "<Phase> completed"
   
   # Or create a backup branch
   git branch "backup/<phase-name>-$(date +%Y%m%d)"
   ```

3. **Document Completion**
   - Update task status in track plan
   - Add summary to commit message
   - Note any technical debt created

#### Before Next Phase
1. **Verify Previous Phase**
   - All tests pass
   - Coverage meets requirements
   - No clippy warnings
   - Documentation updated

2. **Get Approval** (if in team)
   - Code review completed
   - PR merged (if applicable)

### Checkpoint Commands
```bash
# Create checkpoint before changes
git tag checkpoint/before-<change-name>

# Restore to checkpoint if needed
git checkout checkpoint/before-<change-name>

# List recent checkpoints
git tag -l "checkpoint/*" | tail -10
```

## Code Review Guidelines

### Reviewer Checklist
- [ ] Code follows style guides
- [ ] Tests are comprehensive
- [ ] Error handling is proper
- [ ] Documentation is updated
- [ ] No security issues introduced
- [ ] Performance impact considered

### Review Process
1. Author creates PR with clear description
2. Reviewer assigned (or self-review for small changes)
3. Reviewer provides feedback within 24h
4. Author addresses feedback
5. Reviewer approves
6. PR merged

## Continuous Integration

### GitHub Actions Workflow
```yaml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Install Rust
        uses: actions-rs/toolchain@v1
        with:
          toolchain: stable
      - name: Run tests
        run: cargo test --workspace
      - name: Run clippy
        run: cargo clippy --workspace -- -D warnings

  build:
    runs-on: ubuntu-latest
    needs: test
    steps:
      - uses: actions/checkout@v3
      - name: Build release
        run: cargo build --release --workspace
```

## Release Process

### Version Bump
```bash
# Update version in Cargo.toml files
# Follow semver: MAJOR.MINOR.PATCH

# Create release tag
git tag -a v0.1.0 -m "Release v0.1.0"
git push origin v0.1.0

# Build release artifacts
./rebuild.sh --clean --release
```

### Release Checklist
- [ ] All tests pass
- [ ] Coverage >80%
- [ ] CHANGELOG.md updated
- [ ] Documentation updated
- [ ] Release tag created
- [ ] Binaries built and tested

---

## Enforcement

This workflow is enforced by:
1. **CI/CD**: Automated checks on every PR
2. **Code Review**: Human verification
3. **Pre-commit Hooks**: Local validation

### Pre-commit Hook Example
```bash
#!/bin/bash
# .git/hooks/pre-commit

set -e

echo "Running pre-commit checks..."

# Format check
cargo fmt -- --check

# Clippy
cargo clippy --workspace -- -D warnings

# Tests
cargo test --workspace

echo "All checks passed!"
```

---

**Last Updated**: 2026-02-23  
**Maintained By**: Pickle Rick  
**Compliance**: Mandatory for all contributors
