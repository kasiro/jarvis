#!/usr/bin/env python3
"""
Test script to verify all Python commands in the project
"""
import sys
import os
from pathlib import Path
import importlib.util
import inspect
import asyncio

# Add resources/commands to path
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
COMMANDS_DIR = PROJECT_ROOT / "resources" / "commands"

sys.path.insert(0, str(COMMANDS_DIR))

# Colors
RED = '\033[0;31m'
GREEN = '\033[0;32m'
YELLOW = '\033[1;33m'
BLUE = '\033[0;34m'
NC = '\033[0m'

def print_status(msg, color=NC):
    print(f"{color}>>> {msg}{NC}")

def print_success(msg):
    print_status(msg, GREEN)

def print_error(msg):
    print_status(msg, RED)

def print_warning(msg):
    print_status(msg, YELLOW)

def print_info(msg):
    print_status(msg, BLUE)

# Test results
passed = 0
failed = 0
skipped = 0

def test_module(module_path, module_name):
    """Test if module can be imported and has execute function"""
    global passed, failed, skipped
    
    try:
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        if spec is None or spec.loader is None:
            print_warning(f"⊘ {module_name}: Cannot load spec")
            skipped += 1
            return
        
        module = importlib.util.module_from_spec(spec)
        
        # Skip jarvis_server.py (it's a daemon)
        if module_name == "jarvis_server":
            print_info(f"⊘ {module_name}: Skipped (daemon)")
            skipped += 1
            return
        
        # Skip __init__.py files
        if module_name == "__init__":
            skipped += 1
            return
        
        # Skip test files
        if module_path.parent.name == "tests":
            print_info(f"⊘ {module_name}: Skipped (test file)")
            skipped += 1
            return
        
        # Skip jarvis_api modules (they are libraries)
        if "jarvis_api" in str(module_path):
            print_info(f"⊘ {module_name}: Skipped (library)")
            skipped += 1
            return
        
        # Skip jarvis/reboot.py (requires running jarvis-app)
        if "jarvis/reboot.py" in str(module_path):
            print_info(f"⊘ {module_name}: Skipped (requires running jarvis)")
            skipped += 1
            return
        
        # Try to execute
        spec.loader.exec_module(module)
        
        # Check for execute function
        if hasattr(module, "execute"):
            execute_func = getattr(module, "execute")
            
            # Check if it's async
            if inspect.iscoroutinefunction(execute_func):
                print_success(f"✓ {module_name}: Async execute() found")
            else:
                print_success(f"✓ {module_name}: Sync execute() found")
            
            passed += 1
        else:
            print_warning(f"⚠ {module_name}: No execute() function (might be library)")
            skipped += 1
            
    except ImportError as e:
        print_error(f"✗ {module_name}: Import error - {e}")
        failed += 1
    except Exception as e:
        print_error(f"✗ {module_name}: Error - {e}")
        failed += 1

def check_venv():
    """Check if virtual environment is activated"""
    venv = os.environ.get("VIRTUAL_ENV")
    in_venv = sys.prefix != sys.base_prefix
    
    print_info("🔍 Virtual Environment Check:")
    if in_venv and venv:
        print_success(f"  ✓ Venv activated: {venv}")
        return True
    elif in_venv:
        print_warning(f"  ⚠ Venv active but VIRTUAL_ENV not set: {sys.prefix}")
        return True
    else:
        print_error("  ✗ Venv NOT activated!")
        print_warning("  Hint: Run 'uv venv' and 'source .venv/bin/activate'")
        return False

def main():
    global passed, failed, skipped
    
    print_info("🥒 Pickle Rick's Python Commands Tester")
    print_info("=" * 50)
    print_info(f"Scanning: {COMMANDS_DIR}")
    print()
    
    # Check virtual environment
    venv_ok = check_venv()
    print()
    
    if not venv_ok:
        print_error("❌ Virtual environment not activated! Some imports may fail.")
        print()
    
    # Find all .py files
    py_files = list(COMMANDS_DIR.rglob("*.py"))
    
    print_info(f"Found {len(py_files)} Python files")
    print()
    
    # Test each file
    for py_file in sorted(py_files):
        module_name = py_file.stem
        test_module(py_file, module_name)
    
    # Summary
    print()
    print("=" * 50)
    print_info("Summary:")
    print_success(f"  ✓ Passed:  {passed}")
    print_error(f"  ✗ Failed:  {failed}")
    print_warning(f"  ⊘ Skipped: {skipped}")
    print()
    
    if failed > 0:
        print_error(f"❌ {failed} module(s) failed to load!")
        return 1
    else:
        print_success("✅ All modules loaded successfully!")
        return 0

if __name__ == "__main__":
    sys.exit(main())
