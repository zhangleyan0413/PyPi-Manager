# 测试进度条功能
from main import CommandLineInstaller

# 创建实例
app = CommandLineInstaller()

print("=== 测试进度条功能 ===")
print("\n1. 测试加载动画:")
app._print_spinner()
print("加载动画测试完成！")

print("\n2. 测试文件大小格式化:")
sizes = [1023, 1024, 1048576, 1073741824]
for size in sizes:
    print(f"{size} bytes = {app._format_size(size)}")
print("文件大小格式化测试完成！")

print("\n3. 测试检查可更新依赖库进度条:")
try:
    app.check_updatable_packages()
except Exception as e:
    print(f"检查可更新依赖库时出错: {e}")

print("\n测试完成！")