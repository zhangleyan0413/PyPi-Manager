import wx
import wx.adv
import sys
import os
import threading
import time

class ProgressDialog(wx.Dialog):
    """进度条对话框"""
    def __init__(self, parent, title, maximum=100):
        super().__init__(parent, title=title, size=(400, 120))
        
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        # 创建进度条
        self.gauge = wx.Gauge(panel, range=maximum)
        vbox.Add(self.gauge, 0, wx.ALL | wx.EXPAND, 10)
        
        # 创建状态文本
        self.status_text = wx.StaticText(panel, label="准备中...")
        vbox.Add(self.status_text, 0, wx.ALL | wx.ALIGN_CENTER, 10)
        
        panel.SetSizer(vbox)
        self.Center()
    
    def update(self, value, status=""):
        """更新进度条"""
        if wx.Thread_IsMain():
            self.gauge.SetValue(value)
            if status:
                self.status_text.SetLabel(status)
            self.Refresh()
            self.Update()
        else:
            wx.CallAfter(self.gauge.SetValue, value)
            if status:
                wx.CallAfter(self.status_text.SetLabel, status)
            wx.CallAfter(self.Refresh)
            wx.CallAfter(self.Update)
    
    def close(self):
        """关闭对话框"""
        if wx.Thread_IsMain():
            self.Close()
        else:
            wx.CallAfter(self.Close)

# 添加当前目录到系统路径，确保可以导入其他模块
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from version_fetcher import VersionFetcher
from installer import PythonInstaller

