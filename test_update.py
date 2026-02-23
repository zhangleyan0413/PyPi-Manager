# 测试检查更新功能
import requests
import json

print("测试从GitHub检查更新功能...")

# 获取当前版本
current_version = "1.1.0"

# 从GitHub API获取最新版本
url = "https://api.github.com/repos/zhangleyan0413/PyPi-Manager/releases/latest"

print(f"当前版本: {current_version}")
print(f"检查URL: {url}")

try:
    response = requests.get(url, timeout=10)
    print(f"响应状态码: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"获取到的数据: {json.dumps(data, indent=2, ensure_ascii=False)}")
    else:
        print(f"请求失败，状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
except Exception as e:
    print(f"发生错误: {str(e)}")