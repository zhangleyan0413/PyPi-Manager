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
                print("\nPyPi Manager")
                print("1. 管理pip包")
                print("2. 检查并修复pip")
                print("3. 配置镜像源")
                print("4. 批量包管理")
                print("5. Python版本管理")
                print("6. 关于作者")
                print("7. 退出")
                
                choice = input("请输入选择 (1-7): ")
                
                if choice == "1":
                    self.manage_pip_packages()
                elif choice == "2":
                    self.check_and_fix_pip()
                elif choice == "3":
                    self.manage_mirrors()
                elif choice == "4":
                    self.batch_package_management()
                elif choice == "5":
                    self.manage_python_versions()
                elif choice == "6":
                    self.show_author_info()
                elif choice == "7":
                    print("\n退出程序...")
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
            print("8. 检查可更新的依赖库")
            print("9. 返回主菜单")
            
            choice = input("请输入选择 (1-9): ")
            
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
                self.check_updatable_packages()
            elif choice == "9":
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
        import time
        
        try:
            python_path = sys.executable
            print(f"\n安装依赖库: {package_spec}...")
            mirror_url = self.get_default_mirror_url()
            print(f"使用镜像源: {self.get_mirror_name(self.default_mirror)} - {mirror_url}")
            
            cmd = [python_path, "-m", "pip", "install", package_spec]
            if mirror_url:
                cmd.extend(["-i", mirror_url])
            
            # 显示安装进度
            print("\n安装过程中...")
            
            # 定义安装步骤
            install_steps = [
                "解析依赖关系",
                "下载依赖库",
                "安装依赖库",
                "验证安装结果"
            ]
            
            # 启动安装线程
            import threading
            result = None
            error = None
            
            def install_thread():
                nonlocal result, error
                try:
                    result = subprocess.run(
                        cmd,
                        capture_output=True,
                        text=True,
                        timeout=60
                    )
                except Exception as e:
                    error = e
            
            thread = threading.Thread(target=install_thread)
            thread.daemon = True
            thread.start()
            
            # 显示进度
            step = 0
            while thread.is_alive() and step < len(install_steps):
                print(f"[{install_steps[step]}] ", end="")
                self._print_spinner()
                time.sleep(0.5)
                step += 1
            
            # 等待线程结束
            thread.join()
            
            if error:
                raise error
            
            if result.returncode == 0:
                print("\n[验证安装结果] ✅")
                print("\n安装成功！")
                print(result.stdout)
                # 再次显示版本信息，确认安装结果
                print("\n安装后版本信息:")
                self.get_package_versions(package_name)
            else:
                print("\n[验证安装结果] ❌")
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
        import sys
        import time
        import threading
        
        try:
            python_path = sys.executable
            print(f"\n升级依赖库: {package_name}...")
            mirror_url = self.get_default_mirror_url()
            print(f"使用镜像源: {self.get_mirror_name(self.default_mirror)} - {mirror_url}")
            
            cmd = [python_path, "-m", "pip", "install", "--upgrade", package_name]
            if mirror_url:
                cmd.extend(["-i", mirror_url])
            
            # 显示升级进度
            print("\n升级过程中...")
            
            # 定义升级步骤
            upgrade_steps = [
                "检查当前版本",
                "下载最新版本",
                "安装最新版本",
                "验证升级结果"
            ]
            
            # 启动升级线程
            result = None
            error = None
            
            def upgrade_thread():
                nonlocal result, error
                try:
                    result = subprocess.run(
                        cmd,
                        capture_output=True,
                        text=True,
                        timeout=60
                    )
                except Exception as e:
                    error = e
            
            thread = threading.Thread(target=upgrade_thread)
            thread.daemon = True
            thread.start()
            
            # 显示进度
            step = 0
            while thread.is_alive() and step < len(upgrade_steps):
                print(f"[{upgrade_steps[step]}] ", end="")
                self._print_spinner()
                time.sleep(0.5)
                step += 1
            
            # 等待线程结束
            thread.join()
            
            if error:
                raise error
            
            if result.returncode == 0:
                print("\n[验证升级结果] ✅")
                print("\n升级成功！")
                print(result.stdout)
            else:
                print("\n[验证升级结果] ❌")
                print(f"\n升级失败: {result.stderr}")
                # 检测pip错误
                self.detect_pip_error(result.stderr)
        except Exception as e:
            print(f"升级依赖库时出错: {e}")
            # 检测异常中的pip错误
            if "pip" in str(e).lower():
                self.suggest_fix_pip()
    
    def check_updatable_packages(self):
        """检查可更新的依赖库"""
        import subprocess
        import sys
        import time
        import threading
        
        try:
            python_path = sys.executable
            print("\n检查可更新的依赖库...")
            print("这可能需要一些时间，请耐心等待...")
            
            # 定义检查步骤
            check_steps = [
                "收集已安装的依赖库",
                "检查每个依赖库的版本",
                "比对最新版本信息",
                "生成可更新列表"
            ]
            
            # 启动检查线程
            result = None
            error = None
            
            def check_thread():
                nonlocal result, error
                try:
                    # 运行pip list --outdated命令
                    result = subprocess.run(
                        [python_path, "-m", "pip", "list", "--outdated"],
                        capture_output=True,
                        text=True,
                        timeout=60
                    )
                except Exception as e:
                    error = e
            
            thread = threading.Thread(target=check_thread)
            thread.daemon = True
            thread.start()
            
            # 显示进度
            step = 0
            while thread.is_alive() and step < len(check_steps):
                print(f"[{check_steps[step]}] ", end="")
                self._print_spinner()
                time.sleep(0.5)
                step += 1
            
            # 等待线程结束
            thread.join()
            
            if error:
                raise error
            
            if result.returncode == 0:
                output = result.stdout
                if output.strip():
                    print("\n发现可更新的依赖库:")
                    print("=" * 80)
                    print(output)
                    print("=" * 80)
                    
                    # 提取可更新的包名列表
                    lines = output.strip().split('\n')[2:]  # 跳过表头
                    updatable_packages = []
                    for line in lines:
                        if line.strip():
                            parts = line.split()
                            if len(parts) >= 1:
                                updatable_packages.append(parts[0])
                    
                    # 询问用户是否更新
                    if updatable_packages:
                        print("\n更新选项:")
                        print("1. 更新所有可更新的依赖库")
                        print("2. 选择特定的依赖库更新")
                        print("3. 不更新，返回菜单")
                        
                        choice = input("\n请输入选择 (1-3): ")
                        
                        if choice == "1":
                            # 更新所有
                            self.update_all_packages(updatable_packages)
                        elif choice == "2":
                            # 选择更新
                            self.selective_update(updatable_packages)
                        elif choice == "3":
                            # 不更新
                            print("\n取消更新操作")
                        else:
                            print("\n无效选择，请重新输入")
                else:
                    print("\n所有依赖库均为最新版本，无需更新！")
            else:
                print(f"\n检查失败: {result.stderr}")
                # 检测pip错误
                self.detect_pip_error(result.stderr)
        except Exception as e:
            print(f"检查可更新依赖库时出错: {e}")
            # 检测异常中的pip错误
            if "pip" in str(e).lower():
                self.suggest_fix_pip()
    
    def update_all_packages(self, packages):
        """更新所有可更新的依赖库"""
        import subprocess
        import sys
        import time
        import threading
        
        python_path = sys.executable
        mirror_url = self.get_default_mirror_url()
        
        print(f"\n更新所有 {len(packages)} 个可更新的依赖库...")
        print(f"使用镜像源: {self.get_mirror_name(self.default_mirror)} - {mirror_url}")
        
        success_count = 0
        fail_count = 0
        
        for i, package in enumerate(packages, 1):
            try:
                print(f"\n[{i}/{len(packages)}] 正在更新: {package}...")
                
                cmd = [python_path, "-m", "pip", "install", "--upgrade", package]
                if mirror_url:
                    cmd.extend(["-i", mirror_url])
                
                # 显示更新进度
                print("更新过程中...")
                
                # 定义更新步骤
                update_steps = [
                    "检查当前版本",
                    "下载最新版本",
                    "安装最新版本",
                    "验证更新结果"
                ]
                
                # 启动更新线程
                result = None
                error = None
                
                def update_thread():
                    nonlocal result, error
                    try:
                        result = subprocess.run(
                            cmd,
                            capture_output=True,
                            text=True,
                            timeout=60
                        )
                    except Exception as e:
                        error = e
                
                thread = threading.Thread(target=update_thread)
                thread.daemon = True
                thread.start()
                
                # 显示进度
                step = 0
                while thread.is_alive() and step < len(update_steps):
                    print(f"[{update_steps[step]}] ", end="")
                    self._print_spinner()
                    time.sleep(0.3)
                    step += 1
                
                # 等待线程结束
                thread.join()
                
                if error:
                    raise error
                
                if result.returncode == 0:
                    print("\n[验证更新结果] ✅")
                    print(f"✅ {package} 更新成功！")
                    success_count += 1
                else:
                    print("\n[验证更新结果] ❌")
                    print(f"❌ {package} 更新失败: {result.stderr[:100]}...")
                    fail_count += 1
            except Exception as e:
                print(f"❌ {package} 更新时出错: {e}")
                fail_count += 1
        
        print(f"\n更新完成！")
        print(f"成功: {success_count}, 失败: {fail_count}")
    
    def selective_update(self, packages):
        """选择特定的依赖库更新"""
        print("\n选择要更新的依赖库（输入编号，多个编号用空格分隔）:")
        
        for i, package in enumerate(packages, 1):
            print(f"{i}. {package}")
        
        user_input = input("\n请输入选择: ")
        
        try:
            selected_indices = [int(idx) - 1 for idx in user_input.split() if idx.isdigit()]
            selected_packages = [packages[idx] for idx in selected_indices if 0 <= idx < len(packages)]
            
            if selected_packages:
                print(f"\n将更新以下 {len(selected_packages)} 个依赖库:")
                for pkg in selected_packages:
                    print(f"- {pkg}")
                
                confirm = input("\n确认更新吗？ (y/n): ")
                if confirm.lower() == "y":
                    self.update_all_packages(selected_packages)
                else:
                    print("\n取消更新操作")
            else:
                print("\n未选择任何依赖库")
        except Exception as e:
            print(f"\n选择依赖库时出错: {e}")
    
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
    
    def show_author_info(self):
        """显示作者信息"""
        print("\n关于作者")
        print("=======================================")
        print("项目名称: PyPi Manager")
        print("全称: Python Pip Manager")
        print("版本: 1.1.0")
        print("作者: Your Name")
        print("邮箱: your.email@example.com")
        print("GitHub: https://github.com/yourusername/pypi-manager")
        print("=======================================")
        print("PyPi Manager 是一个功能强大的pip管理工具")
        print("支持pip包管理、镜像源配置、批量操作和Python版本管理")
        print("=======================================")
        input("按回车键返回主菜单...")
    
    def manage_pip_packages(self):
        """管理pip包"""
        print("\npip包管理")
        
        import subprocess
        import os
        
        while True:
            print("\npip包管理菜单")
            print("1. 显示已安装的包")
            print("2. 搜索包")
            print("3. 安装包")
            print("4. 升级包")
            print("5. 卸载包")
            print("6. 从wheel文件安装包")
            print("7. 返回主菜单")
            
            choice = input("请输入选择 (1-7): ")
            
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
                break
            else:
                print("无效选择，请重新输入")
    
    def check_and_fix_pip(self):
        """检查并修复pip"""
        print("\n检查并修复pip")
        
        # 首先检查pip状态
        self.check_pip_status()
        
        print("\npip修复选项")
        print("1. 使用ensurepip修复pip")
        print("2. 使用get-pip.py脚本安装pip")
        print("3. 仅检查pip状态")
        print("4. 返回主菜单")
        
        choice = input("请输入选择 (1-4): ")
        
        if choice == "1":
            self.fix_pip_with_ensurepip()
        elif choice == "2":
            self.install_pip_with_get_pip()
        elif choice == "3":
            self.check_pip_status()
        elif choice == "4":
            pass
        else:
            print("无效选择，请重新输入")
    
    def manage_mirrors(self):
        """配置镜像源"""
        print("\n配置镜像源")
        
        while True:
            print("\n镜像源管理菜单")
            print("1. 显示当前镜像源")
            print("2. 选择内置镜像源")
            print("3. 添加自定义镜像源")
            print("4. 删除自定义镜像源")
            print("5. 设置默认镜像源")
            print("6. 返回主菜单")
            
            choice = input("请输入选择 (1-6): ")
            
            if choice == "1":
                self.show_current_mirror()
            elif choice == "2":
                self.select_builtin_mirror()
            elif choice == "3":
                self.add_custom_mirror()
            elif choice == "4":
                self.delete_custom_mirror()
            elif choice == "5":
                self.set_default_mirror()
            elif choice == "6":
                break
            else:
                print("无效选择，请重新输入")
    
    def batch_package_management(self):
        """批量包管理"""
        print("\n批量包管理")
        
        while True:
            print("\n批量包管理菜单")
            print("1. 检查可更新的包")
            print("2. 批量更新所有包")
            print("3. 批量卸载包")
            print("4. 导出已安装的包列表")
            print("5. 从文件安装包")
            print("6. 返回主菜单")
            
            choice = input("请输入选择 (1-6): ")
            
            if choice == "1":
                self.check_updatable_packages()
            elif choice == "2":
                self.batch_update_packages()
            elif choice == "3":
                self.batch_uninstall_packages()
            elif choice == "4":
                self.export_packages()
            elif choice == "5":
                self.install_from_requirements()
            elif choice == "6":
                break
            else:
                print("无效选择，请重新输入")
    
    def manage_python_versions(self):
        """Python版本管理"""
        print("\nPython版本管理")
        
        while True:
            print("\nPython版本管理菜单")
            print("1. 获取可用Python版本")
            print("2. 安装指定版本")
            print("3. 检查已安装的Python版本")
            print("4. 返回主菜单")
            
            choice = input("请输入选择 (1-4): ")
            
            if choice == "1":
                self.fetch_versions()
            elif choice == "2":
                self.install_version()
            elif choice == "3":
                self.check_installed_versions()
            elif choice == "4":
                break
            else:
                print("无效选择，请重新输入")
    
    def _format_size(self, size):
        """格式化文件大小"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /= 1024
        return f"{size:.2f} TB"
    
    def _print_spinner(self):
        """打印加载动画"""
        import sys
        import time
        
        spinner = ['|', '/', '-', '\\']
        for char in spinner:
            sys.stdout.write(f"{char}\r")
            sys.stdout.flush()
            time.sleep(0.1)
        sys.stdout.write(" " * 10 + "\r")
        sys.stdout.flush()
    
    def batch_update_packages(self):
        """批量更新所有包"""
        print("\n批量更新所有包")
        print("这可能需要一些时间，请耐心等待...")
        
        import subprocess
        import sys
        import time
        import threading
        
        try:
            python_path = sys.executable
            mirror_url = self.get_default_mirror_url()
            print(f"使用镜像源: {self.get_mirror_name(self.default_mirror)} - {mirror_url}")
            
            # 定义更新步骤
            update_steps = [
                "检查可更新的包",
                "下载最新版本",
                "安装更新",
                "验证更新结果"
            ]
            
            # 启动更新线程
            result = None
            error = None
            
            def update_thread():
                nonlocal result, error
                try:
                    cmd = [python_path, "-m", "pip", "list", "--outdated"]
                    outdated_result = subprocess.run(
                        cmd,
                        capture_output=True,
                        text=True,
                        timeout=60
                    )
                    
                    if outdated_result.returncode == 0:
                        # 处理输出格式
                        lines = outdated_result.stdout.strip().split('\n')
                        outdated_packages = []
                        
                        # 跳过表头
                        for line in lines[2:]:  # 跳过前两行表头
                            if line.strip():
                                parts = line.split()
                                if len(parts) >= 1:
                                    pkg_name = parts[0]
                                    outdated_packages.append(pkg_name)
                        
                        if outdated_packages:
                            print(f"\n发现 {len(outdated_packages)} 个可更新的包")
                            print("可更新的包:")
                            for pkg in outdated_packages:
                                print(f"- {pkg}")
                            
                            # 逐个更新
                            success_count = 0
                            fail_count = 0
                            
                            for i, pkg_name in enumerate(outdated_packages, 1):
                                print(f"\n[{i}/{len(outdated_packages)}] 正在更新: {pkg_name}")
                                
                                update_cmd = [python_path, "-m", "pip", "install", "--upgrade", pkg_name]
                                if mirror_url:
                                    update_cmd.extend(["-i", mirror_url])
                                
                                # 定义更新步骤
                                update_steps = [
                                    "解析依赖关系",
                                    "下载最新版本",
                                    "安装更新",
                                    "验证更新结果"
                                ]
                                
                                # 启动更新线程
                                update_result = None
                                update_error = None
                                
                                def update_thread():
                                    nonlocal update_result, update_error
                                    try:
                                        update_result = subprocess.run(
                                            update_cmd,
                                            capture_output=True,
                                            text=True,
                                            timeout=60
                                        )
                                    except Exception as e:
                                        update_error = e
                                
                                thread = threading.Thread(target=update_thread)
                                thread.daemon = True
                                thread.start()
                                
                                # 显示进度
                                step = 0
                                while thread.is_alive() and step < len(update_steps):
                                    print(f"[{update_steps[step]}] ", end="")
                                    self._print_spinner()
                                    time.sleep(0.3)
                                    step += 1
                                
                                # 等待线程结束
                                thread.join()
                                
                                if update_error:
                                    print(f"❌ {pkg_name} 更新时出错: {update_error}")
                                    fail_count += 1
                                elif update_result.returncode == 0:
                                    print("[验证更新结果] ✅")
                                    print(f"✅ {pkg_name} 更新成功")
                                    success_count += 1
                                else:
                                    print("[验证更新结果] ❌")
                                    print(f"❌ {pkg_name} 更新失败")
                                    fail_count += 1
                            
                            print(f"\n更新完成！成功: {success_count}, 失败: {fail_count}")
                        else:
                            print("\n所有包都是最新版本，无需更新")
                    else:
                        print(f"\n检查可更新包失败: {outdated_result.stderr}")
                except Exception as e:
                    error = e
            
            thread = threading.Thread(target=update_thread)
            thread.daemon = True
            thread.start()
            
            # 显示进度
            step = 0
            while thread.is_alive() and step < len(update_steps):
                print(f"[{update_steps[step]}] ", end="")
                self._print_spinner()
                time.sleep(0.5)
                step += 1
            
            # 等待线程结束
            thread.join()
            
            if error:
                raise error
        except Exception as e:
            print(f"批量更新包时出错: {e}")
    
    def batch_uninstall_packages(self):
        """批量卸载包"""
        print("\n批量卸载包")
        
        import subprocess
        import sys
        
        try:
            python_path = sys.executable
            
            # 获取已安装的包
            print("获取已安装的包列表...")
            result = subprocess.run(
                [python_path, "-m", "pip", "list", "--format=freeze"],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                packages = result.stdout.strip().split('\n')
                if packages and packages[0]:
                    print("\n已安装的包:")
                    for i, pkg in enumerate(packages, 1):
                        if pkg:
                            pkg_name = pkg.split('==')[0]
                            print(f"{i}. {pkg_name}")
                    
                    # 让用户选择要卸载的包
                    selection = input("\n请输入要卸载的包的编号（多个编号用空格分隔）: ")
                    selected_indices = [int(idx) - 1 for idx in selection.split() if idx.isdigit()]
                    
                    if selected_indices:
                        packages_to_uninstall = [packages[idx].split('==')[0] for idx in selected_indices if 0 <= idx < len(packages)]
                        
                        print(f"\n将卸载以下 {len(packages_to_uninstall)} 个包:")
                        for pkg in packages_to_uninstall:
                            print(f"- {pkg}")
                        
                        confirm = input("\n确认卸载吗？ (y/n): ")
                        if confirm.lower() == "y":
                            import threading
                            import time
                            
                            for i, pkg in enumerate(packages_to_uninstall, 1):
                                print(f"\n[{i}/{len(packages_to_uninstall)}] 正在卸载: {pkg}")
                                
                                # 定义卸载步骤
                                uninstall_steps = [
                                    "准备卸载",
                                    "移除文件",
                                    "清理配置",
                                    "验证卸载结果"
                                ]
                                
                                # 启动卸载线程
                                uninstall_result = None
                                uninstall_error = None
                                
                                def uninstall_thread():
                                    nonlocal uninstall_result, uninstall_error
                                    try:
                                        uninstall_result = subprocess.run(
                                            [python_path, "-m", "pip", "uninstall", "-y", pkg],
                                            capture_output=True,
                                            text=True,
                                            timeout=30
                                        )
                                    except Exception as e:
                                        uninstall_error = e
                                
                                thread = threading.Thread(target=uninstall_thread)
                                thread.daemon = True
                                thread.start()
                                
                                # 显示进度
                                step = 0
                                while thread.is_alive() and step < len(uninstall_steps):
                                    print(f"[{uninstall_steps[step]}] ", end="")
                                    self._print_spinner()
                                    time.sleep(0.3)
                                    step += 1
                                
                                # 等待线程结束
                                thread.join()
                                
                                if uninstall_error:
                                    print(f"❌ {pkg} 卸载时出错: {uninstall_error}")
                                elif uninstall_result.returncode == 0:
                                    print("[验证卸载结果] ✅")
                                    print(f"✅ {pkg} 卸载成功")
                                else:
                                    print("[验证卸载结果] ❌")
                                    print(f"❌ {pkg} 卸载失败")
                    else:
                        print("\n未选择任何包")
                else:
                    print("\n未安装任何包")
            else:
                print(f"\n获取包列表失败: {result.stderr}")
        except Exception as e:
            print(f"批量卸载包时出错: {e}")
    
    def export_packages(self):
        """导出已安装的包列表"""
        print("\n导出已安装的包列表")
        
        import subprocess
        import sys
        import os
        
        try:
            python_path = sys.executable
            import threading
            import time
            
            # 定义导出步骤
            export_steps = [
                "获取已安装的包",
                "处理包列表数据",
                "写入文件",
                "验证导出结果"
            ]
            
            # 启动导出线程
            result = None
            export_error = None
            packages = None
            
            def export_thread():
                nonlocal result, export_error, packages
                try:
                    # 获取已安装的包
                    result = subprocess.run(
                        [python_path, "-m", "pip", "list", "--format=freeze"],
                        capture_output=True,
                        text=True,
                        timeout=30
                    )
                    if result.returncode == 0:
                        packages = result.stdout
                except Exception as e:
                    export_error = e
            
            thread = threading.Thread(target=export_thread)
            thread.daemon = True
            thread.start()
            
            # 显示进度
            step = 0
            while thread.is_alive() and step < len(export_steps):
                print(f"[{export_steps[step]}] ", end="")
                self._print_spinner()
                time.sleep(0.3)
                step += 1
            
            # 等待线程结束
            thread.join()
            
            if export_error:
                print(f"\n导出包列表时出错: {export_error}")
                return
            
            if result.returncode == 0 and packages:
                # 导出到文件
                export_path = os.path.join(os.getcwd(), "requirements.txt")
                with open(export_path, "w", encoding="utf-8") as f:
                    f.write(packages)
                
                print(f"\n包列表已导出到: {export_path}")
                # 修复f-string语法错误
                newline = '\n'
                package_count = len(packages.strip().split(newline))
                print(f"共导出 {package_count} 个包")
            else:
                print(f"\n导出包列表失败: {result.stderr}")
        except Exception as e:
            print(f"导出包列表时出错: {e}")
    
    def install_from_requirements(self):
        """从文件安装包"""
        print("\n从文件安装包")
        
        import subprocess
        import sys
        import os
        import time
        import threading
        
        try:
            python_path = sys.executable
            mirror_url = self.get_default_mirror_url()
            
            # 让用户输入文件路径
            file_path = input("请输入requirements文件路径（默认: requirements.txt）: ")
            if not file_path:
                file_path = "requirements.txt"
            
            # 检查文件是否存在
            if not os.path.exists(file_path):
                print(f"\n文件不存在: {file_path}")
                return
            
            print(f"\n从文件安装包: {file_path}")
            print(f"使用镜像源: {self.get_mirror_name(self.default_mirror)} - {mirror_url}")
            
            # 定义安装步骤
            install_steps = [
                "读取依赖文件",
                "解析依赖关系",
                "下载依赖包",
                "安装依赖包",
                "验证安装结果"
            ]
            
            # 启动安装线程
            result = None
            error = None
            
            def install_thread():
                nonlocal result, error
                try:
                    cmd = [python_path, "-m", "pip", "install", "-r", file_path]
                    if mirror_url:
                        cmd.extend(["-i", mirror_url])
                    
                    result = subprocess.run(
                        cmd,
                        capture_output=True,
                        text=True,
                        timeout=300  # 增加超时时间
                    )
                except Exception as e:
                    error = e
            
            thread = threading.Thread(target=install_thread)
            thread.daemon = True
            thread.start()
            
            # 显示进度
            step = 0
            while thread.is_alive() and step < len(install_steps):
                print(f"[{install_steps[step]}] ", end="")
                self._print_spinner()
                time.sleep(0.5)
                step += 1
            
            # 等待线程结束
            thread.join()
            
            if error:
                raise error
            
            if result.returncode == 0:
                print("\n✅ 从文件安装包成功！")
                print(result.stdout)
            else:
                print(f"\n❌ 从文件安装包失败: {result.stderr}")
                self.detect_pip_error(result.stderr)
        except Exception as e:
            print(f"从文件安装包时出错: {e}")
    
    def fix_pip_with_ensurepip(self):
        """使用ensurepip修复pip"""
        import subprocess
        import sys
        import time
        import threading
        
        try:
            python_path = sys.executable
            print(f"\n正在使用ensurepip修复pip...")
            print(f"使用Python可执行文件: {python_path}")
            
            # 定义修复步骤
            fix_steps = [
                "启动ensurepip模块",
                "检查当前pip版本",
                "下载最新版本",
                "安装并配置pip",
                "验证修复结果"
            ]
            
            # 启动修复线程
            result = None
            error = None
            
            def fix_thread():
                nonlocal result, error
                try:
                    result = subprocess.run(
                        [python_path, "-m", "ensurepip", "--upgrade"],
                        capture_output=True,
                        text=True,
                        timeout=30
                    )
                except Exception as e:
                    error = e
            
            thread = threading.Thread(target=fix_thread)
            thread.daemon = True
            thread.start()
            
            # 显示进度
            step = 0
            while thread.is_alive() and step < len(fix_steps):
                print(f"[{fix_steps[step]}] ", end="")
                self._print_spinner()
                time.sleep(0.5)
                step += 1
            
            # 等待线程结束
            thread.join()
            
            if error:
                raise error
            
            if result.returncode == 0:
                print("\n[验证修复结果] ✅")
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

