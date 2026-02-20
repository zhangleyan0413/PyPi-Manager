import requests
import re

class VersionFetcher:
    def __init__(self):
        self.base_url = "https://www.python.org"
        self.ftp_url = "https://www.python.org/ftp/python/"
    
    def get_available_versions(self):
        """动态获取可用的Python版本信息"""
        try:
            print("正在从Python官网获取可用版本...")
            # 获取FTP目录列表
            response = requests.get(self.ftp_url, timeout=10)
            response.raise_for_status()
            
            # 解析HTML，提取版本目录
            versions = []
            # 使用正则表达式匹配版本目录
            version_pattern = re.compile(r'<a href="(\d+\.\d+\.\d+)/">')
            matches = version_pattern.findall(response.text)
            
            # 去重并排序
            unique_versions = list(set(matches))
            # 按版本号排序（从高到低）
            unique_versions.sort(key=lambda v: tuple(map(int, v.split('.'))), reverse=True)
            
            # 构建版本信息列表
            for version in unique_versions[:10]:  # 只取最新的10个版本
                versions.append({
                    'version': version,
                    'date': '未知',  # FTP目录没有发布日期信息
                    'type': 'stable',  # 默认为稳定版
                    'download_link': f"{self.ftp_url}{version}/"
                })
            
            # 如果FTP获取失败，使用备用静态列表
            if not versions:
                print("从FTP获取失败，使用备用版本列表")
                versions = self._get_fallback_versions()
            
            print(f"成功获取到 {len(versions)} 个可用版本")
            return versions
            
        except Exception as e:
            print(f"获取版本信息失败: {e}")
            # 使用备用静态列表
            return self._get_fallback_versions()
    
    def _get_fallback_versions(self):
        """获取备用静态版本列表"""
        return [
            {'version': '3.12.0', 'date': '2023-10-02', 'type': 'stable'},
            {'version': '3.11.0', 'date': '2022-10-24', 'type': 'stable'},
            {'version': '3.10.0', 'date': '2021-10-04', 'type': 'stable'},
            {'version': '3.9.0', 'date': '2020-10-05', 'type': 'stable'},
            {'version': '3.8.0', 'date': '2019-10-14', 'type': 'stable'},
            {'version': '3.7.0', 'date': '2018-06-27', 'type': 'stable'}
        ]
    
    def get_download_url(self, version):
        """获取指定版本的下载URL"""
        try:
            # 构建直接的下载链接
            # 注意：这里使用的是Python官网的标准下载链接格式
            # 实际使用时可能需要根据版本号调整
            version_no_dots = version.replace('.', '')
            download_url = f"https://www.python.org/ftp/python/{version}/python-{version}-amd64.exe"
            
            # 验证链接是否有效
            response = requests.head(download_url, timeout=5)
            if response.status_code == 200:
                return download_url
            else:
                # 如果64位链接无效，尝试32位
                download_url_32bit = f"https://www.python.org/ftp/python/{version}/python-{version}.exe"
                response = requests.head(download_url_32bit, timeout=5)
                if response.status_code == 200:
                    return download_url_32bit
                return None
                
        except Exception as e:
            print(f"获取下载链接失败: {e}")
            # 如果网络请求失败，返回基于版本号构建的链接
            return f"https://www.python.org/ftp/python/{version}/python-{version}-amd64.exe"

if __name__ == "__main__":
    fetcher = VersionFetcher()
    versions = fetcher.get_available_versions()
    print("可用的Python版本:")
    for v in versions:
        print(f"{v['type']}: Python {v['version']} ({v['date']})")
    
    # 测试获取下载链接
    if versions:
        test_version = versions[0]['version']
        download_url = fetcher.get_download_url(test_version)
        print(f"\n{test_version} 的下载链接: {download_url}")
