# 测试批量包管理的进度条功能
from main import CommandLineInstaller

# 创建实例
app = CommandLineInstaller()

print("=== 测试批量包管理进度条功能 ===")
print("\n1. 测试导出包列表进度条:")
try:
    app.export_packages()
except Exception as e:
    print(f"导出包列表时出错: {e}")

print("\n2. 测试检查可更新包进度条:")
try:
    app.check_updatable_packages()
except Exception as e:
    print(f"检查可更新包时出错: {e}")

print("\n测试完成！")