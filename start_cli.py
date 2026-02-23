#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PyPi Manager - CLI Launcher
直接启动PyPi Manager的命令行版本
"""

import os
import sys
import subprocess

# 设置工作目录为脚本所在目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))

print("=" * 60)
print("PyPi Manager - CLI Launcher")
print("=" * 60)

# 检查Python版本
print("Checking Python version...")
try:
    result = subprocess.run([sys.executable, "--version"], capture_output=True, text=True)
    print(f"Python: {result.stdout.strip()}")
except Exception as e:
    print(f"Error checking Python version: {e}")

# 检查依赖库
print("\nChecking dependencies...")
dependencies = ["requests"]
for dep in dependencies:
    try:
        __import__(dep)
        print(f"{dep}: OK")
    except ImportError:
        print(f"{dep}: NOT FOUND")
        print(f"Installing {dep}...")
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", dep, "-i", "https://pypi.tuna.tsinghua.edu.cn/simple"],
                check=True
            )
            print(f"{dep}: INSTALLED")
        except Exception as e:
            print(f"Error installing {dep}: {e}")

# 启动命令行版本
print("\nStarting PyPi Manager CLI...")
try:
    subprocess.run([sys.executable, "main.py"])
except Exception as e:
    print(f"Error starting CLI: {e}")

print("\nProgram execution completed.")
input("Press Enter to exit...")