class PyPiManagerGUI(wx.Frame):
    def __init__(self):
        super().__init__(None, title="PyPi Manager", size=(900, 700))
        self.SetIcon(wx.Icon(os.path.join(os.path.dirname(__file__), "icon.ico")) if os.path.exists(os.path.join(os.path.dirname(__file__), "icon.ico")) else wx.NullIcon)
        
        # 初始化各个模块
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
        
        # 创建主面板
        self.panel = wx.Panel(self)
        
        # 创建状态栏
        self.status_bar = self.CreateStatusBar()
        self.status_bar.SetStatusText("就绪")
        
        # 创建主菜单
        self.create_main_menu()
        
        # 显示主窗口
        self.Center()
        self.Show()
    
    def create_main_menu(self):
        """创建主菜单"""
        # 创建菜单条
        menu_bar = wx.MenuBar()
        
        # 创建文件菜单
        file_menu = wx.Menu()
        
        # 新建项目
        new_item = file_menu.Append(wx.ID_NEW, "新建项目(&N)", "创建新的Python项目")
        self.Bind(wx.EVT_MENU, self.on_new_project, new_item)
        
        # 打开项目
        open_item = file_menu.Append(wx.ID_OPEN, "打开项目(&O)", "打开已有的Python项目")
        self.Bind(wx.EVT_MENU, self.on_open_project, open_item)
        
        # 添加分隔线
        file_menu.AppendSeparator()
        
        # 退出
        exit_item = file_menu.Append(wx.ID_EXIT, "退出(&E)", "退出程序")
        self.Bind(wx.EVT_MENU, self.on_exit, exit_item)
        
        menu_bar.Append(file_menu, "文件(&F)")
        
        # 创建包管理菜单
        package_menu = wx.Menu()
        
        # pip包管理
        pip_manage_item = package_menu.Append(wx.ID_ANY, "管理pip包(&P)", "管理Python包")
        self.Bind(wx.EVT_MENU, self.manage_pip_packages, pip_manage_item)
        
        # 检查并修复pip
        pip_fix_item = package_menu.Append(wx.ID_ANY, "检查并修复pip(&F)", "检查并修复pip")
        self.Bind(wx.EVT_MENU, self.check_and_fix_pip, pip_fix_item)
        
        # 配置镜像源
        mirror_item = package_menu.Append(wx.ID_ANY, "配置镜像源(&M)", "配置pip镜像源")
        self.Bind(wx.EVT_MENU, self.manage_mirrors, mirror_item)
        
        # 添加分隔线
        package_menu.AppendSeparator()
        
        # 批量包管理
        batch_item = package_menu.Append(wx.ID_ANY, "批量包管理(&B)", "批量管理Python包")
        self.Bind(wx.EVT_MENU, self.batch_package_management, batch_item)
        
        menu_bar.Append(package_menu, "包管理(&P)")
        
        # 创建Python菜单
        python_menu = wx.Menu()
        
        # Python版本管理
        python_item = python_menu.Append(wx.ID_ANY, "Python版本管理(&V)", "管理Python版本")
        self.Bind(wx.EVT_MENU, self.manage_python_versions, python_item)
        
        # Python环境管理
        env_item = python_menu.Append(wx.ID_ANY, "Python环境管理(&E)", "管理Python虚拟环境")
        self.Bind(wx.EVT_MENU, self.manage_python_environments, env_item)
        
        menu_bar.Append(python_menu, "Python(&Y)")
        
        # 创建工具菜单
        tool_menu = wx.Menu()
        
        # 代码格式化
        format_item = tool_menu.Append(wx.ID_ANY, "代码格式化(&F)", "格式化Python代码")
        self.Bind(wx.EVT_MENU, self.format_code, format_item)
        
        # 代码检查
        lint_item = tool_menu.Append(wx.ID_ANY, "代码检查(&L)", "检查Python代码质量")
        self.Bind(wx.EVT_MENU, self.lint_code, lint_item)
        
        menu_bar.Append(tool_menu, "工具(&T)")
        
        # 创建帮助菜单
        help_menu = wx.Menu()
        
        # 检查更新
        update_item = help_menu.Append(wx.ID_ANY, "检查更新(&U)", "检查程序更新")
        self.Bind(wx.EVT_MENU, self.check_for_updates, update_item)
        
        # 检查文件完整性
        integrity_item = help_menu.Append(wx.ID_ANY, "检查文件完整性(&I)", "检查程序文件完整性")
        self.Bind(wx.EVT_MENU, self.check_file_integrity, integrity_item)
        
        # 添加分隔线
        help_menu.AppendSeparator()
        
        # 文档
        doc_item = help_menu.Append(wx.ID_ANY, "文档(&D)", "查看程序文档")
        self.Bind(wx.EVT_MENU, self.show_documentation, doc_item)
        
        # 关于作者
        about_item = help_menu.Append(wx.ID_ABOUT, "关于作者(&A)", "关于程序和作者")
        self.Bind(wx.EVT_MENU, self.show_author_info, about_item)
        
        menu_bar.Append(help_menu, "帮助(&H)")
        
        # 设置菜单条
        self.SetMenuBar(menu_bar)
        
        # 创建主面板内容
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        # 添加标题区域
        title_panel = wx.Panel(self.panel)
        title_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        # 添加图标
        icon_path = os.path.join(os.path.dirname(__file__), "icon.ico")
        if os.path.exists(icon_path):
            icon = wx.Bitmap(icon_path, wx.BITMAP_TYPE_ICO)
            icon_ctrl = wx.StaticBitmap(title_panel, bitmap=icon)
            title_sizer.Add(icon_ctrl, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 10)
        
        # 添加标题
        title = wx.StaticText(title_panel, label="PyPi Manager")
        title_font = wx.Font(24, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        title.SetFont(title_font)
        title.SetForegroundColour(wx.Colour(0, 100, 200))
        title_sizer.Add(title, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 10)
        
        title_panel.SetSizer(title_sizer)
        vbox.Add(title_panel, 0, wx.ALL | wx.EXPAND, 10)
        
        # 添加版本信息
        version_info = wx.StaticText(self.panel, label="版本: 1.3.0", style=wx.ALIGN_RIGHT)
        version_font = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_NORMAL)
        version_info.SetFont(version_font)
        version_info.SetForegroundColour(wx.Colour(100, 100, 100))
        vbox.Add(version_info, 0, wx.ALL | wx.ALIGN_RIGHT, 10)
        
        # 添加快速操作区域
        quick_panel = wx.Panel(self.panel)
        quick_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        # 快速操作标题
        quick_title = wx.StaticText(quick_panel, label="快速操作:")
        quick_title.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        quick_sizer.Add(quick_title, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 10)
        
        # 添加间隔
        quick_sizer.Add((20, 0), 0)
        
        # 快速安装按钮
        quick_install_btn = wx.Button(quick_panel, label="快速安装包")
        quick_install_btn.Bind(wx.EVT_BUTTON, self.quick_install_package)
        quick_sizer.Add(quick_install_btn, 0, wx.ALL, 5)
        
        # 添加间隔
        quick_sizer.Add((10, 0), 0)
        
        # 快速卸载按钮
        quick_uninstall_btn = wx.Button(quick_panel, label="快速卸载包")
        quick_uninstall_btn.Bind(wx.EVT_BUTTON, self.quick_uninstall_package)
        quick_sizer.Add(quick_uninstall_btn, 0, wx.ALL, 5)
        
        # 添加间隔
        quick_sizer.Add((10, 0), 0)
        
        # 检查更新按钮
        check_update_btn = wx.Button(quick_panel, label="检查更新")
        check_update_btn.Bind(wx.EVT_BUTTON, self.check_for_updates)
        quick_sizer.Add(check_update_btn, 0, wx.ALL, 5)
        
        quick_panel.SetSizer(quick_sizer)
        vbox.Add(quick_panel, 0, wx.ALL | wx.EXPAND, 10)
        
        # 添加功能按钮网格
        grid_sizer = wx.GridSizer(2, 3, 10, 10)
        
        # 按钮1: 管理pip包
        pip_btn = wx.Button(self.panel, label="管理pip包")
        pip_btn.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        pip_btn.SetBackgroundColour(wx.Colour(220, 240, 255))
        pip_btn.Bind(wx.EVT_BUTTON, self.manage_pip_packages)
        grid_sizer.Add(pip_btn, 0, wx.EXPAND)
        
        # 按钮2: 检查并修复pip
        fix_btn = wx.Button(self.panel, label="检查并修复pip")
        fix_btn.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        fix_btn.SetBackgroundColour(wx.Colour(220, 240, 255))
        fix_btn.Bind(wx.EVT_BUTTON, self.check_and_fix_pip)
        grid_sizer.Add(fix_btn, 0, wx.EXPAND)
        
        # 按钮3: 配置镜像源
        mirror_btn = wx.Button(self.panel, label="配置镜像源")
        mirror_btn.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        mirror_btn.SetBackgroundColour(wx.Colour(220, 240, 255))
        mirror_btn.Bind(wx.EVT_BUTTON, self.manage_mirrors)
        grid_sizer.Add(mirror_btn, 0, wx.EXPAND)
        
        # 按钮4: 批量包管理
        batch_btn = wx.Button(self.panel, label="批量包管理")
        batch_btn.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        batch_btn.SetBackgroundColour(wx.Colour(220, 240, 255))
        batch_btn.Bind(wx.EVT_BUTTON, self.batch_package_management)
        grid_sizer.Add(batch_btn, 0, wx.EXPAND)
        
        # 按钮5: Python版本管理
        python_btn = wx.Button(self.panel, label="Python版本管理")
        python_btn.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        python_btn.SetBackgroundColour(wx.Colour(220, 240, 255))
        python_btn.Bind(wx.EVT_BUTTON, self.manage_python_versions)
        grid_sizer.Add(python_btn, 0, wx.EXPAND)
        
        # 按钮6: Python环境管理
        env_btn = wx.Button(self.panel, label="Python环境管理")
        env_btn.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        env_btn.SetBackgroundColour(wx.Colour(220, 240, 255))
        env_btn.Bind(wx.EVT_BUTTON, self.manage_python_environments)
        grid_sizer.Add(env_btn, 0, wx.EXPAND)
        
        vbox.Add(grid_sizer, 0, wx.ALL | wx.EXPAND, 20)
        
        # 添加系统信息区域
        info_panel = wx.Panel(self.panel)
        info_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # 系统信息标题
        info_title = wx.StaticText(info_panel, label="系统信息:")
        info_title.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        info_sizer.Add(info_title, 0, wx.ALL, 10)
        
        # Python版本信息
        python_version = f"Python版本: {sys.version.split()[0]}"
        python_info = wx.StaticText(info_panel, label=python_version)
        info_sizer.Add(python_info, 0, wx.LEFT | wx.RIGHT, 10)
        
        # pip版本信息
        try:
            import pip
            pip_version = f"pip版本: {pip.__version__}"
        except:
            pip_version = "pip版本: 未知"
        pip_info = wx.StaticText(info_panel, label=pip_version)
        info_sizer.Add(pip_info, 0, wx.LEFT | wx.RIGHT, 10)
        
        # 当前镜像源信息
        current_mirror = self.mirror_sources.get(self.default_mirror, "未知")
        mirror_info = wx.StaticText(info_panel, label=f"当前镜像源: {current_mirror}")
        info_sizer.Add(mirror_info, 0, wx.LEFT | wx.RIGHT, 10)
        
        info_panel.SetSizer(info_sizer)
        vbox.Add(info_panel, 0, wx.ALL | wx.EXPAND, 10)
        

        
        self.panel.SetSizer(vbox)
    
    def on_exit(self, event):
        """退出程序"""
        self.Close()
    
    def on_new_project(self, event):
        """新建项目"""
        dlg = wx.DirDialog(self, "选择项目目录", style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
        if dlg.ShowModal() == wx.ID_OK:
            project_dir = dlg.GetPath()
            # 创建基本的项目结构
            try:
                # 创建requirements.txt文件
                req_path = os.path.join(project_dir, "requirements.txt")
                with open(req_path, 'w', encoding='utf-8') as f:
                    f.write("# Python dependencies\n")
                
                # 创建README.md文件
                readme_path = os.path.join(project_dir, "README.md")
                with open(readme_path, 'w', encoding='utf-8') as f:
                    f.write("# Project README\n\nDescription of your project\n")
                
                # 创建main.py文件
                main_path = os.path.join(project_dir, "main.py")
                with open(main_path, 'w', encoding='utf-8') as f:
                    f.write("# Main script\n\nif __name__ == '__main__':\n    print('Hello, World!')\n")
                
                self.show_message("成功", f"项目创建成功：{project_dir}", wx.ICON_INFORMATION)
            except Exception as e:
                self.show_message("错误", f"创建项目失败：{str(e)}", wx.ICON_ERROR)
        dlg.Destroy()
    
    def on_open_project(self, event):
        """打开项目"""
        dlg = wx.DirDialog(self, "选择项目目录", style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            project_dir = dlg.GetPath()
            # 检查项目结构
            has_req = os.path.exists(os.path.join(project_dir, "requirements.txt"))
            has_main = os.path.exists(os.path.join(project_dir, "main.py"))
            
            info = f"项目目录：{project_dir}\n"
            info += f"包含requirements.txt：{'是' if has_req else '否'}\n"
            info += f"包含main.py：{'是' if has_main else '否'}\n"
            
            # 如果有requirements.txt，显示依赖项
            if has_req:
                try:
                    with open(os.path.join(project_dir, "requirements.txt"), 'r', encoding='utf-8') as f:
                        dependencies = f.read().strip()
                    if dependencies:
                        info += f"\n依赖项：\n{dependencies}"
                    else:
                        info += "\n依赖项：无"
                except Exception as e:
                    info += f"\n读取依赖项失败：{str(e)}"
            
            self.show_message("项目信息", info, wx.ICON_INFORMATION)
        dlg.Destroy()
    
    def manage_python_environments(self, event):
        """管理Python虚拟环境"""
        dlg = wx.Dialog(self, title="Python环境管理", size=(600, 400))
        panel = wx.Panel(dlg)
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        # 添加环境列表
        env_list = wx.ListCtrl(panel, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        env_list.InsertColumn(0, "环境名称", width=200)
        env_list.InsertColumn(1, "路径", width=350)
        vbox.Add(env_list, 1, wx.ALL | wx.EXPAND, 10)
        
        # 添加按钮
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        create_btn = wx.Button(panel, label="创建环境")
        activate_btn = wx.Button(panel, label="激活环境")
        delete_btn = wx.Button(panel, label="删除环境")
        close_btn = wx.Button(panel, label="关闭")
        
        btn_sizer.Add(create_btn, 0, wx.ALL, 5)
        btn_sizer.Add(activate_btn, 0, wx.ALL, 5)
        btn_sizer.Add(delete_btn, 0, wx.ALL, 5)
        btn_sizer.Add(close_btn, 0, wx.ALL, 5)
        
        vbox.Add(btn_sizer, 0, wx.ALIGN_RIGHT)
        
        panel.SetSizer(vbox)
        dlg.Center()
        
        # 绑定事件
        close_btn.Bind(wx.EVT_BUTTON, lambda e: dlg.Close())
        
        dlg.ShowModal()
        dlg.Destroy()
    
    def format_code(self, event):
        """格式化Python代码"""
        dlg = wx.FileDialog(self, "选择Python文件", wildcard="Python files (*.py)|*.py", style=wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            file_path = dlg.GetPath()
            try:
                import autopep8
                # 读取文件
                with open(file_path, 'r', encoding='utf-8') as f:
                    code = f.read()
                
                # 格式化代码
                formatted_code = autopep8.fix_code(code)
                
                # 写回文件
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(formatted_code)
                
                self.show_message("成功", f"代码格式化成功：{file_path}", wx.ICON_INFORMATION)
            except ImportError:
                self.show_message("错误", "需要安装autopep8：pip install autopep8", wx.ICON_ERROR)
            except Exception as e:
                self.show_message("错误", f"格式化失败：{str(e)}", wx.ICON_ERROR)
        dlg.Destroy()
    
    def lint_code(self, event):
        """检查Python代码质量"""
        dlg = wx.FileDialog(self, "选择Python文件", wildcard="Python files (*.py)|*.py", style=wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            file_path = dlg.GetPath()
            try:
                import pylint
                from pylint.lint import Run
                
                # 运行pylint
                results = Run([file_path], exit=False)
                score = results.linter.stats.get('global_note', 0)
                
                self.show_message("代码检查结果", f"文件：{file_path}\n评分：{score}/10\n\n请查看终端输出获取详细信息", wx.ICON_INFORMATION)
            except ImportError:
                self.show_message("错误", "需要安装pylint：pip install pylint", wx.ICON_ERROR)
            except Exception as e:
                self.show_message("错误", f"检查失败：{str(e)}", wx.ICON_ERROR)
        dlg.Destroy()
    
    def show_documentation(self, event):
        """查看程序文档"""
        dlg = wx.Dialog(self, title="PyPi Manager 文档", size=(700, 500))
        panel = wx.Panel(dlg)
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        # 添加文档内容
        doc_text = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH2)
        doc_text.SetFont(wx.Font(10, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        
        # 填充文档内容
        doc_content = """PyPi Manager 文档

1. 功能介绍
   - 包管理：安装、卸载、更新Python包
   - 镜像源配置：切换不同的pip镜像源
   - 批量操作：批量安装、卸载、更新包
   - Python版本管理：安装和切换不同Python版本
   - 代码工具：格式化和检查Python代码

2. 使用指南
   - 包管理：在"包管理"菜单中选择"管理pip包"
   - 批量操作：在"包管理"菜单中选择"批量包管理"
   - 镜像源配置：在"包管理"菜单中选择"配置镜像源"
   - Python版本：在"Python"菜单中选择"Python版本管理"
   - 代码工具：在"工具"菜单中选择相应功能

3. 快捷键
   - 文件菜单：Alt+F
   - 包管理菜单：Alt+P
   - Python菜单：Alt+Y
   - 工具菜单：Alt+T
   - 帮助菜单：Alt+H

4. 常见问题
   - 安装失败：检查网络连接和镜像源设置
   - 权限错误：以管理员身份运行程序
   - 版本冲突：使用虚拟环境隔离依赖

5. 联系我们
   - 作者：myiunagn
   - 邮箱：myiunagn@outlook.com
   - GitHub：https://github.com/zhangleyan0413/PyPi-Manager
"""
        
        doc_text.SetValue(doc_content)
        vbox.Add(doc_text, 1, wx.ALL | wx.EXPAND, 10)
        
        # 添加关闭按钮
        close_btn = wx.Button(panel, label="关闭")
        close_btn.Bind(wx.EVT_BUTTON, lambda e: dlg.Close())
        vbox.Add(close_btn, 0, wx.ALL | wx.ALIGN_RIGHT, 10)
        
        panel.SetSizer(vbox)
        dlg.Center()
        dlg.ShowModal()
        dlg.Destroy()
    
    def quick_install_package(self, event):
        """快速安装包"""
        dlg = wx.Dialog(self, title="快速安装包", size=(400, 200))
        panel = wx.Panel(dlg)
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        # 包名输入
        name_sizer = wx.BoxSizer(wx.HORIZONTAL)
        name_label = wx.StaticText(panel, label="包名:")
        name_sizer.Add(name_label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 10)
        
        package_text = wx.TextCtrl(panel, size=(200, -1))
        name_sizer.Add(package_text, 1, wx.ALL, 10)
        vbox.Add(name_sizer, 0, wx.EXPAND)
        
        # 版本输入
        version_sizer = wx.BoxSizer(wx.HORIZONTAL)
        version_label = wx.StaticText(panel, label="版本:")
        version_sizer.Add(version_label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 10)
        
        version_text = wx.TextCtrl(panel, size=(200, -1), value="最新版本")
        version_sizer.Add(version_text, 1, wx.ALL, 10)
        vbox.Add(version_sizer, 0, wx.EXPAND)
        
        # 按钮
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        install_btn = wx.Button(panel, label="安装")
        cancel_btn = wx.Button(panel, label="取消")
        
        btn_sizer.Add(install_btn, 0, wx.ALL, 5)
        btn_sizer.Add(cancel_btn, 0, wx.ALL, 5)
        vbox.Add(btn_sizer, 0, wx.ALIGN_RIGHT)
        
        panel.SetSizer(vbox)
        dlg.Center()
        
        # 绑定事件
        def on_install(e):
            package_name = package_text.GetValue().strip()
            if not package_name:
                wx.MessageBox("请输入包名", "提示", wx.ICON_INFORMATION)
                return
            
            version = version_text.GetValue().strip()
            if version and version != "最新版本":
                package_spec = f"{package_name}=={version}"
            else:
                package_spec = package_name
            
            self.status_bar.SetStatusText(f"正在安装包 {package_spec}...")
            
            # 在后台线程中安装
            def install():  
                try:
                    import subprocess
                    cmd = [sys.executable, "-m", "pip", "install", package_spec, "-i", "https://pypi.tuna.tsinghua.edu.cn/simple"]
                    result = subprocess.run(cmd, capture_output=True, text=True)
                    
                    if result.returncode == 0:
                        wx.CallAfter(self.status_bar.SetStatusText, "安装包成功")
                        wx.CallAfter(wx.MessageBox, f"包 {package_spec} 安装成功", "成功", wx.ICON_INFORMATION)
                    else:
                        wx.CallAfter(self.status_bar.SetStatusText, "安装包失败")
                        wx.CallAfter(wx.MessageBox, f"安装包失败: {result.stderr}", "错误", wx.ICON_ERROR)
                except Exception as e:
                    wx.CallAfter(self.status_bar.SetStatusText, "安装包失败")
                    wx.CallAfter(wx.MessageBox, f"安装包失败: {str(e)}", "错误", wx.ICON_ERROR)
            
            import threading
            thread = threading.Thread(target=install)
            thread.daemon = True
            thread.start()
            dlg.Close()
        
        install_btn.Bind(wx.EVT_BUTTON, on_install)
        cancel_btn.Bind(wx.EVT_BUTTON, lambda e: dlg.Close())
        
        dlg.ShowModal()
        dlg.Destroy()
    
    def quick_uninstall_package(self, event):
        """快速卸载包"""
        dlg = wx.Dialog(self, title="快速卸载包", size=(400, 200))
        panel = wx.Panel(dlg)
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        # 包名输入
        name_sizer = wx.BoxSizer(wx.HORIZONTAL)
        name_label = wx.StaticText(panel, label="包名:")
        name_sizer.Add(name_label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 10)
        
        package_text = wx.TextCtrl(panel, size=(200, -1))
        name_sizer.Add(package_text, 1, wx.ALL, 10)
        vbox.Add(name_sizer, 0, wx.EXPAND)
        
        # 按钮
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        uninstall_btn = wx.Button(panel, label="卸载")
        cancel_btn = wx.Button(panel, label="取消")
        
        btn_sizer.Add(uninstall_btn, 0, wx.ALL, 5)
        btn_sizer.Add(cancel_btn, 0, wx.ALL, 5)
        vbox.Add(btn_sizer, 0, wx.ALIGN_RIGHT)
        
        panel.SetSizer(vbox)
        dlg.Center()
        
        # 绑定事件
        def on_uninstall(e):
            package_name = package_text.GetValue().strip()
            if not package_name:
                wx.MessageBox("请输入包名", "提示", wx.ICON_INFORMATION)
                return
            
            self.status_bar.SetStatusText(f"正在卸载包 {package_name}...")
            
            # 在后台线程中卸载
            def uninstall():  
                try:
                    import subprocess
                    cmd = [sys.executable, "-m", "pip", "uninstall", "-y", package_name]
                    result = subprocess.run(cmd, capture_output=True, text=True)
                    
                    if result.returncode == 0:
                        wx.CallAfter(self.status_bar.SetStatusText, "卸载包成功")
                        wx.CallAfter(wx.MessageBox, f"包 {package_name} 卸载成功", "成功", wx.ICON_INFORMATION)
                    else:
                        wx.CallAfter(self.status_bar.SetStatusText, "卸载包失败")
                        wx.CallAfter(wx.MessageBox, f"卸载包失败: {result.stderr}", "错误", wx.ICON_ERROR)
                except Exception as e:
                    wx.CallAfter(self.status_bar.SetStatusText, "卸载包失败")
                    wx.CallAfter(wx.MessageBox, f"卸载包失败: {str(e)}", "错误", wx.ICON_ERROR)
            
            import threading
            thread = threading.Thread(target=uninstall)
            thread.daemon = True
            thread.start()
            dlg.Close()
        
        uninstall_btn.Bind(wx.EVT_BUTTON, on_uninstall)
        cancel_btn.Bind(wx.EVT_BUTTON, lambda e: dlg.Close())
        
        dlg.ShowModal()
        dlg.Destroy()
    
    def check_file_integrity(self, event):
        """检查文件完整性"""
        import threading
        
        # 在后台线程中执行诊断逻辑
        def run_diagnostic():
            try:
                # 更新状态栏
                wx.CallAfter(self.status_bar.SetStatusText, "正在检查文件完整性...")
                
                # 获取当前目录
                current_dir = os.path.dirname(os.path.abspath(__file__))
                
                # 构建诊断结果
                output = []
                output.append("=" * 60)
                output.append("PyPi Manager - Diagnostic Tool")
                output.append("=" * 60)
                output.append(f"Current directory: {current_dir}")
                output.append(f"Python path: {sys.executable}")
                
                # 检查必要的文件
                files = ["main.py", "main_gui.py", "version_fetcher.py", "installer.py"]
                output.append("\nChecking files:")
                all_files_exist = True
                for file in files:
                    file_path = os.path.join(current_dir, file)
                    if os.path.exists(file_path):
                        output.append(f"OK {file} - exists")
                        output.append(f"  Path: {file_path}")
                    else:
                        output.append(f"ERR {file} - missing")
                        output.append(f"  Expected path: {file_path}")
                        all_files_exist = False
                
                # 检查Python版本
                output.append("\nChecking Python:")
                try:
                    output.append(f"Python version: {sys.version}")
                    output.append(f"Python path: {sys.executable}")
                    python_ok = True
                except Exception as e:
                    output.append(f"Python error: {e}")
                    python_ok = False
                
                # 检查依赖项
                output.append("\nChecking dependencies:")
                deps = ["requests", "wx"]
                deps_ok = True
                
                for dep in deps:
                    try:
                        module = __import__(dep)
                        output.append(f"OK {dep} - installed")
                        if hasattr(module, "__version__"):
                            output.append(f"  Version: {module.__version__}")
                    except ImportError as e:
                        output.append(f"ERR {dep} - not installed")
                        output.append(f"  Error: {e}")
                        deps_ok = False
                    except Exception as e:
                        output.append(f"??? {dep} - error checking")
                        output.append(f"  Error: {e}")
                        deps_ok = False
                
                # 总结
                output.append("\n" + "=" * 60)
                output.append("Check result summary:")
                output.append("=" * 60)
                
                if all_files_exist:
                    output.append("OK All necessary files exist")
                else:
                    output.append("ERR Some necessary files missing")
                
                if python_ok:
                    output.append("OK Python available")
                else:
                    output.append("ERR Python not available")
                
                if deps_ok:
                    output.append("OK All dependencies installed")
                else:
                    output.append("ERR Some dependencies missing")
                    output.append("\nPlease run:")
                    output.append("python -m pip install requests wxPython -i https://pypi.tuna.tsinghua.edu.cn/simple")
                
                # 检查是否可以导入主模块
                output.append("\n" + "=" * 60)
                output.append("Trying to import main module:")
                output.append("=" * 60)
                
                try:
                    # 添加当前目录到Python路径
                    sys.path.insert(0, current_dir)
                    
                    import main
                    output.append("OK main.py imported successfully")
                except Exception as e:
                    output.append(f"ERR main.py import failed: {e}")
                
                output.append("\n" + "=" * 60)
                output.append("Diagnostic completed")
                output.append("=" * 60)
                
                # 显示结果
                wx.CallAfter(self.status_bar.SetStatusText, "文件完整性检查完成")
                
                # 保存诊断结果
                diagnostic_output = "\n".join(output)
                
                # 如果文件不完整，询问是否从GitHub获取最新文件
                if not all_files_exist:
                    wx.CallAfter(self.ask_and_repair_files, current_dir, files, diagnostic_output)
                else:
                    # 文件完整，直接显示结果
                    wx.CallAfter(self.show_diagnostic_result, diagnostic_output)
            except Exception as e:
                wx.CallAfter(self.status_bar.SetStatusText, "文件完整性检查失败")
                error_msg = f"检查文件完整性时出错:\n{str(e)}"
                wx.CallAfter(wx.MessageBox, error_msg, "错误", wx.OK | wx.ICON_ERROR)
        
        # 启动后台线程
        thread = threading.Thread(target=run_diagnostic)
        thread.daemon = True
        thread.start()
    
    def show_diagnostic_result(self, output):
        """显示诊断结果"""
        # 创建一个对话框显示结果
        dlg = wx.Dialog(self, title="文件完整性检查结果", size=(600, 400))
        panel = wx.Panel(dlg)
        
        # 创建文本控件显示结果
        text = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_DONTWRAP)
        text.SetValue(output)
        
        # 创建确定按钮
        btn = wx.Button(panel, wx.ID_OK, "确定")
        
        # 设置布局
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(text, 1, wx.ALL | wx.EXPAND, 10)
        vbox.Add(btn, 0, wx.ALL | wx.ALIGN_CENTER, 10)
        
        panel.SetSizer(vbox)
        dlg.Center()
        dlg.ShowModal()
        dlg.Destroy()
    
    def ask_and_repair_files(self, current_dir, files, diagnostic_output):
        """询问是否修复文件并执行修复操作"""
        # 显示询问对话框
        dlg = wx.MessageDialog(
            self,
            "检测到文件不完整，是否从GitHub获取最新文件来修复？",
            "文件修复",
            wx.YES_NO | wx.ICON_QUESTION
        )
        result = dlg.ShowModal()
        dlg.Destroy()
        
        if result == wx.ID_YES:
            # 用户同意修复，开始从GitHub下载文件
            self.repair_files(current_dir, files)
        else:
            # 用户取消修复，显示诊断结果
            self.show_diagnostic_result(diagnostic_output)
    
    def repair_files(self, current_dir, files):
        """从GitHub下载最新文件并修复"""
        import threading
        import requests
        
        # 在后台线程中执行修复操作
        def run_repair():
            try:
                # 更新状态栏
                wx.CallAfter(self.status_bar.SetStatusText, "正在从GitHub下载最新文件...")
                
                # GitHub仓库信息
                repo_owner = "username"  # 替换为实际的仓库所有者
                repo_name = "pypi-manager"  # 替换为实际的仓库名称
                branch = "main"
                
                # 要下载的文件列表
                files_to_download = [
                    "main.py",
                    "main_gui.py",
                    "version_fetcher.py",
                    "installer.py"
                ]
                
                # 构建修复结果
                output = []
                output.append("=" * 60)
                output.append("文件修复结果")
                output.append("=" * 60)
                
                success_count = 0
                fail_count = 0
                
                for file in files_to_download:
                    # 构建GitHub文件URL
                    file_url = f"https://raw.githubusercontent.com/{repo_owner}/{repo_name}/{branch}/{file}"
                    file_path = os.path.join(current_dir, file)
                    
                    try:
                        # 下载文件
                        response = requests.get(file_url, timeout=10)
                        response.raise_for_status()
                        
                        # 写入文件
                        with open(file_path, "wb") as f:
                            f.write(response.content)
                        
                        output.append(f"OK {file} - 已修复")
                        success_count += 1
                    except Exception as e:
                        output.append(f"ERR {file} - 修复失败: {e}")
                        fail_count += 1
                
                # 总结
                output.append("\n" + "=" * 60)
                output.append("修复结果总结:")
                output.append("=" * 60)
                output.append(f"成功修复: {success_count} 个文件")
                output.append(f"修复失败: {fail_count} 个文件")
                
                if fail_count == 0:
                    output.append("\n所有文件修复成功！")
                else:
                    output.append("\n部分文件修复失败，请手动检查。")
                
                output.append("\n" + "=" * 60)
                output.append("修复完成")
                output.append("=" * 60)
                
                # 显示结果
                wx.CallAfter(self.status_bar.SetStatusText, "文件修复完成")
                wx.CallAfter(self.show_diagnostic_result, "\n".join(output))
            except Exception as e:
                wx.CallAfter(self.status_bar.SetStatusText, "文件修复失败")
                error_msg = f"修复文件时出错:\n{str(e)}"
                wx.CallAfter(wx.MessageBox, error_msg, "错误", wx.OK | wx.ICON_ERROR)
        
        # 启动后台线程
        thread = threading.Thread(target=run_repair)
        thread.daemon = True
        thread.start()
    
    def show_message(self, title, message, style=wx.ICON_INFORMATION):
        """显示消息对话框"""
        dlg = wx.MessageDialog(self, message, title, style)
        dlg.ShowModal()
        dlg.Destroy()
    
    def show_author_info(self, event):
        """显示关于作者信息"""
        info = wx.adv.AboutDialogInfo()
        info.SetName("PyPi Manager")
        info.SetVersion("1.3.0")
        info.SetDescription("A powerful Python package management tool")
        info.SetCopyright("(C) 2026 PyPi Manager")
        info.SetWebSite("https://github.com/zhangleyan0413/PyPi-Manager")
        info.AddDeveloper("myiunagn (myiunagn@outlook.com)")
        
        wx.adv.AboutBox(info)
    
    def manage_pip_packages(self, event):
        """管理pip包"""
        # 创建pip包管理对话框
        dlg = PipPackageManagerDialog(self)
        dlg.ShowModal()
        dlg.Destroy()
    
    def check_and_fix_pip(self, event):
        """检查并修复pip"""
        # 创建pip修复对话框
        dlg = PipFixDialog(self)
        dlg.ShowModal()
        dlg.Destroy()
    
    def manage_mirrors(self, event):
        """配置镜像源"""
        # 创建镜像源管理对话框
        dlg = MirrorManagerDialog(self)
        dlg.ShowModal()
        dlg.Destroy()
    
    def batch_package_management(self, event):
        """批量包管理"""
        # 创建批量包管理对话框
        dlg = BatchPackageManagerDialog(self)
        dlg.ShowModal()
        dlg.Destroy()
    
    def manage_python_versions(self, event):
        """Python版本管理"""
        # 创建Python版本管理对话框
        dlg = PythonVersionManagerDialog(self)
        dlg.ShowModal()
        dlg.Destroy()
    
    def check_for_updates(self, event):
        """检查更新"""
        # 创建检查更新对话框
        dlg = UpdateCheckerDialog(self)
        dlg.ShowModal()
        dlg.Destroy()

class PipPackageManagerDialog(wx.Dialog):
    def __init__(self, parent):
        super().__init__(parent, title="pip包管理", size=(700, 500))
        self.parent = parent
        
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        # 创建选项卡
        notebook = wx.Notebook(panel)
        
        # 已安装包选项卡
        installed_tab = wx.Panel(notebook)
        self.create_installed_packages_tab(installed_tab)
        notebook.AddPage(installed_tab, "已安装的包")
        
        # 搜索和安装选项卡
        search_install_tab = wx.Panel(notebook)
        self.create_search_install_tab(search_install_tab)
        notebook.AddPage(search_install_tab, "搜索和安装")
        
        # 卸载包选项卡
        uninstall_tab = wx.Panel(notebook)
        self.create_uninstall_package_tab(uninstall_tab)
        notebook.AddPage(uninstall_tab, "卸载包")
        
        vbox.Add(notebook, 1, wx.ALL | wx.EXPAND, 10)
        
        # 添加按钮
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        close_btn = wx.Button(panel, label="关闭")
        close_btn.Bind(wx.EVT_BUTTON, self.on_close)
        btn_sizer.Add(close_btn, 0, wx.ALL, 10)
        
        vbox.Add(btn_sizer, 0, wx.ALIGN_RIGHT)
        
        panel.SetSizer(vbox)
        self.Center()
    
    def create_installed_packages_tab(self, panel):
        """创建已安装包选项卡"""
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        # 添加刷新按钮
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        refresh_btn = wx.Button(panel, label="刷新")
        refresh_btn.Bind(wx.EVT_BUTTON, self.on_refresh_installed)
        btn_sizer.Add(refresh_btn, 0, wx.ALL, 10)
        vbox.Add(btn_sizer, 0, wx.ALIGN_LEFT)
        
        # 添加包列表
        self.installed_list = wx.ListCtrl(panel, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        self.installed_list.InsertColumn(0, "包名", width=300)
        self.installed_list.InsertColumn(1, "版本", width=100)
        vbox.Add(self.installed_list, 1, wx.ALL | wx.EXPAND, 10)
        
        panel.SetSizer(vbox)
    
    def create_search_install_tab(self, panel):
        """创建搜索和安装选项卡"""
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        # 搜索区域
        search_sizer = wx.BoxSizer(wx.HORIZONTAL)
        search_label = wx.StaticText(panel, label="包名:")
        search_sizer.Add(search_label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 10)
        
        self.search_text = wx.TextCtrl(panel, size=(300, -1))
        search_sizer.Add(self.search_text, 0, wx.ALL, 10)
        
        search_btn = wx.Button(panel, label="搜索")
        search_btn.Bind(wx.EVT_BUTTON, self.on_search)
        search_sizer.Add(search_btn, 0, wx.ALL, 10)
        
        vbox.Add(search_sizer, 0, wx.ALIGN_LEFT)
        
        # 搜索结果列表
        self.search_list = wx.ListCtrl(panel, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        self.search_list.InsertColumn(0, "版本", width=100)
        vbox.Add(self.search_list, 1, wx.ALL | wx.EXPAND, 10)
        
        # 快速安装区域
        quick_install_sizer = wx.BoxSizer(wx.HORIZONTAL)
        version_label = wx.StaticText(panel, label="快速安装:")
        quick_install_sizer.Add(version_label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 10)
        
        self.quick_install_text = wx.TextCtrl(panel, size=(300, -1), value="最新版本")
        quick_install_sizer.Add(self.quick_install_text, 0, wx.ALL, 10)
        
        quick_install_btn = wx.Button(panel, label="安装")
        quick_install_btn.Bind(wx.EVT_BUTTON, self.on_quick_install)
        quick_install_sizer.Add(quick_install_btn, 0, wx.ALL, 10)
        
        vbox.Add(quick_install_sizer, 0, wx.ALIGN_LEFT)
        
        # 从搜索结果安装按钮
        install_from_search_btn = wx.Button(panel, label="安装选中的版本")
        install_from_search_btn.Bind(wx.EVT_BUTTON, self.on_install_from_search)
        vbox.Add(install_from_search_btn, 0, wx.ALL, 10)
        
        panel.SetSizer(vbox)
    
    def create_search_packages_tab(self, panel):
        """创建搜索包选项卡"""
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        # 添加搜索控件
        search_sizer = wx.BoxSizer(wx.HORIZONTAL)
        search_label = wx.StaticText(panel, label="包名:")
        search_sizer.Add(search_label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 10)
        
        self.search_text = wx.TextCtrl(panel, size=(300, -1))
        search_sizer.Add(self.search_text, 0, wx.ALL, 10)
        
        search_btn = wx.Button(panel, label="搜索")
        search_btn.Bind(wx.EVT_BUTTON, self.on_search)
        search_sizer.Add(search_btn, 0, wx.ALL, 10)
        
        vbox.Add(search_sizer, 0, wx.ALIGN_LEFT)
        
        # 添加搜索结果列表
        self.search_list = wx.ListCtrl(panel, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        self.search_list.InsertColumn(0, "版本", width=100)
        vbox.Add(self.search_list, 1, wx.ALL | wx.EXPAND, 10)
        
        # 添加安装按钮
        install_btn = wx.Button(panel, label="安装选中版本")
        install_btn.Bind(wx.EVT_BUTTON, self.on_install_from_search)
        vbox.Add(install_btn, 0, wx.ALL, 10)
        
        panel.SetSizer(vbox)
    
    def create_install_package_tab(self, panel):
        """创建安装包选项卡"""
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        # 添加包名输入
        name_sizer = wx.BoxSizer(wx.HORIZONTAL)
        name_label = wx.StaticText(panel, label="包名:")
        name_sizer.Add(name_label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 10)
        
        self.install_name_text = wx.TextCtrl(panel, size=(300, -1))
        name_sizer.Add(self.install_name_text, 0, wx.ALL, 10)
        vbox.Add(name_sizer, 0, wx.ALIGN_LEFT)
        
        # 添加版本输入
        version_sizer = wx.BoxSizer(wx.HORIZONTAL)
        version_label = wx.StaticText(panel, label="版本:")
        version_sizer.Add(version_label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 10)
        
        self.version_text = wx.TextCtrl(panel, size=(100, -1), value="最新版本")
        version_sizer.Add(self.version_text, 0, wx.ALL, 10)
        vbox.Add(version_sizer, 0, wx.ALIGN_LEFT)
        
        # 添加安装按钮
        install_btn = wx.Button(panel, label="安装")
        install_btn.Bind(wx.EVT_BUTTON, self.on_install)
        vbox.Add(install_btn, 0, wx.ALL, 10)
        
        # 添加安装结果
        self.install_result = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY)
        vbox.Add(self.install_result, 1, wx.ALL | wx.EXPAND, 10)
        
        panel.SetSizer(vbox)
    
    def create_uninstall_package_tab(self, panel):
        """创建卸载包选项卡"""
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        # 刷新包列表按钮
        refresh_btn = wx.Button(panel, label="刷新包列表")
        refresh_btn.Bind(wx.EVT_BUTTON, self.on_refresh_packages)
        vbox.Add(refresh_btn, 0, wx.ALL, 10)
        
        # 包列表
        package_sizer = wx.BoxSizer(wx.HORIZONTAL)
        package_label = wx.StaticText(panel, label="已安装的包:")
        package_sizer.Add(package_label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 10)
        
        # 创建包列表控件
        self.package_list = wx.ListBox(panel, size=(400, 200), style=wx.LB_SINGLE)
        package_sizer.Add(self.package_list, 1, wx.ALL | wx.EXPAND, 10)
        vbox.Add(package_sizer, 0, wx.EXPAND)
        
        # 卸载按钮
        uninstall_btn = wx.Button(panel, label="卸载选中的包")
        uninstall_btn.Bind(wx.EVT_BUTTON, self.on_uninstall)
        vbox.Add(uninstall_btn, 0, wx.ALL, 10)
        
        # 结果显示
        self.uninstall_result = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY)
        vbox.Add(self.uninstall_result, 1, wx.ALL | wx.EXPAND, 10)
        
        panel.SetSizer(vbox)
        
        # 初始加载包列表
        self.on_refresh_packages(None)
    
    def on_refresh_packages(self, event):
        """刷新已安装包列表"""
        import subprocess
        import threading
        
        self.package_list.Clear()
        
        # 显示加载中
        self.parent.status_bar.SetStatusText("正在获取已安装包...")
        
        # 在后台线程中执行
        def refresh_packages():
            try:
                # 获取已安装的包
                result = subprocess.run([sys.executable, "-m", "pip", "list", "--format=freeze"], 
                                      capture_output=True, text=True, timeout=30)
                
                packages = []
                for line in result.stdout.strip().split('\n'):
                    if line:
                        package_info = line.split('==')
                        if len(package_info) >= 2:
                            packages.append(f"{package_info[0]}=={package_info[1]}")
                
                # 更新UI
                wx.CallAfter(self.package_list.Append, packages)
                wx.CallAfter(self.parent.status_bar.SetStatusText, "已安装包列表刷新完成")
            except Exception as e:
                wx.CallAfter(self.parent.status_bar.SetStatusText, "获取已安装包失败")
                wx.CallAfter(self.show_message, "错误", f"获取已安装包失败: {str(e)}", wx.ICON_ERROR)
        
        thread = threading.Thread(target=refresh_packages)
        thread.daemon = True
        thread.start()
    
    def on_refresh_installed(self, event):
        """刷新已安装包列表"""
        self.installed_list.DeleteAllItems()
        
        # 显示加载中
        self.parent.status_bar.SetStatusText("正在获取已安装包...")
        
        # 在后台线程中获取已安装包
        def get_installed_packages():
            try:
                import subprocess
                cmd = [sys.executable, "-m", "pip", "list", "--format=freeze"]
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.returncode == 0:
                    packages = result.stdout.strip().split('\n')
                    for i, pkg in enumerate(packages):
                        if pkg:
                            parts = pkg.split('==')
                            if len(parts) >= 2:
                                name = parts[0]
                                version = parts[1]
                                self.installed_list.InsertItem(i, name)
                                self.installed_list.SetItem(i, 1, version)
                    
                    wx.CallAfter(self.parent.status_bar.SetStatusText, f"共 {len(packages)} 个已安装包")
                else:
                    wx.CallAfter(self.parent.status_bar.SetStatusText, "获取已安装包失败")
                    wx.CallAfter(self.show_message, "错误", f"获取已安装包失败: {result.stderr}", wx.ICON_ERROR)
            except Exception as e:
                wx.CallAfter(self.parent.status_bar.SetStatusText, "获取已安装包失败")
                wx.CallAfter(self.show_message, "错误", f"获取已安装包失败: {str(e)}", wx.ICON_ERROR)
        
        thread = threading.Thread(target=get_installed_packages)
        thread.daemon = True
        thread.start()
    
    def on_search(self, event):
        """搜索包"""
        package_name = self.search_text.GetValue().strip()
        if not package_name:
            self.show_message("提示", "请输入包名", wx.ICON_INFORMATION)
            return
        
        self.search_list.DeleteAllItems()
        self.parent.status_bar.SetStatusText(f"正在搜索包 {package_name}...")
        
        # 在后台线程中搜索包
        def search_package():
            try:
                import subprocess
                cmd = [sys.executable, "-m", "pip", "index", "versions", package_name]
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.returncode == 0:
                    # 解析结果
                    lines = result.stdout.strip().split('\n')
                    versions = []
                    for line in lines:
                        if "Available versions:" in line:
                            # 提取版本号
                            version_str = line.split("Available versions:")[1].strip()
                            versions = [v.strip() for v in version_str.split(",")]
                            break
                    
                    for i, version in enumerate(versions):
                        self.search_list.InsertItem(i, version)
                    
                    wx.CallAfter(self.parent.status_bar.SetStatusText, f"找到 {len(versions)} 个版本")
                else:
                    wx.CallAfter(self.parent.status_bar.SetStatusText, "搜索包失败")
                    wx.CallAfter(self.show_message, "错误", f"搜索包失败: {result.stderr}", wx.ICON_ERROR)
            except Exception as e:
                wx.CallAfter(self.parent.status_bar.SetStatusText, "搜索包失败")
                wx.CallAfter(self.show_message, "错误", f"搜索包失败: {str(e)}", wx.ICON_ERROR)
        
        thread = threading.Thread(target=search_package)
        thread.daemon = True
        thread.start()
    
    def on_install_from_search(self, event):
        """从搜索结果中安装选中的版本"""
        package_name = self.search_text.GetValue().strip()
        if not package_name:
            self.show_message("提示", "请先搜索包", wx.ICON_INFORMATION)
            return
        
        # 获取选中的版本
        selected_index = self.search_list.GetFirstSelected()
        if selected_index == -1:
            self.show_message("提示", "请选择要安装的版本", wx.ICON_INFORMATION)
            return
        
        version = self.search_list.GetItemText(selected_index)
        package_spec = f"{package_name}=={version}"
        
        self.parent.status_bar.SetStatusText(f"正在安装包 {package_spec}...")
        
        # 在后台线程中安装包
        def install_package():
            try:
                import subprocess
                cmd = [sys.executable, "-m", "pip", "install", package_spec, "-i", "https://pypi.tuna.tsinghua.edu.cn/simple"]
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.returncode == 0:
                    wx.CallAfter(self.parent.status_bar.SetStatusText, "安装包成功")
                    wx.CallAfter(self.show_message, "成功", f"包 {package_spec} 安装成功", wx.ICON_INFORMATION)
                else:
                    wx.CallAfter(self.parent.status_bar.SetStatusText, "安装包失败")
                    wx.CallAfter(self.show_message, "错误", f"安装包失败: {result.stderr}", wx.ICON_ERROR)
            except Exception as e:
                wx.CallAfter(self.parent.status_bar.SetStatusText, "安装包失败")
                wx.CallAfter(self.show_message, "错误", f"安装包失败: {str(e)}", wx.ICON_ERROR)
        
        thread = threading.Thread(target=install_package)
        thread.daemon = True
        thread.start()
    
    def on_quick_install(self, event):
        """快速安装包"""
        package_name = self.search_text.GetValue().strip()
        if not package_name:
            self.show_message("提示", "请输入包名", wx.ICON_INFORMATION)
            return
        
        version = self.quick_install_text.GetValue().strip()
        if version and version != "最新版本":
            package_spec = f"{package_name}=={version}"
        else:
            package_spec = package_name
        
        self.parent.status_bar.SetStatusText(f"正在安装包 {package_spec}...")
        
        # 在后台线程中安装包
        def install_package():
            try:
                import subprocess
                cmd = [sys.executable, "-m", "pip", "install", package_spec, "-i", "https://pypi.tuna.tsinghua.edu.cn/simple"]
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.returncode == 0:
                    wx.CallAfter(self.parent.status_bar.SetStatusText, "安装包成功")
                    wx.CallAfter(self.show_message, "成功", f"包 {package_spec} 安装成功", wx.ICON_INFORMATION)
                else:
                    wx.CallAfter(self.parent.status_bar.SetStatusText, "安装包失败")
                    wx.CallAfter(self.show_message, "错误", f"安装包失败: {result.stderr}", wx.ICON_ERROR)
            except Exception as e:
                wx.CallAfter(self.parent.status_bar.SetStatusText, "安装包失败")
                wx.CallAfter(self.show_message, "错误", f"安装包失败: {str(e)}", wx.ICON_ERROR)
        
        thread = threading.Thread(target=install_package)
        thread.daemon = True
        thread.start()
    
    def on_install(self, event):
        """安装包"""
        package_name = self.install_name_text.GetValue().strip()
        if not package_name:
            self.show_message("提示", "请输入包名", wx.ICON_INFORMATION)
            return
        
        version = self.version_text.GetValue().strip()
        if version and version != "最新版本":
            package_spec = f"{package_name}=={version}"
        else:
            package_spec = package_name
        
        self.install_result.SetValue("")
        self.parent.status_bar.SetStatusText(f"正在安装包 {package_spec}...")
        
        # 在后台线程中安装包
        def install_package():
            try:
                import subprocess
                cmd = [sys.executable, "-m", "pip", "install", package_spec, "-i", "https://pypi.tuna.tsinghua.edu.cn/simple"]
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                output = f"命令: {' '.join(cmd)}\n\n"
                output += f"输出:\n{result.stdout}\n\n"
                if result.stderr:
                    output += f"错误:\n{result.stderr}\n"
                
                wx.CallAfter(self.install_result.SetValue, output)
                
                if result.returncode == 0:
                    wx.CallAfter(self.parent.status_bar.SetStatusText, "安装包成功")
                    wx.CallAfter(self.show_message, "成功", f"包 {package_spec} 安装成功", wx.ICON_INFORMATION)
                else:
                    wx.CallAfter(self.parent.status_bar.SetStatusText, "安装包失败")
                    wx.CallAfter(self.show_message, "错误", f"安装包失败", wx.ICON_ERROR)
            except Exception as e:
                wx.CallAfter(self.install_result.SetValue, f"安装失败: {str(e)}")
                wx.CallAfter(self.parent.status_bar.SetStatusText, "安装包失败")
                wx.CallAfter(self.show_message, "错误", f"安装包失败: {str(e)}", wx.ICON_ERROR)
        
        thread = threading.Thread(target=install_package)
        thread.daemon = True
        thread.start()
    
    def on_uninstall(self, event):
        """卸载包"""
        # 从包列表中获取选中的包
        selected_index = self.package_list.GetSelection()
        if selected_index == -1:
            self.show_message("提示", "请选择要卸载的包", wx.ICON_INFORMATION)
            return
        
        # 获取包名（去掉版本号）
        selected_package = self.package_list.GetString(selected_index)
        package_name = selected_package.split('==')[0]
        
        self.uninstall_result.SetValue("")
        self.parent.status_bar.SetStatusText(f"正在卸载包 {package_name}...")
        
        # 在后台线程中卸载包
        def uninstall_package():
            try:
                import subprocess
                cmd = [sys.executable, "-m", "pip", "uninstall", "-y", package_name]
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                output = f"命令: {' '.join(cmd)}\n\n"
                output += f"输出:\n{result.stdout}\n\n"
                if result.stderr:
                    output += f"错误:\n{result.stderr}\n"
                
                # 刷新包列表
                wx.CallAfter(self.on_refresh_packages, None)
                wx.CallAfter(self.uninstall_result.SetValue, output)
                
                if result.returncode == 0:
                    wx.CallAfter(self.parent.status_bar.SetStatusText, "卸载包成功")
                    wx.CallAfter(self.show_message, "成功", f"包 {package_name} 卸载成功", wx.ICON_INFORMATION)
                else:
                    wx.CallAfter(self.parent.status_bar.SetStatusText, "卸载包失败")
                    wx.CallAfter(self.show_message, "错误", f"卸载包失败", wx.ICON_ERROR)
            except Exception as e:
                wx.CallAfter(self.uninstall_result.SetValue, f"卸载失败: {str(e)}")
                wx.CallAfter(self.parent.status_bar.SetStatusText, "卸载包失败")
                wx.CallAfter(self.show_message, "错误", f"卸载包失败: {str(e)}", wx.ICON_ERROR)
        
        thread = threading.Thread(target=uninstall_package)
        thread.daemon = True
        thread.start()
    
    def show_message(self, title, message, style=wx.ICON_INFORMATION):
        """显示消息对话框"""
        dlg = wx.MessageDialog(self, message, title, style)
        dlg.ShowModal()
        dlg.Destroy()
    
    def on_close(self, event):
        """关闭对话框"""
        self.Close()

class PipFixDialog(wx.Dialog):
    def __init__(self, parent):
        super().__init__(parent, title="检查并修复pip", size=(600, 400))
        self.parent = parent
        
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        # 添加检查按钮
        check_btn = wx.Button(panel, label="检查pip状态")
        check_btn.Bind(wx.EVT_BUTTON, self.on_check_pip)
        vbox.Add(check_btn, 0, wx.ALL, 10)
        
        # 添加修复方法选择
        fix_sizer = wx.BoxSizer(wx.HORIZONTAL)
        fix_label = wx.StaticText(panel, label="修复方法:")
        fix_sizer.Add(fix_label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 10)
        
        self.fix_method = wx.Choice(panel, choices=["使用ensurepip模块", "使用get-pip.py脚本"])
        self.fix_method.SetSelection(0)
        fix_sizer.Add(self.fix_method, 1, wx.ALL, 10)
        vbox.Add(fix_sizer, 0, wx.ALL | wx.EXPAND, 10)
        
        # 添加修复按钮
        fix_btn = wx.Button(panel, label="修复pip")
        fix_btn.Bind(wx.EVT_BUTTON, self.on_fix_pip)
        vbox.Add(fix_btn, 0, wx.ALL, 10)
        
        # 添加结果文本框
        self.result_text = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY)
        vbox.Add(self.result_text, 1, wx.ALL | wx.EXPAND, 10)
        
        # 添加关闭按钮
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        close_btn = wx.Button(panel, label="关闭")
        close_btn.Bind(wx.EVT_BUTTON, self.on_close)
        btn_sizer.Add(close_btn, 0, wx.ALL, 10)
        
        vbox.Add(btn_sizer, 0, wx.ALIGN_RIGHT)
        
        panel.SetSizer(vbox)
        self.Center()
    
    def on_check_pip(self, event):
        """检查pip状态"""
        self.parent.status_bar.SetStatusText("正在检查pip状态...")
        
        # 在后台线程中检查pip状态
        def check_pip_status():
            try:
                import subprocess
                cmd = [sys.executable, "-m", "pip", "--version"]
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                output = f"命令: {' '.join(cmd)}\n\n"
                output += f"输出:\n{result.stdout}\n\n"
                if result.stderr:
                    output += f"错误:\n{result.stderr}\n"
                
                wx.CallAfter(self.result_text.SetValue, output)
                
                if result.returncode == 0:
                    wx.CallAfter(self.parent.status_bar.SetStatusText, "pip状态正常")
                    wx.CallAfter(self.show_message, "成功", "pip状态正常", wx.ICON_INFORMATION)
                else:
                    wx.CallAfter(self.parent.status_bar.SetStatusText, "pip状态异常")
                    wx.CallAfter(self.show_message, "警告", "pip状态异常，建议修复", wx.ICON_WARNING)
            except Exception as e:
                wx.CallAfter(self.result_text.SetValue, f"检查失败: {str(e)}")
                wx.CallAfter(self.parent.status_bar.SetStatusText, "检查pip状态失败")
                wx.CallAfter(self.show_message, "错误", f"检查pip状态失败: {str(e)}", wx.ICON_ERROR)
        
        thread = threading.Thread(target=check_pip_status)
        thread.daemon = True
        thread.start()
    
    def on_fix_pip(self, event):
        """修复pip"""
        fix_method = self.fix_method.GetSelection()
        self.parent.status_bar.SetStatusText("正在修复pip...")
        
        # 在后台线程中修复pip
        def fix_pip():
            try:
                import subprocess
                if fix_method == 0:
                    # 使用ensurepip模块
                    cmd = [sys.executable, "-m", "ensurepip", "--upgrade"]
                else:
                    # 使用get-pip.py脚本
                    # 先下载get-pip.py
                    import requests
                    url = "https://bootstrap.pypa.io/get-pip.py"
                    r = requests.get(url)
                    with open("get-pip.py", "wb") as f:
                        f.write(r.content)
                    cmd = [sys.executable, "get-pip.py"]
                
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                output = f"命令: {' '.join(cmd)}\n\n"
                output += f"输出:\n{result.stdout}\n\n"
                if result.stderr:
                    output += f"错误:\n{result.stderr}\n"
                
                wx.CallAfter(self.result_text.SetValue, output)
                
                # 清理临时文件
                if fix_method == 1 and os.path.exists("get-pip.py"):
                    os.remove("get-pip.py")
                
                if result.returncode == 0:
                    wx.CallAfter(self.parent.status_bar.SetStatusText, "修复pip成功")
                    wx.CallAfter(self.show_message, "成功", "修复pip成功", wx.ICON_INFORMATION)
                else:
                    wx.CallAfter(self.parent.status_bar.SetStatusText, "修复pip失败")
                    wx.CallAfter(self.show_message, "错误", "修复pip失败", wx.ICON_ERROR)
            except Exception as e:
                wx.CallAfter(self.result_text.SetValue, f"修复失败: {str(e)}")
                wx.CallAfter(self.parent.status_bar.SetStatusText, "修复pip失败")
                wx.CallAfter(self.show_message, "错误", f"修复pip失败: {str(e)}", wx.ICON_ERROR)
        
        thread = threading.Thread(target=fix_pip)
        thread.daemon = True
        thread.start()
    
    def show_message(self, title, message, style=wx.ICON_INFORMATION):
        """显示消息对话框"""
        dlg = wx.MessageDialog(self, message, title, style)
        dlg.ShowModal()
        dlg.Destroy()
    
    def on_close(self, event):
        """关闭对话框"""
        self.Close()

class MirrorManagerDialog(wx.Dialog):
    def __init__(self, parent):
        super().__init__(parent, title="配置镜像源", size=(600, 400))
        self.parent = parent
        
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        # 添加镜像源列表
        self.mirror_list = wx.ListCtrl(panel, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        self.mirror_list.InsertColumn(0, "编号", width=50)
        self.mirror_list.InsertColumn(1, "名称", width=100)
        self.mirror_list.InsertColumn(2, "URL", width=400)
        vbox.Add(self.mirror_list, 1, wx.ALL | wx.EXPAND, 10)
        
        # 添加按钮
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        refresh_btn = wx.Button(panel, label="刷新")
        refresh_btn.Bind(wx.EVT_BUTTON, self.on_refresh_mirrors)
        btn_sizer.Add(refresh_btn, 0, wx.ALL, 10)
        
        set_default_btn = wx.Button(panel, label="设为默认")
        set_default_btn.Bind(wx.EVT_BUTTON, self.on_set_default)
        btn_sizer.Add(set_default_btn, 0, wx.ALL, 10)
        
        add_btn = wx.Button(panel, label="添加")
        add_btn.Bind(wx.EVT_BUTTON, self.on_add_mirror)
        btn_sizer.Add(add_btn, 0, wx.ALL, 10)
        
        delete_btn = wx.Button(panel, label="删除")
        delete_btn.Bind(wx.EVT_BUTTON, self.on_delete_mirror)
        btn_sizer.Add(delete_btn, 0, wx.ALL, 10)
        
        vbox.Add(btn_sizer, 0, wx.ALIGN_LEFT)
        
        # 添加当前默认镜像源信息
        self.default_mirror_info = wx.StaticText(panel, label="当前默认镜像源: 清华源")
        vbox.Add(self.default_mirror_info, 0, wx.ALL, 10)
        
        # 添加关闭按钮
        close_btn = wx.Button(panel, label="关闭")
        close_btn.Bind(wx.EVT_BUTTON, self.on_close)
        vbox.Add(close_btn, 0, wx.ALL | wx.ALIGN_RIGHT, 10)
        
        panel.SetSizer(vbox)
        self.Center()
        
        # 初始化镜像源列表
        self.on_refresh_mirrors(None)
    
    def on_refresh_mirrors(self, event):
        """刷新镜像源列表"""
        self.mirror_list.DeleteAllItems()
        
        # 添加内置镜像源
        mirror_names = {
            "1": "清华源",
            "2": "中科大源",
            "3": "阿里云源",
            "4": "豆瓣源",
            "5": "官方源"
        }
        
        for key, url in self.parent.mirror_sources.items():
            name = mirror_names.get(key, f"镜像源{key}")
            index = self.mirror_list.InsertItem(self.mirror_list.GetItemCount(), key)
            self.mirror_list.SetItem(index, 1, name)
            self.mirror_list.SetItem(index, 2, url)
        
        # 添加自定义镜像源
        for key, url in self.parent.custom_mirrors.items():
            index = self.mirror_list.InsertItem(self.mirror_list.GetItemCount(), key)
            self.mirror_list.SetItem(index, 1, f"自定义{key}")
            self.mirror_list.SetItem(index, 2, url)
        
        # 更新默认镜像源信息
        default_key = self.parent.default_mirror
        if default_key in mirror_names:
            default_name = mirror_names[default_key]
        elif default_key in self.parent.custom_mirrors:
            default_name = f"自定义{default_key}"
        else:
            default_name = "未知"
        
        self.default_mirror_info.SetLabel(f"当前默认镜像源: {default_name}")
    
    def on_set_default(self, event):
        """设置默认镜像源"""
        selected = self.mirror_list.GetFirstSelected()
        if selected == -1:
            self.show_message("提示", "请选择一个镜像源", wx.ICON_INFORMATION)
            return
        
        key = self.mirror_list.GetItemText(selected, 0)
        self.parent.default_mirror = key
        
        # 更新默认镜像源信息
        mirror_names = {
            "1": "清华源",
            "2": "中科大源",
            "3": "阿里云源",
            "4": "豆瓣源",
            "5": "官方源"
        }
        
        if key in mirror_names:
            default_name = mirror_names[key]
        elif key in self.parent.custom_mirrors:
            default_name = f"自定义{key}"
        else:
            default_name = "未知"
        
        self.default_mirror_info.SetLabel(f"当前默认镜像源: {default_name}")
        self.show_message("成功", f"默认镜像源已设置为: {default_name}", wx.ICON_INFORMATION)
    
    def on_add_mirror(self, event):
        """添加自定义镜像源"""
        dlg = wx.TextEntryDialog(self, "请输入镜像源URL:", "添加镜像源")
        if dlg.ShowModal() == wx.ID_OK:
            url = dlg.GetValue().strip()
            if url:
                # 生成新的自定义镜像源键
                import re
                # 提取域名作为名称
                match = re.search(r'https?://([^/]+)', url)
                if match:
                    name = match.group(1)
                else:
                    name = "custom"
                
                # 生成唯一键
                key = str(len(self.parent.custom_mirrors) + 6)  # 从6开始，避免与内置镜像源冲突
                
                # 添加到自定义镜像源
                self.parent.custom_mirrors[key] = url
                
                # 刷新列表
                self.on_refresh_mirrors(None)
                self.show_message("成功", "镜像源添加成功", wx.ICON_INFORMATION)
        dlg.Destroy()
    
    def on_delete_mirror(self, event):
        """删除自定义镜像源"""
        selected = self.mirror_list.GetFirstSelected()
        if selected == -1:
            self.show_message("提示", "请选择一个镜像源", wx.ICON_INFORMATION)
            return
        
        key = self.mirror_list.GetItemText(selected, 0)
        
        # 检查是否是自定义镜像源
        if key not in self.parent.custom_mirrors:
            self.show_message("提示", "只能删除自定义镜像源", wx.ICON_INFORMATION)
            return
        
        # 确认删除
        dlg = wx.MessageDialog(self, "确定要删除这个镜像源吗？", "确认删除", wx.YES_NO | wx.ICON_QUESTION)
        if dlg.ShowModal() == wx.ID_YES:
            del self.parent.custom_mirrors[key]
            self.on_refresh_mirrors(None)
            self.show_message("成功", "镜像源删除成功", wx.ICON_INFORMATION)
        dlg.Destroy()
    
    def show_message(self, title, message, style=wx.ICON_INFORMATION):
        """显示消息对话框"""
        dlg = wx.MessageDialog(self, message, title, style)
        dlg.ShowModal()
        dlg.Destroy()
    
    def on_close(self, event):
        """关闭对话框"""
        self.Close()

class BatchPackageManagerDialog(wx.Dialog):
    def __init__(self, parent):
        super().__init__(parent, title="批量包管理", size=(600, 400))
        self.parent = parent
        
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        # 添加选项卡
        notebook = wx.Notebook(panel)
        
        # 批量更新选项卡
        update_tab = wx.Panel(notebook)
        self.create_batch_update_tab(update_tab)
        notebook.AddPage(update_tab, "批量更新")
        
        # 批量卸载选项卡
        uninstall_tab = wx.Panel(notebook)
        self.create_batch_uninstall_tab(uninstall_tab)
        notebook.AddPage(uninstall_tab, "批量卸载")
        
        # 导出包列表选项卡
        export_tab = wx.Panel(notebook)
        self.create_export_tab(export_tab)
        notebook.AddPage(export_tab, "导出包列表")
        
        # 从文件安装选项卡
        install_tab = wx.Panel(notebook)
        self.create_install_from_file_tab(install_tab)
        notebook.AddPage(install_tab, "从文件安装")
        
        vbox.Add(notebook, 1, wx.ALL | wx.EXPAND, 10)
        
        # 添加关闭按钮
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        close_btn = wx.Button(panel, label="关闭")
        close_btn.Bind(wx.EVT_BUTTON, self.on_close)
        btn_sizer.Add(close_btn, 0, wx.ALL, 10)
        
        vbox.Add(btn_sizer, 0, wx.ALIGN_RIGHT)
        
        panel.SetSizer(vbox)
        self.Center()
    
    def create_batch_update_tab(self, panel):
        """创建批量更新选项卡"""
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        # 添加检查按钮
        check_btn = wx.Button(panel, label="检查可更新的包")
        check_btn.Bind(wx.EVT_BUTTON, self.on_check_updatable)
        vbox.Add(check_btn, 0, wx.ALL, 10)
        
        # 添加可更新包列表
        self.updatable_list = wx.ListCtrl(panel, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        self.updatable_list.InsertColumn(0, "包名", width=200)
        self.updatable_list.InsertColumn(1, "当前版本", width=100)
        self.updatable_list.InsertColumn(2, "最新版本", width=100)
        vbox.Add(self.updatable_list, 1, wx.ALL | wx.EXPAND, 10)
        
        # 添加更新按钮
        update_btn = wx.Button(panel, label="更新选中的包")
        update_btn.Bind(wx.EVT_BUTTON, self.on_update_selected)
        vbox.Add(update_btn, 0, wx.ALL, 10)
        
        # 添加更新全部按钮
        update_all_btn = wx.Button(panel, label="更新所有包")
        update_all_btn.Bind(wx.EVT_BUTTON, self.on_update_all)
        vbox.Add(update_all_btn, 0, wx.ALL, 10)
        
        # 添加结果文本框
        self.update_result = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY)
        vbox.Add(self.update_result, 1, wx.ALL | wx.EXPAND, 10)
        
        panel.SetSizer(vbox)
    
    def create_batch_uninstall_tab(self, panel):
        """创建批量卸载选项卡"""
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        # 刷新包列表按钮
        refresh_btn = wx.Button(panel, label="刷新包列表")
        refresh_btn.Bind(wx.EVT_BUTTON, self.on_refresh_batch_packages)
        vbox.Add(refresh_btn, 0, wx.ALL, 10)
        
        # 包列表
        package_sizer = wx.BoxSizer(wx.HORIZONTAL)
        package_label = wx.StaticText(panel, label="已安装的包:")
        package_sizer.Add(package_label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 10)
        
        # 创建包列表控件（支持多选）
        self.batch_package_list = wx.ListBox(panel, size=(400, 200), style=wx.LB_EXTENDED)
        package_sizer.Add(self.batch_package_list, 1, wx.ALL | wx.EXPAND, 10)
        vbox.Add(package_sizer, 0, wx.EXPAND)
        
        # 添加卸载按钮
        uninstall_btn = wx.Button(panel, label="批量卸载选中的包")
        uninstall_btn.Bind(wx.EVT_BUTTON, self.on_batch_uninstall)
        vbox.Add(uninstall_btn, 0, wx.ALL, 10)
        
        # 添加结果文本框
        self.uninstall_result = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY)
        vbox.Add(self.uninstall_result, 1, wx.ALL | wx.EXPAND, 10)
        
        panel.SetSizer(vbox)
        
        # 初始加载包列表
        self.on_refresh_batch_packages(None)
    
    def on_refresh_batch_packages(self, event):
        """刷新批量卸载选项卡中的包列表"""
        import subprocess
        import threading
        
        self.batch_package_list.Clear()
        
        # 显示加载中
        self.parent.status_bar.SetStatusText("正在获取已安装包...")
        
        # 在后台线程中执行
        def refresh_packages():
            try:
                # 获取已安装的包
                result = subprocess.run([sys.executable, "-m", "pip", "list", "--format=freeze"], 
                                      capture_output=True, text=True, timeout=30)
                
                packages = []
                for line in result.stdout.strip().split('\n'):
                    if line:
                        package_info = line.split('==')
                        if len(package_info) >= 2:
                            packages.append(f"{package_info[0]}=={package_info[1]}")
                
                # 更新UI
                wx.CallAfter(self.batch_package_list.Append, packages)
                wx.CallAfter(self.parent.status_bar.SetStatusText, "已安装包列表刷新完成")
            except Exception as e:
                wx.CallAfter(self.parent.status_bar.SetStatusText, "获取已安装包失败")
                wx.CallAfter(self.show_message, "错误", f"获取已安装包失败: {str(e)}", wx.ICON_ERROR)
        
        thread = threading.Thread(target=refresh_packages)
        thread.daemon = True
        thread.start()
    
    def create_export_tab(self, panel):
        """创建导出包列表选项卡"""
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        # 添加导出按钮
        export_btn = wx.Button(panel, label="导出包列表")
        export_btn.Bind(wx.EVT_BUTTON, self.on_export_packages)
        vbox.Add(export_btn, 0, wx.ALL, 10)
        
        # 添加结果文本框
        self.export_result = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY)
        vbox.Add(self.export_result, 1, wx.ALL | wx.EXPAND, 10)
        
        panel.SetSizer(vbox)
    
    def create_install_from_file_tab(self, panel):
        """创建从文件安装选项卡"""
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        # 添加文件选择
        file_sizer = wx.BoxSizer(wx.HORIZONTAL)
        file_label = wx.StaticText(panel, label="文件路径:")
        file_sizer.Add(file_label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 10)
        
        self.file_path_text = wx.TextCtrl(panel, size=(300, -1))
        file_sizer.Add(self.file_path_text, 1, wx.ALL, 10)
        
        browse_btn = wx.Button(panel, label="浏览")
        browse_btn.Bind(wx.EVT_BUTTON, self.on_browse_file)
        file_sizer.Add(browse_btn, 0, wx.ALL, 10)
        
        vbox.Add(file_sizer, 0, wx.ALL | wx.EXPAND, 10)
        
        # 添加安装按钮
        install_btn = wx.Button(panel, label="从文件安装")
        install_btn.Bind(wx.EVT_BUTTON, self.on_install_from_file)
        vbox.Add(install_btn, 0, wx.ALL, 10)
        
        # 添加结果文本框
        self.install_from_file_result = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY)
        vbox.Add(self.install_from_file_result, 1, wx.ALL | wx.EXPAND, 10)
        
        panel.SetSizer(vbox)
    
    def on_check_updatable(self, event):
        """检查可更新的包"""
        self.updatable_list.DeleteAllItems()
        self.parent.status_bar.SetStatusText("正在检查可更新的包...")
        
        # 在后台线程中检查可更新的包
        def check_updatable():
            try:
                import subprocess
                cmd = [sys.executable, "-m", "pip", "list", "--outdated"]
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.returncode == 0:
                    lines = result.stdout.strip().split('\n')
                    for i, line in enumerate(lines[2:]):  # 跳过表头
                        if line.strip():
                            parts = line.split()
                            if len(parts) >= 3:
                                name = parts[0]
                                current_version = parts[1]
                                latest_version = parts[2]
                                self.updatable_list.InsertItem(i, name)
                                self.updatable_list.SetItem(i, 1, current_version)
                                self.updatable_list.SetItem(i, 2, latest_version)
                    
                    wx.CallAfter(self.parent.status_bar.SetStatusText, f"找到 {len(lines) - 2} 个可更新的包")
                else:
                    wx.CallAfter(self.parent.status_bar.SetStatusText, "检查可更新的包失败")
                    wx.CallAfter(self.show_message, "错误", f"检查可更新的包失败: {result.stderr}", wx.ICON_ERROR)
            except Exception as e:
                wx.CallAfter(self.parent.status_bar.SetStatusText, "检查可更新的包失败")
                wx.CallAfter(self.show_message, "错误", f"检查可更新的包失败: {str(e)}", wx.ICON_ERROR)
        
        thread = threading.Thread(target=check_updatable)
        thread.daemon = True
        thread.start()
    
    def on_update_selected(self, event):
        """更新选中的包"""
        selected = self.updatable_list.GetFirstSelected()
        if selected == -1:
            self.show_message("提示", "请选择一个包", wx.ICON_INFORMATION)
            return
        
        package_name = self.updatable_list.GetItemText(selected, 0)
        self.update_package(package_name)
    
    def on_update_all(self, event):
        """更新所有包"""
        count = self.updatable_list.GetItemCount()
        if count == 0:
            self.show_message("提示", "没有可更新的包", wx.ICON_INFORMATION)
            return
        
        # 确认更新
        dlg = wx.MessageDialog(self, f"确定要更新所有 {count} 个包吗？", "确认更新", wx.YES_NO | wx.ICON_QUESTION)
        if dlg.ShowModal() == wx.ID_YES:
            # 创建进度条对话框
            progress_dlg = ProgressDialog(self, "批量更新包", count)
            progress_dlg.Show()
            
            # 逐个更新包
            def update_all_packages():
                success_count = 0
                fail_count = 0
                
                for i in range(count):
                    package_name = self.updatable_list.GetItemText(i, 0)
                    progress_dlg.update(i, f"正在更新 {package_name} ({i+1}/{count})...")
                    
                    # 更新包
                    try:
                        import subprocess
                        cmd = [sys.executable, "-m", "pip", "install", "--upgrade", package_name, "-i", "https://pypi.tuna.tsinghua.edu.cn/simple"]
                        result = subprocess.run(cmd, capture_output=True, text=True)
                        
                        if result.returncode == 0:
                            success_count += 1
                        else:
                            fail_count += 1
                    except Exception:
                        fail_count += 1
                
                # 完成更新
                progress_dlg.update(count, "更新完成")
                time.sleep(0.5)
                progress_dlg.close()
                
                # 显示结果
                wx.CallAfter(self.show_message, "完成", f"批量更新完成：成功 {success_count}，失败 {fail_count}", wx.ICON_INFORMATION)
                wx.CallAfter(self.parent.status_bar.SetStatusText, f"批量更新完成：成功 {success_count}，失败 {fail_count}")
            
            # 在后台线程中执行
            thread = threading.Thread(target=update_all_packages)
            thread.daemon = True
            thread.start()
        dlg.Destroy()
    
    def update_package(self, package_name):
        """更新单个包"""
        self.parent.status_bar.SetStatusText(f"正在更新包 {package_name}...")
        
        # 在后台线程中更新包
        def update_package_thread():
            try:
                import subprocess
                cmd = [sys.executable, "-m", "pip", "install", "--upgrade", package_name, "-i", "https://pypi.tuna.tsinghua.edu.cn/simple"]
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.returncode == 0:
                    wx.CallAfter(self.parent.status_bar.SetStatusText, f"包 {package_name} 更新成功")
                    wx.CallAfter(self.show_message, "成功", f"包 {package_name} 更新成功", wx.ICON_INFORMATION)
                else:
                    wx.CallAfter(self.parent.status_bar.SetStatusText, f"包 {package_name} 更新失败")
                    wx.CallAfter(self.show_message, "错误", f"包 {package_name} 更新失败", wx.ICON_ERROR)
            except Exception as e:
                wx.CallAfter(self.parent.status_bar.SetStatusText, f"包 {package_name} 更新失败")
                wx.CallAfter(self.show_message, "错误", f"包 {package_name} 更新失败: {str(e)}", wx.ICON_ERROR)
        
        thread = threading.Thread(target=update_package_thread)
        thread.daemon = True
        thread.start()
    
    def on_batch_uninstall(self, event):
        """批量卸载包"""
        # 从包列表中获取选中的包
        selected_indices = self.batch_package_list.GetSelections()
        if not selected_indices:
            self.show_message("提示", "请选择要卸载的包", wx.ICON_INFORMATION)
            return
        
        # 获取选中的包名（去掉版本号）
        packages = []
        for index in selected_indices:
            selected_package = self.batch_package_list.GetString(index)
            package_name = selected_package.split('==')[0]
            packages.append(package_name)
        
        if not packages:
            self.show_message("提示", "请选择有效的包", wx.ICON_INFORMATION)
            return
        
        # 创建进度条对话框
        progress_dlg = ProgressDialog(self, "批量卸载包", len(packages))
        progress_dlg.Show()
        
        # 在后台线程中批量卸载包
        def uninstall_packages():
            try:
                import subprocess
                output = ""
                success_count = 0
                fail_count = 0
                
                for i, package in enumerate(packages):
                    progress_dlg.update(i, f"正在卸载 {package} ({i+1}/{len(packages)})...")
                    
                    cmd = [sys.executable, "-m", "pip", "uninstall", "-y", package]
                    result = subprocess.run(cmd, capture_output=True, text=True)
                    
                    output += f"\n=== 卸载包 {package} ===\n"
                    output += f"命令: {' '.join(cmd)}\n"
                    output += f"输出:\n{result.stdout}\n"
                    if result.stderr:
                        output += f"错误:\n{result.stderr}\n"
                    
                    if result.returncode == 0:
                        success_count += 1
                    else:
                        fail_count += 1
                
                output += f"\n=== 卸载结果 ===\n"
                output += f"成功: {success_count}\n"
                output += f"失败: {fail_count}\n"
                
                # 完成卸载
                progress_dlg.update(len(packages), "卸载完成")
                time.sleep(0.5)
                progress_dlg.close()
                
                # 刷新包列表
                wx.CallAfter(self.on_refresh_batch_packages, None)
                wx.CallAfter(self.uninstall_result.SetValue, output)
                wx.CallAfter(self.parent.status_bar.SetStatusText, f"卸载完成: 成功 {success_count}, 失败 {fail_count}")
                wx.CallAfter(self.show_message, "完成", f"卸载完成: 成功 {success_count}, 失败 {fail_count}", wx.ICON_INFORMATION)
            except Exception as e:
                progress_dlg.close()
                wx.CallAfter(self.uninstall_result.SetValue, f"卸载失败: {str(e)}")
                wx.CallAfter(self.parent.status_bar.SetStatusText, "批量卸载失败")
                wx.CallAfter(self.show_message, "错误", f"批量卸载失败: {str(e)}", wx.ICON_ERROR)
        
        thread = threading.Thread(target=uninstall_packages)
        thread.daemon = True
        thread.start()
    
    def on_export_packages(self, event):
        """导出包列表"""
        self.parent.status_bar.SetStatusText("正在导出包列表...")
        
        # 在后台线程中导出包列表
        def export_packages():
            try:
                import subprocess
                cmd = [sys.executable, "-m", "pip", "list", "--format=freeze"]
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.returncode == 0:
                    # 保存到requirements.txt文件
                    with open("requirements.txt", "w", encoding="utf-8") as f:
                        f.write(result.stdout)
                    
                    newline = '\n'
                    output = f"导出成功！{newline}"
                    output += f"导出到文件: {os.path.abspath('requirements.txt')}{newline}"
                    output += f"共导出 {len(result.stdout.strip().split(newline))} 个包{newline}{newline}"
                    output += "前10个包:\n"
                    packages = result.stdout.strip().split(newline)[:10]
                    output += '\n'.join(packages)
                    
                    wx.CallAfter(self.export_result.SetValue, output)
                    wx.CallAfter(self.parent.status_bar.SetStatusText, "包列表导出成功")
                    wx.CallAfter(self.show_message, "成功", "包列表导出成功", wx.ICON_INFORMATION)
                else:
                    wx.CallAfter(self.export_result.SetValue, f"导出失败: {result.stderr}")
                    wx.CallAfter(self.parent.status_bar.SetStatusText, "包列表导出失败")
                    wx.CallAfter(self.show_message, "错误", "包列表导出失败", wx.ICON_ERROR)
            except Exception as e:
                wx.CallAfter(self.export_result.SetValue, f"导出失败: {str(e)}")
                wx.CallAfter(self.parent.status_bar.SetStatusText, "包列表导出失败")
                wx.CallAfter(self.show_message, "错误", f"包列表导出失败: {str(e)}", wx.ICON_ERROR)
        
        thread = threading.Thread(target=export_packages)
        thread.daemon = True
        thread.start()
    
    def on_browse_file(self, event):
        """浏览文件"""
        dlg = wx.FileDialog(self, "选择requirements.txt文件", wildcard="Text files (*.txt)|*.txt|All files (*.*)|*.*")
        if dlg.ShowModal() == wx.ID_OK:
            self.file_path_text.SetValue(dlg.GetPath())
        dlg.Destroy()
    
    def on_install_from_file(self, event):
        """从文件安装"""
        file_path = self.file_path_text.GetValue().strip()
        if not file_path:
            self.show_message("提示", "请选择文件", wx.ICON_INFORMATION)
            return
        
        if not os.path.exists(file_path):
            self.show_message("提示", "文件不存在", wx.ICON_INFORMATION)
            return
        
        # 计算文件中的包数量
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                # 过滤空行和注释行
                packages = [line.strip() for line in lines if line.strip() and not line.strip().startswith('#')]
                package_count = len(packages)
        except Exception:
            package_count = 100  # 默认值
        
        # 创建进度条对话框
        progress_dlg = ProgressDialog(self, "从文件安装包", package_count)
        progress_dlg.Show()
        
        # 在后台线程中从文件安装
        def install_from_file():
            try:
                import subprocess
                import re
                
                # 执行安装命令
                cmd = [sys.executable, "-m", "pip", "install", "-r", file_path, "-i", "https://pypi.tuna.tsinghua.edu.cn/simple"]
                
                # 使用Popen实时获取输出
                process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                
                output = f"命令: {' '.join(cmd)}\n\n"
                output += "输出:\n"
                
                # 实时读取输出
                installed_count = 0
                for line in process.stdout:
                    output += line
                    # 检测安装成功的包
                    if "Successfully installed" in line:
                        # 提取安装的包名数量
                        match = re.search(r"Successfully installed (.*)", line)
                        if match:
                            installed_packages = match.group(1).split()
                            installed_count += len([p for p in installed_packages if '==' in p])
                            progress_dlg.update(min(installed_count, package_count), f"已安装 {installed_count} 个包...")
                
                # 读取错误输出
                stderr = process.stderr.read()
                if stderr:
                    output += "\n错误:\n"
                    output += stderr
                
                # 等待进程结束
                process.wait()
                
                # 完成安装
                progress_dlg.update(package_count, "安装完成")
                time.sleep(0.5)
                progress_dlg.close()
                
                wx.CallAfter(self.install_from_file_result.SetValue, output)
                
                if process.returncode == 0:
                    wx.CallAfter(self.parent.status_bar.SetStatusText, "从文件安装包成功")
                    wx.CallAfter(self.show_message, "成功", "从文件安装包成功", wx.ICON_INFORMATION)
                else:
                    wx.CallAfter(self.parent.status_bar.SetStatusText, "从文件安装包失败")
                    wx.CallAfter(self.show_message, "错误", "从文件安装包失败", wx.ICON_ERROR)
            except Exception as e:
                progress_dlg.close()
                wx.CallAfter(self.install_from_file_result.SetValue, f"安装失败: {str(e)}")
                wx.CallAfter(self.parent.status_bar.SetStatusText, "从文件安装包失败")
                wx.CallAfter(self.show_message, "错误", f"从文件安装包失败: {str(e)}", wx.ICON_ERROR)
        
        thread = threading.Thread(target=install_from_file)
        thread.daemon = True
        thread.start()
    
    def show_message(self, title, message, style=wx.ICON_INFORMATION):
        """显示消息对话框"""
        dlg = wx.MessageDialog(self, message, title, style)
        dlg.ShowModal()
        dlg.Destroy()
    
    def on_close(self, event):
        """关闭对话框"""
        self.Close()

class PythonVersionManagerDialog(wx.Dialog):
    def __init__(self, parent):
        super().__init__(parent, title="Python版本管理", size=(600, 400))
        self.parent = parent
        
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        # 添加选项卡
        notebook = wx.Notebook(panel)
        
        # 可用版本选项卡
        available_tab = wx.Panel(notebook)
        self.create_available_versions_tab(available_tab)
        notebook.AddPage(available_tab, "可用版本")
        
        # 已安装版本选项卡
        installed_tab = wx.Panel(notebook)
        self.create_installed_versions_tab(installed_tab)
        notebook.AddPage(installed_tab, "已安装版本")
        
        vbox.Add(notebook, 1, wx.ALL | wx.EXPAND, 10)
        
        # 添加关闭按钮
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        close_btn = wx.Button(panel, label="关闭")
        close_btn.Bind(wx.EVT_BUTTON, self.on_close)
        btn_sizer.Add(close_btn, 0, wx.ALL, 10)
        
        vbox.Add(btn_sizer, 0, wx.ALIGN_RIGHT)
        
        panel.SetSizer(vbox)
        self.Center()
    
    def create_available_versions_tab(self, panel):
        """创建可用版本选项卡"""
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        # 添加刷新按钮
        refresh_btn = wx.Button(panel, label="获取可用版本")
        refresh_btn.Bind(wx.EVT_BUTTON, self.on_refresh_available)
        vbox.Add(refresh_btn, 0, wx.ALL, 10)
        
        # 添加版本列表
        self.available_list = wx.ListCtrl(panel, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        self.available_list.InsertColumn(0, "类型", width=100)
        self.available_list.InsertColumn(1, "版本", width=150)
        self.available_list.InsertColumn(2, "发布日期", width=150)
        vbox.Add(self.available_list, 1, wx.ALL | wx.EXPAND, 10)
        
        # 添加安装按钮
        install_btn = wx.Button(panel, label="安装选中的版本")
        install_btn.Bind(wx.EVT_BUTTON, self.on_install_version)
        vbox.Add(install_btn, 0, wx.ALL, 10)
        
        panel.SetSizer(vbox)
    
    def create_installed_versions_tab(self, panel):
        """创建已安装版本选项卡"""
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        # 添加刷新按钮
        refresh_btn = wx.Button(panel, label="检查已安装版本")
        refresh_btn.Bind(wx.EVT_BUTTON, self.on_refresh_installed)
        vbox.Add(refresh_btn, 0, wx.ALL, 10)
        
        # 添加版本列表
        self.installed_list = wx.ListCtrl(panel, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        self.installed_list.InsertColumn(0, "版本", width=150)
        self.installed_list.InsertColumn(1, "路径", width=400)
        vbox.Add(self.installed_list, 1, wx.ALL | wx.EXPAND, 10)
        
        panel.SetSizer(vbox)
    
    def on_refresh_available(self, event):
        """获取可用版本"""
        self.available_list.DeleteAllItems()
        self.parent.status_bar.SetStatusText("正在获取可用Python版本...")
        
        # 在后台线程中获取可用版本
        def get_available_versions():
            try:
                versions = self.parent.version_fetcher.get_available_versions()
                
                if versions:
                    for i, version_info in enumerate(versions):
                        self.available_list.InsertItem(i, version_info['type'])
                        self.available_list.SetItem(i, 1, version_info['version'])
                        self.available_list.SetItem(i, 2, version_info['date'])
                    
                    wx.CallAfter(self.parent.status_bar.SetStatusText, f"找到 {len(versions)} 个可用版本")
                else:
                    wx.CallAfter(self.parent.status_bar.SetStatusText, "获取可用版本失败")
                    wx.CallAfter(self.show_message, "错误", "获取可用版本失败", wx.ICON_ERROR)
            except Exception as e:
                wx.CallAfter(self.parent.status_bar.SetStatusText, "获取可用版本失败")
                wx.CallAfter(self.show_message, "错误", f"获取可用版本失败: {str(e)}", wx.ICON_ERROR)
        
        thread = threading.Thread(target=get_available_versions)
        thread.daemon = True
        thread.start()
    
    def on_install_version(self, event):
        """安装选中的版本"""
        selected = self.available_list.GetFirstSelected()
        if selected == -1:
            self.show_message("提示", "请选择一个版本", wx.ICON_INFORMATION)
            return
        
        version = self.available_list.GetItemText(selected, 1)
        self.parent.status_bar.SetStatusText(f"正在安装Python {version}...")
        
        # 在后台线程中安装版本
        def install_version():
            try:
                # 调用installer模块安装Python
                result = self.parent.installer.install_python(version)
                
                if result:
                    wx.CallAfter(self.parent.status_bar.SetStatusText, f"Python {version} 安装成功")
                    wx.CallAfter(self.show_message, "成功", f"Python {version} 安装成功", wx.ICON_INFORMATION)
                else:
                    wx.CallAfter(self.parent.status_bar.SetStatusText, f"Python {version} 安装失败")
                    wx.CallAfter(self.show_message, "错误", f"Python {version} 安装失败", wx.ICON_ERROR)
            except Exception as e:
                wx.CallAfter(self.parent.status_bar.SetStatusText, f"Python {version} 安装失败")
                wx.CallAfter(self.show_message, "错误", f"Python {version} 安装失败: {str(e)}", wx.ICON_ERROR)
        
        thread = threading.Thread(target=install_version)
        thread.daemon = True
        thread.start()
    
    def on_refresh_installed(self, event):
        """检查已安装版本"""
        self.installed_list.DeleteAllItems()
        self.parent.status_bar.SetStatusText("正在检查已安装的Python版本...")
        
        # 在后台线程中检查已安装版本
        def check_installed_versions():
            try:
                # 检查系统中已安装的Python版本
                import subprocess
                import os
                
                # 检查PATH中的Python
                python_versions = []
                
                # 检查常见的Python安装路径
                common_paths = [
                    r"C:\Python",
                    r"C:\Program Files\Python",
                    r"C:\Program Files (x86)\Python",
                    os.path.expanduser("~\AppData\Local\Programs\Python")
                ]
                
                for base_path in common_paths:
                    if os.path.exists(base_path):
                        for item in os.listdir(base_path):
                            item_path = os.path.join(base_path, item)
                            if os.path.isdir(item_path):
                                python_exe = os.path.join(item_path, "python.exe")
                                if os.path.exists(python_exe):
                                    # 获取版本号
                                    try:
                                        result = subprocess.run([python_exe, "--version"], capture_output=True, text=True)
                                        if result.returncode == 0:
                                            version = result.stdout.strip().split(" ")[1]
                                            python_versions.append((version, item_path))
                                    except:
                                        pass
                
                # 检查当前Python
                current_version = sys.version.split()[0]
                current_path = sys.executable
                python_versions.append((current_version, os.path.dirname(current_path)))
                
                # 去重
                python_versions = list(set(python_versions))
                
                # 显示结果
                for i, (version, path) in enumerate(python_versions):
                    self.installed_list.InsertItem(i, version)
                    self.installed_list.SetItem(i, 1, path)
                
                wx.CallAfter(self.parent.status_bar.SetStatusText, f"找到 {len(python_versions)} 个已安装版本")
            except Exception as e:
                wx.CallAfter(self.parent.status_bar.SetStatusText, "检查已安装版本失败")
                wx.CallAfter(self.show_message, "错误", f"检查已安装版本失败: {str(e)}", wx.ICON_ERROR)
        
        thread = threading.Thread(target=check_installed_versions)
        thread.daemon = True
        thread.start()
    
    def show_message(self, title, message, style=wx.ICON_INFORMATION):
        """显示消息对话框"""
        dlg = wx.MessageDialog(self, message, title, style)
        dlg.ShowModal()
        dlg.Destroy()
    
    def on_close(self, event):
        """关闭对话框"""
        self.Close()

class UpdateCheckerDialog(wx.Dialog):
    def __init__(self, parent):
        super().__init__(parent, title="检查更新", size=(600, 400))
        self.parent = parent
        
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        # 添加检查按钮
        check_btn = wx.Button(panel, label="检查更新")
        check_btn.Bind(wx.EVT_BUTTON, self.on_check_update)
        vbox.Add(check_btn, 0, wx.ALL, 10)
        
        # 添加结果文本框
        self.result_text = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY)
        vbox.Add(self.result_text, 1, wx.ALL | wx.EXPAND, 10)
        
        # 添加关闭按钮
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        close_btn = wx.Button(panel, label="关闭")
        close_btn.Bind(wx.EVT_BUTTON, self.on_close)
        btn_sizer.Add(close_btn, 0, wx.ALL, 10)
        
        vbox.Add(btn_sizer, 0, wx.ALIGN_RIGHT)
        
        panel.SetSizer(vbox)
        self.Center()
    
    def on_check_update(self, event):
        """检查更新"""
        self.parent.status_bar.SetStatusText("正在检查更新...")
        
        # 在后台线程中检查更新
        def check_update():
            try:
                import requests
                import json
                
                # 获取当前版本
                current_version = "1.3.0"
                
                # 从GitHub API获取仓库信息
                repo_url = "https://api.github.com/repos/zhangleyan0413/PyPi-Manager"
                response = requests.get(repo_url, timeout=10)
                
                if response.status_code == 200:
                    repo_data = response.json()
                    
                    # 获取默认分支的最新提交
                    default_branch = repo_data.get("default_branch", "main")
                    branch_url = f"https://api.github.com/repos/zhangleyan0413/PyPi-Manager/branches/{default_branch}"
                    branch_response = requests.get(branch_url, timeout=10)
                    
                    if branch_response.status_code == 200:
                        branch_data = branch_response.json()
                        latest_commit_sha = branch_data.get("commit", {}).get("sha", "")[:7]  # 获取提交SHA的前7位
                        latest_commit_date = branch_data.get("commit", {}).get("commit", {}).get("author", {}).get("date", "")
                        
                        output = "检查更新结果:\n"
                        output += f"当前版本: {current_version}\n"
                        output += f"默认分支: {default_branch}\n"
                        output += f"最新提交: {latest_commit_sha}\n"
                        output += f"提交时间: {latest_commit_date}\n"
                        
                        # 尝试从仓库中获取版本号
                        # 检查README.md文件中的版本号
                        readme_url = f"https://api.github.com/repos/zhangleyan0413/PyPi-Manager/contents/README.md"
                        readme_response = requests.get(readme_url, timeout=10)
                        
                        repo_version = ""
                        if readme_response.status_code == 200:
                            readme_data = readme_response.json()
                            import base64
                            try:
                                readme_content = base64.b64decode(readme_data.get("content", "")).decode('utf-8')
                                # 查找版本号
                                import re
                                # 尝试多种可能的格式
                                version_patterns = [
                                    r'Version: ([\d.]+)',  # 英文格式
                                    r'version: ([\d.]+)',  # 小写英文格式
                                    r'v([\d.]+)',  # 仅版本号前缀
                                    r'([\d.]+)'  # 仅数字格式
                                ]
                                
                                for pattern in version_patterns:
                                    version_match = re.search(pattern, readme_content)
                                    if version_match:
                                        repo_version = version_match.group(1)
                                        break
                            except Exception:
                                pass
                        
                        # 比较版本号
                        if repo_version:
                            output += f"仓库版本: {repo_version}\n"
                            
                            # 比较版本号
                            def compare_versions(v1, v2):
                                v1_parts = list(map(int, v1.split(".")))
                                v2_parts = list(map(int, v2.split(".")))
                                return (v1_parts > v2_parts) - (v1_parts < v2_parts)
                            
                            comparison = compare_versions(repo_version, current_version)
                            if comparison > 0:
                                output += "\n🎉 发现新版本！\n"
                                output += "请访问GitHub仓库下载最新版本:\n"
                                output += "https://github.com/zhangleyan0413/PyPi-Manager"
                                wx.CallAfter(self.parent.status_bar.SetStatusText, "发现新版本")
                            elif comparison < 0:
                                output += "\n⚠️ 当前版本比仓库版本新，可能是开发版本\n"
                                wx.CallAfter(self.parent.status_bar.SetStatusText, "当前是开发版本")
                            else:
                                output += "\n✅ 当前已是最新版本\n"
                                wx.CallAfter(self.parent.status_bar.SetStatusText, "当前是最新版本")
                        else:
                            output += "\n无法获取仓库版本号\n"
                            output += "请访问GitHub仓库查看是否有新版本:\n"
                            output += "https://github.com/zhangleyan0413/PyPi-Manager"
                            wx.CallAfter(self.parent.status_bar.SetStatusText, "无法获取仓库版本号")
                    else:
                        output = "无法获取分支信息，请检查网络连接"
                        wx.CallAfter(self.parent.status_bar.SetStatusText, "无法获取分支信息")
                else:
                    output = "无法连接到GitHub服务器，请检查网络连接"
                    wx.CallAfter(self.parent.status_bar.SetStatusText, "无法连接到GitHub")
            except Exception as e:
                output = f"检查更新失败: {str(e)}\n"
                output += "请手动访问GitHub仓库查看是否有新版本\n"
                output += "https://github.com/zhangleyan0413/PyPi-Manager"
                wx.CallAfter(self.parent.status_bar.SetStatusText, "检查更新失败")
            
            wx.CallAfter(self.result_text.SetValue, output)
        
        thread = threading.Thread(target=check_update)
        thread.daemon = True
        thread.start()
    
    def on_close(self, event):
        """关闭对话框"""
        self.Close()

if __name__ == "__main__":
    # 创建应用程序实例
    app = wx.App()
    
    # 创建主窗口
    frame = PyPiManagerGUI()
    
    # 运行应用程序
    app.MainLoop()