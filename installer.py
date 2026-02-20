import os
import requests
import subprocess
import tempfile

class PythonInstaller:
    def __init__(self):
        self.temp_dir = tempfile.gettempdir()
    
    def download_installer(self, url, version):
        """下载Python安装程序"""
        try:
            # 生成文件名
            file_name = f"python-{version}-installer.exe"
            file_path = os.path.join(self.temp_dir, file_name)
            
            # 发送请求下载文件
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()
            
            # 获取文件大小
            total_size = int(response.headers.get('content-length', 0))
            downloaded_size = 0
            
            # 写入文件
            print(f"开始下载 Python {version} 安装程序...")
            print(f"文件大小: {self._format_size(total_size)}")
            
            with open(file_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)
                        downloaded_size += len(chunk)
                        # 显示进度
                        if total_size > 0:
                            progress = int((downloaded_size / total_size) * 100)
                            self._print_progress(progress, downloaded_size, total_size)
            
            print("\n下载完成！")
            return file_path
            
        except Exception as e:
            print(f"\n下载失败: {e}")
            return None
    
    def _format_size(self, size):
        """格式化文件大小"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /= 1024
        return f"{size:.2f} TB"
    
    def _print_progress(self, progress, current, total):
        """打印进度条"""
        bar_length = 50
        filled_length = int(bar_length * progress / 100)
        bar = '█' * filled_length + '-' * (bar_length - filled_length)
        current_formatted = self._format_size(current)
        total_formatted = self._format_size(total)
        print(f"\r[{bar}] {progress}% ({current_formatted}/{total_formatted})", end="")
    
    def install(self, version, download_url):
        """安装Python"""
        try:
            # 下载安装程序
            installer_path = self.download_installer(download_url, version)
            if not installer_path:
                return False
            
            # 构建安装命令（静默安装）
            # 注意：不同版本的Python安装参数可能略有不同
            install_args = [
                installer_path,
                "/quiet",  # 静默安装
                "/norestart",  # 不重启
                "PrependPath=1",  # 添加到PATH环境变量
                "Include_pip=1",  # 安装pip
                "Include_tcltk=1",  # 安装Tcl/Tk
                "Include_test=0",  # 不安装测试套件
                "Include_doc=0"  # 不安装文档
            ]
            
            # 执行安装命令
            print(f"\n开始安装 Python {version}...")
            print("安装过程可能需要几分钟时间，请耐心等待...")
            
            # 导入所需模块
            import time
            import threading
            
            # 安装步骤
            install_steps = [
                "准备安装环境",
                "复制文件到系统",
                "配置环境变量",
                "安装pip包管理器",
                "注册系统服务",
                "完成安装"
            ]
            
            # 进度变量
            progress = 0
            step_index = 0
            install_complete = False
            install_error = None
            
            # 进度显示函数
            def show_progress():
                nonlocal progress, step_index, install_complete, install_error
                start_time = time.time()
                
                while not install_complete:
                    # 更新进度
                    if step_index < len(install_steps):
                        current_step = install_steps[step_index]
                        # 计算当前步骤的进度
                        step_progress = min(100, int((time.time() - start_time) * 2))
                        progress = int((step_index / len(install_steps)) * 100) + int((step_progress / 100) * (100 / len(install_steps)))
                        progress = min(99, progress)  # 留1%给完成步骤
                        
                        # 打印进度
                        bar_length = 50
                        filled_length = int(bar_length * progress / 100)
                        bar = '█' * filled_length + '-' * (bar_length - filled_length)
                        print(f"\r[{bar}] {progress}% - {current_step}", end="")
                        
                        # 如果当前步骤超过30秒，进入下一步
                        if step_progress >= 100:
                            step_index += 1
                            start_time = time.time()
                    
                    time.sleep(0.5)
                
                # 安装完成
                if not install_error:
                    progress = 100
                    bar_length = 50
                    filled_length = int(bar_length * progress / 100)
                    bar = '█' * filled_length + '-' * (bar_length - filled_length)
                    print(f"\r[{bar}] {progress}% - 安装完成！", end="")
                    print()
            
            # 启动进度显示线程
            progress_thread = threading.Thread(target=show_progress)
            progress_thread.daemon = True
            progress_thread.start()
            
            # 执行安装命令
            start_time = time.time()
            
            try:
                result = subprocess.run(
                    install_args,
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
            except Exception as e:
                install_error = e
                raise
            finally:
                install_complete = True
                time.sleep(1)  # 给进度线程一点时间来更新显示
            
            end_time = time.time()
            install_duration = int(end_time - start_time)
            
            print(f"✅ Python {version} 安装成功！")
            print(f"安装用时: {install_duration} 秒")
            
            # 清理临时文件
            if os.path.exists(installer_path):
                os.remove(installer_path)
                print(f"清理临时文件: {installer_path}")
            
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"\n❌ 安装命令执行失败: {e}")
            print(f"错误输出: {e.stderr}")
            return False
        except Exception as e:
            print(f"\n❌ 安装过程中出错: {e}")
            return False
    
    def verify_installation(self, version):
        """验证Python安装是否成功"""
        try:
            # 尝试运行python命令
            result = subprocess.run(
                ["python", "--version"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                installed_version = result.stdout.strip().split()[1]
                print(f"已安装的Python版本: {installed_version}")
                # 检查是否是我们刚刚安装的版本
                if installed_version.startswith(version[:3]):  # 只检查主版本号和次版本号
                    print(f"验证成功: Python {version} 已正确安装")
                    return True
                else:
                    print(f"验证失败: 已安装的版本 ({installed_version}) 与请求的版本 ({version}) 不匹配")
                    return False
            else:
                print(f"验证失败: 无法运行python命令")
                print(f"错误输出: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"验证过程中出错: {e}")
            return False

if __name__ == "__main__":
    # 测试安装功能
    installer = PythonInstaller()
    # 这里需要传入实际的版本和下载链接
    # installer.install("3.10.0", "https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe")
