import json
import time
from .framework import HttpClient, ConfigLoader
from .parser import ResponseAssertion


class ApiService:
    def __init__(self):
        self.client = HttpClient()
        self.config = ConfigLoader()

    def _load_payload(self, filename: str) -> dict:
        """加载 payloads 文件夹下的 JSON"""
        if not filename:
            return {}
        path = self.config.get_payload_path(filename)
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"[Error] 无法读取Payload文件: {path}")
            return {}

    def execute_interface(self, interface_key: str, dynamic_body: dict = None) -> ResponseAssertion:
        """
        统一执行接口入口
        :param interface_key: config.yaml 中的接口名 (如 'get_app_config')
        :param dynamic_body: 运行时动态参数，会合并/覆盖文件中的参数
        """
        # 1. 获取接口配置
        iface_conf = self.config.get(f"interfaces.{interface_key}")
        if not iface_conf:
            raise ValueError(f"接口 {interface_key} 未在 config.yaml 中定义")

        # 2. 准备 URL
        url = self.config.get("app.base_url") + iface_conf['path']

        # 3. 准备 Body (文件读取 + 动态合并)
        payload_data = self._load_payload(iface_conf.get('payload_file'))
        if dynamic_body:
            payload_data.update(dynamic_body)

        # 4. 构建复杂的 Request 结构 (bizcode 逻辑)
        # 你的需求：bizcode 里面是 {req_body:{}, req_head:{}} 的 JSON 字符串
        req_head = {"code": iface_conf.get('req_head_code'), "ts": str(int(time.time()))}

        biz_structure = {
            "req_body": payload_data,
            "req_head": req_head
        }
        biz_json_str = json.dumps(biz_structure, ensure_ascii=False)

        # 构造 form-data
        final_form_data = {
            "time": time.strftime("%Y-%m-%d %H:%M:%S"),
            "resage": biz_json_str,  # 你的需求：内容相同
            "bizcode": biz_json_str,  # 你的需求：内容相同
            "header": json.dumps({"token": "mock-token-123"})
        }

        # 5. 发送请求
        print(f"\n🚀 正在请求接口: [{interface_key}] - {iface_conf.get('desc', '')}")
        raw_response = self.client.send(
            method=iface_conf['method'],
            url=url,
            data=final_form_data,  # 注意：这是 form-data
            # headers={"Content-Type": "application/x-www-form-urlencoded"} # Requests 会自动处理
        )

        # 6. 返回断言对象
        return ResponseAssertion(raw_response)