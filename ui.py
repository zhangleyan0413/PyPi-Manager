import tkinter as tk
from tkinter import ttk, messagebox
import threading

class PythonInstallerUI:
    def __init__(self, root, version_fetcher, installer):
        self.root = root
        self.version_fetcher = version_fetcher
        self.installer = installer
        self.available_versions = []
        
        self.root.title("Python版本选择安装器")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        # 设置图标（可选）
        # self.root.iconbitmap("python_icon.ico")
        
        # 创建主框架
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建标题
        self.title_label = ttk.Label(
            self.main_frame, 
            text="Python版本选择安装器", 
            font=("微软雅黑", 16, "bold")
        )
        self.title_label.pack(pady=10)
        
        # 创建版本获取按钮
        self.fetch_button = ttk.Button(
            self.main_frame, 
            text="获取可用版本", 
            command=self.fetch_versions
        )
        self.fetch_button.pack(pady=10)
        
        # 创建版本列表框
        self.version_frame = ttk.LabelFrame(self.main_frame, text="可用Python版本", padding="10")
        self.version_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # 创建滚动条
        self.scrollbar = ttk.Scrollbar(self.version_frame, orient=tk.VERTICAL)
        
        # 创建列表框
        self.version_listbox = tk.Listbox(
            self.version_frame, 
            yscrollcommand=self.scrollbar.set, 
            width=70, 
            height=15
        )
        
        self.scrollbar.config(command=self.version_listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.version_listbox.pack(fill=tk.BOTH, expand=True)
        
        # 创建安装按钮
        self.install_button = ttk.Button(
            self.main_frame, 
            text="安装选中版本", 
            command=self.install_selected_version,
            state=tk.DISABLED
        )
        self.install_button.pack(pady=10)
        
        # 创建状态栏
        self.status_var = tk.StringVar()
        self.status_var.set("就绪")
        self.status_bar = ttk.Label(
            self.main_frame, 
            textvariable=self.status_var, 
            relief=tk.SUNKEN, 
            anchor=tk.W
        )
        self.status_bar.pack(fill=tk.X, pady=10)
        
    def fetch_versions(self):
        """获取可用版本信息"""
        def fetch_in_thread():
            self.status_var.set("正在获取版本信息...")
            self.fetch_button.config(state=tk.DISABLED)
            
            try:
                # 调用版本获取器获取版本列表
                self.available_versions = self.version_fetcher.get_available_versions()
                
                # 清空列表框
                self.version_listbox.delete(0, tk.END)
                
                if not self.available_versions:
                    messagebox.showerror("错误", "无法获取Python版本信息，请检查网络连接")
                    self.status_var.set("获取失败")
                    return
                
                # 填充版本列表
                for version_info in self.available_versions:
                    version_text = f"{version_info['type']}: Python {version_info['version']} ({version_info['date']})"
                    self.version_listbox.insert(tk.END, version_text)
                
                self.status_var.set(f"成功获取 {len(self.available_versions)} 个版本")
                self.install_button.config(state=tk.NORMAL)
                
            except Exception as e:
                messagebox.showerror("错误", f"获取版本信息时出错: {str(e)}")
                self.status_var.set("获取失败")
            finally:
                self.fetch_button.config(state=tk.NORMAL)
        
        # 在后台线程中执行，避免界面卡顿
        thread = threading.Thread(target=fetch_in_thread)
        thread.daemon = True
        thread.start()
    
    def install_selected_version(self):
        """安装选中的版本"""
        # 获取选中的索引
        selected_index = self.version_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("警告", "请先选择一个Python版本")
            return
        
        # 获取选中的版本信息
        selected_version_info = self.available_versions[selected_index[0]]
        version = selected_version_info['version']
        
        # 确认安装
        if not messagebox.askyesno("确认安装", f"确定要安装 Python {version} 吗？"):
            return
        
        def install_in_thread():
            self.status_var.set(f"正在准备安装 Python {version}...")
            self.install_button.config(state=tk.DISABLED)
            self.fetch_button.config(state=tk.DISABLED)
            
            try:
                # 获取下载链接
                download_url = self.version_fetcher.get_download_url(version)
                if not download_url:
                    messagebox.showerror("错误", f"无法获取 Python {version} 的下载链接")
                    self.status_var.set("安装失败")
                    return
                
                # 下载并安装
                self.status_var.set(f"正在下载 Python {version}...")
                success = self.installer.install(version, download_url)
                
                if success:
                    messagebox.showinfo("成功", f"Python {version} 安装成功！")
                    self.status_var.set(f"Python {version} 安装成功")
                else:
                    messagebox.showerror("错误", f"Python {version} 安装失败")
                    self.status_var.set("安装失败")
                    
            except Exception as e:
                messagebox.showerror("错误", f"安装过程中出错: {str(e)}")
                self.status_var.set("安装失败")
            finally:
                self.install_button.config(state=tk.NORMAL)
                self.fetch_button.config(state=tk.NORMAL)
        
        # 在后台线程中执行，避免界面卡顿
        thread = threading.Thread(target=install_in_thread)
        thread.daemon = True
        thread.start()

if __name__ == "__main__":
    # 测试界面
    root = tk.Tk()
    # 这里需要传入实际的version_fetcher和installer实例
    # ui = PythonInstallerUI(root, version_fetcher, installer)
    root.mainloop()
