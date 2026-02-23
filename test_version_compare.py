# 测试版本号比较功能
import requests
import base64
import re

# 获取当前版本
current_version = "1.1.0"
print(f"当前版本: {current_version}")

# 从GitHub API获取README.md文件
try:
    readme_url = "https://api.github.com/repos/zhangleyan0413/PyPi-Manager/contents/README.md"
    response = requests.get(readme_url, timeout=10)
    
    if response.status_code == 200:
        data = response.json()
        readme_content = base64.b64decode(data.get("content", "")).decode('utf-8')
        
        # 查找版本号
        # 尝试多种可能的格式
        version_patterns = [
            r'版本：([\d.]+)',  # 中文格式
            r'Version: ([\d.]+)',  # 英文格式
            r'version: ([\d.]+)',  # 小写英文格式
            r'v([\d.]+)',  # 仅版本号前缀
            r'([\d.]+)'  # 仅数字格式
        ]
        
        repo_version = None
        for pattern in version_patterns:
            version_match = re.search(pattern, readme_content)
            if version_match:
                repo_version = version_match.group(1)
                print(f"使用模式 '{pattern}' 找到版本号: {repo_version}")
                break
        
        if repo_version:
            print(f"仓库版本: {repo_version}")
            
            # 比较版本号
            def compare_versions(v1, v2):
                v1_parts = list(map(int, v1.split(".")))
                v2_parts = list(map(int, v2.split(".")))
                return (v1_parts > v2_parts) - (v1_parts < v2_parts)
            
            comparison = compare_versions(repo_version, current_version)
            if comparison > 0:
                print("发现新版本！")
            elif comparison < 0:
                print("当前版本比仓库版本新，可能是开发版本")
            else:
                print("当前已是最新版本")
        else:
            print("无法从README.md中找到版本号")
    else:
        print(f"无法获取README.md文件，状态码: {response.status_code}")
except Exception as e:
    print(f"发生错误: {str(e)}")