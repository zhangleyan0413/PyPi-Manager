#!/usr/bin/env python3
# 测试脚本，用于检查各个模块是否能正常导入和初始化

print("开始测试模块导入...")

try:
    import sys
    print(f"✅ Python版本: {sys.version}")
except Exception as e:
    print(f"❌ 导入sys模块失败: {e}")

try:
    import requests
    print(f"✅ requests模块版本: {requests.__version__}")
except Exception as e:
    print(f"❌ 导入requests模块失败: {e}")

try:
    from version_fetcher import VersionFetcher
    print("✅ 导入VersionFetcher模块成功")
    fetcher = VersionFetcher()
    print("✅ 初始化VersionFetcher成功")
    versions = fetcher.get_available_versions()
    print(f"✅ 获取版本列表成功，共 {len(versions)} 个版本")
except Exception as e:
    print(f"❌ VersionFetcher模块测试失败: {e}")
    import traceback
    traceback.print_exc()

try:
    from installer import PythonInstaller
    print("✅ 导入PythonInstaller模块成功")
    installer = PythonInstaller()
    print("✅ 初始化PythonInstaller成功")
except Exception as e:
    print(f"❌ PythonInstaller模块测试失败: {e}")
    import traceback
    traceback.print_exc()

try:
    from main import CommandLineInstaller
    print("✅ 导入CommandLineInstaller模块成功")
except Exception as e:
    print(f"❌ CommandLineInstaller模块测试失败: {e}")
    import traceback
    traceback.print_exc()

print("\n测试完成！")
input("按Enter键退出...")
