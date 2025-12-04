import yaml
import os
import requests
import time
from typing import Optional, Dict, Any


# --- 配置加载器 (单例) ---
class ConfigLoader:
    _instance = None
    _config = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigLoader, cls).__new__(cls)
            cls._instance._load()
        return cls._instance

    def _load(self):
        # 自动定位到项目根目录下的 config/config.yaml
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        print(base_dir)
        path = os.path.join(base_dir, "config", "config.yaml")
        print(path)
        try:
            with open(path, 'r', encoding='utf-8') as f:
                self._config = yaml.safe_load(f)
        except Exception as e:
            raise RuntimeError(f"配置文件加载失败: {e}")

    def get(self, key_path: str, default=None):
        """支持 'app.base_url' 格式读取"""
        keys = key_path.split('.')
        val = self._config
        try:
            for k in keys:
                val = val[k]
            return val
        except (KeyError, TypeError):
            return default

    def get_payload_path(self, filename: str) -> str:
        """获取 payload 文件的绝对路径"""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_dir, "payloads", filename)


# --- HTTP 客户端 (含重试逻辑) ---
class HttpClient:
    def __init__(self):
        self.session = requests.Session()

    def send(self, method: str, url: str, headers: Dict = None, data: Any = None,
             json_data: Any = None, max_retries: int = 3) -> Dict:
        """
        发送请求，具备自动重试机制
        返回结构: {"success": bool, "status": int, "data": dict/str, "error": str}
        """
        for attempt in range(max_retries):
            try:
                # print(f"发起请求 ({attempt+1}/{max_retries}): {url}")
                response = self.session.request(
                    method=method, url=url, headers=headers,
                    data=data, json=json_data, timeout=15
                )

                # 基础成功判断：状态码 200 且 有返回内容
                if response.status_code == 200 and response.content:
                    try:
                        res_json = response.json()
                    except:
                        res_json = response.text

                    return {
                        "success": True,
                        "status": response.status_code,
                        "data": res_json,
                        "headers": dict(response.headers)
                    }
                else:
                    print(f"[Warning] 状态码非200或内容为空: {response.status_code}")

            except requests.RequestException as e:
                print(f"[Error] 网络请求异常: {e}")

            # 如果失败，等待后重试
            if attempt < max_retries - 1:
                time.sleep(1.5)

        # 彻底失败
        return {
            "success": False,
            "status": None,
            "data": None,
            "error": "达到最大重试次数"
        }