import json
import os


def load_json_file(filename):
    """读取 payloads 文件夹下的 JSON 文件"""
    # 假设 payloads 文件夹在项目根目录
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_path, "payloads", filename)

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)  # 直接转成 Python 字典
    except FileNotFoundError:
        print(f"[Error] Payload file not found: {file_path}")
        return {}