class ResponseAssertion:
    """
    封装对返回结果的断言与解析逻辑
    """
    def __init__(self, result_dict: dict):
        self.raw_result = result_dict
        self.success = result_dict.get("success", False)
        self.http_status = result_dict.get("status")
        # 确保 data 是字典，如果是字符串则为空字典
        self.data = result_dict.get("data") if isinstance(result_dict.get("data"), dict) else {}

    # --- 数据提取工具 ---
    def get_value(self, key_chain: str):
        """
        安全提取深层嵌套的值
        例如: get_value("translationServices.openai.model")
        """
        keys = key_chain.split('.')
        curr = self.data
        try:
            for k in keys:
                if isinstance(curr, dict):
                    curr = curr.get(k)
                else:
                    return None
            return curr
        except Exception:
            return None

    # --- 断言方法 ---
    def assert_http_ok(self):
        """断言 HTTP 层是否成功"""
        if not self.success or self.http_status != 200:
            return False
            raise AssertionError(f"HTTP请求失败! Status: {self.http_status}, Error: {self.raw_result.get('error')}")
        print("✅ HTTP 状态检查通过")
        return self

    def assert_field_exists(self, key_chain: str):
        """断言某个字段是否存在"""
        val = self.get_value(key_chain)
        if val is None:
            raise AssertionError(f"断言失败: 关键字段 '{key_chain}' 不存在!")
        print(f"✅ 字段存在检查通过: {key_chain}")
        return self

    def assert_field_equals(self, key_chain: str, expected_value):
        """断言字段值是否等于预期"""
        actual = self.get_value(key_chain)
        if actual != expected_value:
             raise AssertionError(f"断言失败: '{key_chain}' 预期为 '{expected_value}', 实际为 '{actual}'")
        print(f"✅ 字段值匹配通过: {key_chain} == {expected_value}")
        return self

    def assert_list_contains(self, list_key: str, item_value):
        """断言列表字段中包含某项"""
        actual_list = self.get_value(list_key)
        if not isinstance(actual_list, list) or item_value not in actual_list:
             raise AssertionError(f"断言失败: 列表 '{list_key}' 不包含 '{item_value}'")
        print(f"✅ 列表包含检查通过: {list_key} 含 {item_value}")
        return self