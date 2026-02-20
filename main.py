from version_fetcher import VersionFetcher
from installer import PythonInstaller
import sys
import traceback

class CommandLineInstaller:
    def __init__(self):
        # 初始化各个模块
        try:
            self.version_fetcher = VersionFetcher()
            self.installer = PythonInstaller()
            print("Python版本选择安装器初始化成功")
        except Exception as e:
            print(f"程序初始化失败: {str(e)}")
            traceback.print_exc()
            sys.exit(1)
    
    def __init__(self):
        # 初始化各个模块
        try:
            self.version_fetcher = VersionFetcher()
            self.installer = PythonInstaller()
            # 初始化镜像源设置
            self.mirror_sources = {
                "1": "https://pypi.tuna.tsinghua.edu.cn/simple",  # 清华源
                "2": "https://pypi.mirrors.ustc.edu.cn/simple",  # 中科大源
                "3": "https://mirrors.aliyun.com/pypi/simple",  # 阿里云源
                "4": "https://pypi.douban.com/simple",  # 豆瓣源
                "5": "https://pypi.org/simple"  # 官方源
            }
            self.custom_mirrors = {}
            self.default_mirror = "1"  # 默认使用清华源
            print("Python版本选择安装器初始化成功")
        except Exception as e:
            print(f"程序初始化失败: {str(e)}")
            traceback.print_exc()
            sys.exit(1)
    
    def run(self):
        """运行命令行界面"""
        try:
            while True:
                print("\npy manager")
                print("1. 获取可用Python版本")
                print("2. 安装指定版本")
                print("3. 检查已安装的Python版本")
                print("4. 管理Python依赖库")
                print("5. 设置")
                print("6. 退出")
                
                choice = input("请输入选择 (1-6): ")
                
                if choice == "1":
                    self.fetch_versions()
                elif choice == "2":
                    self.install_version()
                elif choice == "3":
                    self.check_installed_versions()
                elif choice == "4":
                    self.manage_dependencies()
                elif choice == "5":
                    self.settings()
                elif choice == "6":
                    print("感谢使用，再见！")
                    break
                else:
                    print("无效选择，请重新输入")
                    
        except Exception as e:
            print(f"程序运行时出错: {e}")
            traceback.print_exc()
    
    def fetch_versions(self):
        """获取并显示可用版本"""
        print("\n正在获取可用Python版本...")
        versions = self.version_fetcher.get_available_versions()
        
        if not versions:
            print("无法获取Python版本信息，请检查网络连接")
            return
        
        print(f"\n成功获取到 {len(versions)} 个版本:")
        print("-" * 80)
        
        for i, version_info in enumerate(versions, 1):
            print(f"{i}. {version_info['type']}: Python {version_info['version']} ({version_info['date']})")
        
        print("-" * 80)
    
    def install_version(self):
        """安装指定版本"""
        # 先获取版本列表
        print("\n正在获取可用Python版本...")
        versions = self.version_fetcher.get_available_versions()
        
        if not versions:
            print("无法获取Python版本信息，请检查网络连接")
            return
        
        # 显示版本列表
        print(f"\n可用版本列表:")
        print("-" * 80)
        
        for i, version_info in enumerate(versions, 1):
            print(f"{i}. {version_info['type']}: Python {version_info['version']} ({version_info['date']})")
        
        print("-" * 80)
        
        # 获取用户选择
        try:
            choice = int(input("请输入要安装的版本编号: "))
            if choice < 1 or choice > len(versions):
                print("无效的版本编号")
                return
            
            selected_version = versions[choice - 1]
            version = selected_version['version']
            
            print(f"\n您选择了: Python {version}")
            confirm = input("确定要安装吗？ (y/n): ")
            
            if confirm.lower() != "y":
                print("安装已取消")
                return
            
            # 获取下载链接
            print(f"\n正在获取 Python {version} 的下载链接...")
            download_url = self.version_fetcher.get_download_url(version)
            
            if not download_url:
                print(f"无法获取 Python {version} 的下载链接")
                return
            
            # 开始安装
            print(f"\n开始安装 Python {version}...")
            print(f"下载链接: {download_url}")
            
            success = self.installer.install(version, download_url)
            
            if success:
                print(f"\n🎉 Python {version} 安装成功！")
                # 验证安装
                self.installer.verify_installation(version)
            else:
                print(f"\n❌ Python {version} 安装失败")
                
        except ValueError:
            print("请输入有效的数字")
        except Exception as e:
            print(f"安装过程中出错: {e}")
            traceback.print_exc()
    
    def check_installed_versions(self):
        """检查已安装的Python版本"""
        print("\n检查已安装的Python版本...")
        
        import subprocess
        import os
        
        # 检查当前Python版本
        print("\n当前Python版本:")
        try:
            result = subprocess.run(
                ["python", "--version"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                print(f"  {result.stdout.strip()}")
            else:
                print("  无法获取当前Python版本")
        except Exception as e:
            print(f"  获取当前Python版本时出错: {e}")
        
        # 检查Python可执行文件路径
        print("\nPython可执行文件路径:")
        try:
            result = subprocess.run(
                ["where", "python"],  # Windows系统使用where命令
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                paths = result.stdout.strip().split('\n')
                for path in paths:
                    print(f"  {path}")
            else:
                # 尝试使用which命令（适用于其他系统）
                try:
                    result = subprocess.run(
                        ["which", "python"],
                        capture_output=True,
                        text=True,
                        timeout=10
                    )
                    if result.returncode == 0:
                        print(f"  {result.stdout.strip()}")
                    else:
                        print("  无法找到Python可执行文件")
                except Exception:
                    print("  无法找到Python可执行文件")
        except Exception as e:
            print(f"  获取Python路径时出错: {e}")
        
        # 检查环境变量中的Python路径
        print("\n环境变量中的Python相关路径:")
        path_env = os.environ.get("PATH", "")
        python_paths = [p for p in path_env.split(';') if 'python' in p.lower()]
        if python_paths:
            for p in python_paths:
                print(f"  {p}")
        else:
            print("  环境变量中未找到Python相关路径")
        
        # 检查已安装的Python版本（通过注册表，仅Windows）
        if os.name == "nt":  # Windows系统
            print("\n从Windows注册表检查Python版本:")
            try:
                import winreg
                
                # 检查64位注册表
                try:
                    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\Python\PythonCore")
                    print("  已安装的Python版本:")
                    i = 0
                    while True:
                        try:
                            version = winreg.EnumKey(key, i)
                            print(f"    - Python {version}")
                            # 尝试获取安装路径
                            try:
                                install_key = winreg.OpenKey(key, f"{version}\InstallPath")
                                install_path = winreg.QueryValue(install_key, "")
                                print(f"      安装路径: {install_path}")
                                install_key.Close()
                            except Exception:
                                pass
                            i += 1
                        except WindowsError:
                            break
                    key.Close()
                except Exception as e:
                    print(f"  检查注册表时出错: {e}")
            except ImportError:
                print("  无法访问Windows注册表")
        
        print("\n检查完成！")
    
    def manage_dependencies(self):
        """管理Python依赖库"""
        print("\nPython依赖库管理")
        
        import subprocess
        import os
        
        while True:
            print("\n依赖库管理菜单")
            print("1. 显示已安装的依赖库")
            print("2. 搜索依赖库")
            print("3. 安装依赖库")
            print("4. 升级依赖库")
            print("5. 卸载依赖库")
            print("6. 从wheel文件安装依赖库")
            print("7. 安装/修复pip")
            print("8. 返回主菜单")
            
            choice = input("请输入选择 (1-8): ")
            
            if choice == "1":
                self.show_installed_packages()
            elif choice == "2":
                self.search_package()
            elif choice == "3":
                self.install_package()
            elif choice == "4":
                self.upgrade_package()
            elif choice == "5":
                self.uninstall_package()
            elif choice == "6":
                self.install_from_wheel()
            elif choice == "7":
                self.install_pip()
            elif choice == "8":
                break
            else:
                print("无效选择，请重新输入")
    
    def show_installed_packages(self):
        """显示已安装的依赖库"""
        print("\n显示已安装的依赖库...")
        
        import subprocess
        import sys
        
        try:
            # 首先检查Python可执行文件路径
            print("\n正在检查Python环境...")
            python_path = sys.executable
            print(f"当前Python可执行文件: {python_path}")
            
            # 尝试使用当前Python可执行文件运行pip list
            print("\n正在获取已安装的依赖库...")
            result = subprocess.run(
                [python_path, "-m", "pip", "list"],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                print("\n已安装的依赖库:")
                print(result.stdout)
            else:
                print(f"获取依赖库列表失败: {result.stderr}")
                # 检测pip错误
                if "No module named pip" in result.stderr:
                    print("\n⚠️  检测到pip未安装")
                    print("建议运行: python -m ensurepip --upgrade 来安装pip")
                elif "ImportError" in result.stderr or "ModuleNotFoundError" in result.stderr:
                    print("\n⚠️  检测到pip损坏")
                    self.suggest_fix_pip()
        except subprocess.TimeoutExpired:
            print("\n❌ 获取依赖库列表超时，请检查网络连接或尝试重新运行")
        except FileNotFoundError:
            print("\n❌ 找不到Python可执行文件，请检查Python安装")
        except Exception as e:
            print(f"\n❌ 显示依赖库时出错: {e}")
            # 尝试使用where命令查找Python
            try:
                where_result = subprocess.run(
                    ["where", "python"],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                if where_result.returncode == 0:
                    print("\n系统中找到的Python可执行文件:")
                    print(where_result.stdout)
            except Exception:
                pass
    
    def search_package(self):
        """搜索依赖库"""
        package_name = input("\n请输入要搜索的依赖库名称: ")
        
        import subprocess
        import sys
        
        try:
            python_path = sys.executable
            print(f"\n搜索依赖库: {package_name}...")
            
            # 尝试使用pip search命令
            print("\n使用pip search命令搜索...")
            result = subprocess.run(
                [python_path, "-m", "pip", "search", package_name],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                print("\n搜索结果:")
                print(result.stdout)
                # 尝试获取版本信息
                self.get_package_versions(package_name)
            else:
                # pip search命令失败，尝试使用pip index versions命令获取版本信息
                print("\npip search命令不可用，尝试获取版本信息...")
                self.get_package_versions(package_name)
                
                # 提供备用方案
                print("\n备用搜索方式:")
                print(f"请访问 https://pypi.org/search/?q={package_name} 查看详细搜索结果")
                print("\n或者尝试直接安装:")
                confirm = input("是否直接安装此依赖库？ (y/n): ")
                if confirm.lower() == "y":
                    self.install_package(package_name)
        except Exception as e:
            print(f"搜索依赖库时出错: {e}")
            # 尝试获取版本信息作为备用
            self.get_package_versions(package_name)
    
    def get_package_versions(self, package_name):
        """获取依赖库的版本信息"""
        import subprocess
        import sys
        
        try:
            python_path = sys.executable
            print(f"\n获取 {package_name} 的版本信息...")
            
            # 尝试使用pip index versions命令
            result = subprocess.run(
                [python_path, "-m", "pip", "index", "versions", package_name],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                print("\n版本信息:")
                print(result.stdout)
            else:
                # 尝试使用pip show命令获取已安装版本
                print("\n尝试检查已安装版本...")
                show_result = subprocess.run(
                    [python_path, "-m", "pip", "show", package_name],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                if show_result.returncode == 0:
                    print("\n已安装版本信息:")
                    print(show_result.stdout)
                else:
                    print(f"\n无法获取 {package_name} 的版本信息")
                    print("该依赖库可能未安装，或者pip版本不支持此命令")
        except Exception as e:
            print(f"获取版本信息时出错: {e}")
    
    def install_package(self, package_name=None):
        """安装依赖库"""
        if not package_name:
            package_name = input("\n请输入要安装的依赖库名称: ")
        
        # 显示版本信息
        self.get_package_versions(package_name)
        
        version = input("请输入版本号（可选，按回车安装最新版本）: ")
        if version:
            package_spec = f"{package_name}=={version}"
        else:
            package_spec = package_name
        
        import subprocess
        import sys
        
        try:
            python_path = sys.executable
            print(f"\n安装依赖库: {package_spec}...")
            mirror_url = self.get_default_mirror_url()
            print(f"使用镜像源: {self.get_mirror_name(self.default_mirror)} - {mirror_url}")
            
            cmd = [python_path, "-m", "pip", "install", package_spec]
            if mirror_url:
                cmd.extend(["-i", mirror_url])
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                print("\n安装成功！")
                print(result.stdout)
                # 再次显示版本信息，确认安装结果
                print("\n安装后版本信息:")
                self.get_package_versions(package_name)
            else:
                print(f"\n安装失败: {result.stderr}")
                # 检测pip错误
                self.detect_pip_error(result.stderr)
        except Exception as e:
            print(f"安装依赖库时出错: {e}")
            # 检测异常中的pip错误
            if "pip" in str(e).lower():
                self.suggest_fix_pip()
    
    def upgrade_package(self):
        """升级依赖库"""
        package_name = input("\n请输入要升级的依赖库名称: ")
        
        import subprocess
        
        try:
            print(f"\n升级依赖库: {package_name}...")
            mirror_url = self.get_default_mirror_url()
            print(f"使用镜像源: {self.get_mirror_name(self.default_mirror)} - {mirror_url}")
            
            cmd = ["python", "-m", "pip", "install", "--upgrade", package_name]
            if mirror_url:
                cmd.extend(["-i", mirror_url])
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                print("\n升级成功！")
                print(result.stdout)
            else:
                print(f"\n升级失败: {result.stderr}")
                # 检测pip错误
                self.detect_pip_error(result.stderr)
        except Exception as e:
            print(f"升级依赖库时出错: {e}")
            # 检测异常中的pip错误
            if "pip" in str(e).lower():
                self.suggest_fix_pip()
    
    def detect_pip_error(self, error_message):
        """检测pip错误并建议修复"""
        # 常见的pip错误关键词
        pip_error_keywords = [
            "importerror", "modulenotfounderror", "pip._vendor",
            "requirementinformation", "resolvelib", "structs"
        ]
        
        error_lower = error_message.lower()
        for keyword in pip_error_keywords:
            if keyword in error_lower:
                self.suggest_fix_pip()
                break
    
    def suggest_fix_pip(self):
        """建议修复pip"""
        print("\n⚠️  检测到pip相关错误，建议修复pip后重试")
        print("\n修复pip的方法:")
        print("1. 使用ensurepip模块修复: python -m ensurepip --upgrade")
        print("2. 使用get-pip.py脚本重新安装: 访问 https://bootstrap.pypa.io/get-pip.py 下载并运行")
        print("3. 重新安装Python（最彻底的解决方案）")
        
        # 询问用户是否尝试使用ensurepip修复
        choice = input("\n是否尝试使用ensurepip修复pip？ (y/n): ")
        if choice.lower() == "y":
            self.fix_pip_with_ensurepip()
    
    def fix_pip_with_ensurepip(self):
        """使用ensurepip修复pip"""
        import subprocess
        import sys
        
        try:
            python_path = sys.executable
            print(f"\n正在使用ensurepip修复pip...")
            print(f"使用Python可执行文件: {python_path}")
            
            result = subprocess.run(
                [python_path, "-m", "ensurepip", "--upgrade"],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                print("\n✅ pip修复成功！")
                print(result.stdout)
                # 验证修复结果
                verify_result = subprocess.run(
                    [python_path, "-m", "pip", "--version"],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                if verify_result.returncode == 0:
                    print("\npip版本验证:")
                    print(verify_result.stdout)
            else:
                print(f"\n❌ pip修复失败: {result.stderr}")
                print("\n建议尝试其他修复方法或重新安装Python")
        except Exception as e:
            print(f"\n❌ 修复pip时出错: {e}")
            print("\n建议尝试其他修复方法或重新安装Python")
    
    def install_pip(self):
        """安装/修复pip"""
        print("\n安装/修复pip")
        
        while True:
            print("\n安装/修复pip菜单")
            print("1. 使用ensurepip模块安装/修复pip")
            print("2. 使用get-pip.py脚本安装pip")
            print("3. 检查pip状态")
            print("4. 返回依赖库管理菜单")
            
            choice = input("请输入选择 (1-4): ")
            
            if choice == "1":
                self.fix_pip_with_ensurepip()
            elif choice == "2":
                self.install_pip_with_get_pip()
            elif choice == "3":
                self.check_pip_status()
            elif choice == "4":
                break
            else:
                print("无效选择，请重新输入")
    
    def install_pip_with_get_pip(self):
        """使用get-pip.py脚本安装pip"""
        import subprocess
        import os
        import sys
        import urllib.request
        
        try:
            python_path = sys.executable
            print("\n正在使用get-pip.py脚本安装pip...")
            print(f"使用Python可执行文件: {python_path}")
            
            # 下载get-pip.py脚本
            get_pip_url = "https://bootstrap.pypa.io/get-pip.py"
            get_pip_path = os.path.join(os.getcwd(), "get-pip.py")
            
            print(f"\n正在下载get-pip.py脚本...")
            print(f"下载地址: {get_pip_url}")
            
            # 使用urllib下载脚本
            urllib.request.urlretrieve(get_pip_url, get_pip_path)
            print(f"\n脚本下载完成: {get_pip_path}")
            
            # 运行get-pip.py脚本
            print("\n正在运行get-pip.py脚本安装pip...")
            result = subprocess.run(
                [python_path, get_pip_path],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            # 清理临时文件
            if os.path.exists(get_pip_path):
                os.remove(get_pip_path)
                print(f"\n已清理临时文件: {get_pip_path}")
            
            if result.returncode == 0:
                print("\n✅ pip安装成功！")
                # 验证安装结果
                verify_result = subprocess.run(
                    [python_path, "-m", "pip", "--version"],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                if verify_result.returncode == 0:
                    print("\npip版本验证:")
                    print(verify_result.stdout)
            else:
                print(f"\n❌ pip安装失败: {result.stderr}")
                print("\n建议尝试其他安装方法或重新安装Python")
        except urllib.error.URLError as e:
            print(f"\n❌ 下载get-pip.py脚本失败: {e}")
            print("\n请检查网络连接后重试")
        except Exception as e:
            print(f"\n❌ 安装pip时出错: {e}")
            print("\n建议尝试其他安装方法或重新安装Python")
        finally:
            # 确保临时文件被清理
            get_pip_path = os.path.join(os.getcwd(), "get-pip.py")
            if os.path.exists(get_pip_path):
                try:
                    os.remove(get_pip_path)
                except:
                    pass
    
    def check_pip_status(self):
        """检查pip状态"""
        import subprocess
        import sys
        
        try:
            python_path = sys.executable
            print("\n正在检查pip状态...")
            print(f"使用Python可执行文件: {python_path}")
            
            # 检查pip是否安装
            result = subprocess.run(
                [python_path, "-m", "pip", "--version"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                print("\n✅ pip已安装")
                print(result.stdout)
            else:
                print("\n❌ pip未安装或损坏")
                print(f"错误信息: {result.stderr}")
                print("\n建议使用安装/修复pip功能来解决此问题")
        except Exception as e:
            print(f"\n❌ 检查pip状态时出错: {e}")
            print("\npip可能未安装或Python环境存在问题")
    
    def uninstall_package(self):
        """卸载依赖库"""
        package_name = input("\n请输入要卸载的依赖库名称: ")
        
        import subprocess
        
        try:
            print(f"\n卸载依赖库: {package_name}...")
            result = subprocess.run(
                ["python", "-m", "pip", "uninstall", "-y", package_name],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                print("\n卸载成功！")
                print(result.stdout)
            else:
                print(f"\n卸载失败: {result.stderr}")
        except Exception as e:
            print(f"卸载依赖库时出错: {e}")
    
    def install_from_wheel(self):
        """从wheel文件安装依赖库"""
        wheel_path = input("\n请输入wheel文件的路径: ")
        
        import subprocess
        import os
        
        if not os.path.exists(wheel_path):
            print(f"\n错误: 文件 {wheel_path} 不存在！")
            return
        
        try:
            print(f"\n从wheel文件安装: {wheel_path}...")
            result = subprocess.run(
                ["python", "-m", "pip", "install", wheel_path],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                print("\n安装成功！")
                print(result.stdout)
            else:
                print(f"\n安装失败: {result.stderr}")
        except Exception as e:
            print(f"安装依赖库时出错: {e}")
    
    def settings(self):
        """设置菜单"""
        print("\n设置")
        
        while True:
            print("\n设置菜单")
            print("1. 管理镜像源")
            print("2. 返回主菜单")
            
            choice = input("请输入选择 (1-2): ")
            
            if choice == "1":
                self.manage_mirrors()
            elif choice == "2":
                break
            else:
                print("无效选择，请重新输入")
    
    def manage_mirrors(self):
        """管理镜像源"""
        print("\n镜像源管理")
        
        while True:
            print("\n镜像源管理菜单")
            print("1. 显示当前镜像源")
            print("2. 选择内置镜像源")
            print("3. 添加自定义镜像源")
            print("4. 删除自定义镜像源")
            print("5. 设置默认镜像源")
            print("6. 返回设置菜单")
            
            choice = input("请输入选择 (1-6): ")
            
            if choice == "1":
                self.show_current_mirror()
            elif choice == "2":
                self.select_builtin_mirror()
            elif choice == "3":
                self.add_custom_mirror()
            elif choice == "4":
                self.remove_custom_mirror()
            elif choice == "5":
                self.set_default_mirror()
            elif choice == "6":
                break
            else:
                print("无效选择，请重新输入")
    
    def show_current_mirror(self):
        """显示当前镜像源"""
        print("\n当前镜像源设置:")
        print(f"默认镜像源: {self.get_mirror_name(self.default_mirror)}")
        print(f"镜像源URL: {self.get_mirror_url(self.default_mirror)}")
        
        print("\n内置镜像源:")
        for key, url in self.mirror_sources.items():
            print(f"{key}. {self.get_mirror_name(key)} - {url}")
        
        if self.custom_mirrors:
            print("\n自定义镜像源:")
            for key, (name, url) in self.custom_mirrors.items():
                print(f"{key}. {name} - {url}")
    
    def select_builtin_mirror(self):
        """选择内置镜像源"""
        print("\n选择内置镜像源:")
        for key, url in self.mirror_sources.items():
            print(f"{key}. {self.get_mirror_name(key)} - {url}")
        
        choice = input("请输入选择的镜像源编号: ")
        if choice in self.mirror_sources:
            self.default_mirror = choice
            print(f"\n已设置默认镜像源为: {self.get_mirror_name(choice)}")
        else:
            print("\n无效的选择，请重新输入")
    
    def add_custom_mirror(self):
        """添加自定义镜像源"""
        name = input("\n请输入自定义镜像源名称: ")
        url = input("请输入自定义镜像源URL: ")
        
        # 生成自定义镜像源编号
        custom_keys = [int(k) for k in self.custom_mirrors.keys() if k.isdigit()]
        if custom_keys:
            next_key = str(max(custom_keys) + 1)
        else:
            next_key = str(len(self.mirror_sources) + 1)
        
        self.custom_mirrors[next_key] = (name, url)
        print(f"\n已添加自定义镜像源: {name} - {url}")
    
    def remove_custom_mirror(self):
        """删除自定义镜像源"""
        if not self.custom_mirrors:
            print("\n没有自定义镜像源可以删除")
            return
        
        print("\n自定义镜像源:")
        for key, (name, url) in self.custom_mirrors.items():
            print(f"{key}. {name} - {url}")
        
        choice = input("请输入要删除的镜像源编号: ")
        if choice in self.custom_mirrors:
            name, url = self.custom_mirrors[choice]
            del self.custom_mirrors[choice]
            print(f"\n已删除自定义镜像源: {name} - {url}")
        else:
            print("\n无效的选择，请重新输入")
    
    def set_default_mirror(self):
        """设置默认镜像源"""
        print("\n可用镜像源:")
        
        # 显示内置镜像源
        for key, url in self.mirror_sources.items():
            print(f"{key}. {self.get_mirror_name(key)} - {url}")
        
        # 显示自定义镜像源
        for key, (name, url) in self.custom_mirrors.items():
            print(f"{key}. {name} - {url}")
        
        choice = input("请输入要设置为默认的镜像源编号: ")
        if choice in self.mirror_sources or choice in self.custom_mirrors:
            self.default_mirror = choice
            print(f"\n已设置默认镜像源为: {self.get_mirror_name(choice)}")
        else:
            print("\n无效的选择，请重新输入")
    
    def get_mirror_name(self, key):
        """获取镜像源名称"""
        if key in self.mirror_sources:
            if key == "1":
                return "清华源"
            elif key == "2":
                return "中科大源"
            elif key == "3":
                return "阿里云源"
            elif key == "4":
                return "豆瓣源"
            elif key == "5":
                return "官方源"
        elif key in self.custom_mirrors:
            return self.custom_mirrors[key][0]
        return "未知镜像源"
    
    def get_mirror_url(self, key):
        """获取镜像源URL"""
        if key in self.mirror_sources:
            return self.mirror_sources[key]
        elif key in self.custom_mirrors:
            return self.custom_mirrors[key][1]
        return ""
    
    def get_default_mirror_url(self):
        """获取默认镜像源URL"""
        return self.get_mirror_url(self.default_mirror)

if __name__ == "__main__":
    # 设置异常处理
    def exception_hook(exctype, value, tb):
        # 打印异常信息
        traceback.print_exception(exctype, value, tb)
    
    # 替换默认的异常处理
    sys.excepthook = exception_hook
    
    # 启动应用
    app = CommandLineInstaller()
    app.run()

