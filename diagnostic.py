#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PyPi Manager - Diagnostic Tool
检查文件和依赖项，然后尝试运行主程序
"""

import os
import sys

print("=" * 60)
print("PyPi Manager - Diagnostic Tool")
print("=" * 60)
print("Current directory:", os.getcwd())
print("Python path:", sys.executable)

# Check necessary files
files = ["main.py", "main_gui.py", "version_fetcher.py", "installer.py"]

print("\nChecking files:")
all_files_exist = True
for file in files:
    file_path = os.path.join(os.getcwd(), file)
    if os.path.exists(file_path):
        print("OK", file, "- exists")
        print("  Path:", file_path)
    else:
        print("ERR", file, "- missing")
        print("  Expected path:", file_path)
        all_files_exist = False

# Check Python version
print("\nChecking Python:")
try:
    print("Python version:", sys.version)
    print("Python path:", sys.executable)
    python_ok = True
except Exception as e:
    print("Python error:", e)
    python_ok = False

# Check dependencies
print("\nChecking dependencies:")
deps = ["requests", "wx"]
deps_ok = True

for dep in deps:
    try:
        module = __import__(dep)
        print("OK", dep, "- installed")
        if hasattr(module, "__version__"):
            print("  Version:", module.__version__)
    except ImportError as e:
        print("ERR", dep, "- not installed")
        print("  Error:", e)
        deps_ok = False
    except Exception as e:
        print("???", dep, "- error checking")
        print("  Error:", e)
        deps_ok = False

# Summary
print("\n" + "=" * 60)
print("Check result summary:")
print("=" * 60)

if all_files_exist:
    print("OK All necessary files exist")
else:
    print("ERR Some necessary files missing")

if python_ok:
    print("OK Python available")
else:
    print("ERR Python not available")

if deps_ok:
    print("OK All dependencies installed")
else:
    print("ERR Some dependencies missing")
    print("\nPlease run:")
    print("python -m pip install requests wxPython -i https://pypi.tuna.tsinghua.edu.cn/simple")

# Check if main module can be imported
print("\n" + "=" * 60)
print("Trying to import main module:")
print("=" * 60)

try:
    # Add current directory to Python path
    sys.path.insert(0, os.getcwd())
    
    import main
    print("OK main.py imported successfully")
except Exception as e:
    print("ERR main.py import failed:", e)

print("\n" + "=" * 60)
print("Diagnostic completed")
print("=" * 60)
