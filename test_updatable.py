# 测试检查可更新依赖库功能
from main import CommandLineInstaller

# 创建实例
app = CommandLineInstaller()

# 调用检查可更新依赖库方法
app.check_updatable_packages()

print("\n测试完成！")