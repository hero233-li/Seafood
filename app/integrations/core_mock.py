import time

from app.core.store import task_store
from app.utils.service.service import ApiService

service = ApiService()

class CoreMocking:
    def create_customer_mock(self, name, data):
        try:
            # --- 场景 1：调用复杂配置接口 ---
            # 这一步会自动读取 payloads/complex_req.json 并封装进 bizcode
            response = service.execute_interface("get_app_config")
            print(response.raw_result['success'])
            if not response.raw_result['success']:
                print(response.raw_result['success'])
                success = task_store.set_stop_signal(data['taskId'])

            # --- 场景 2：链式断言测试 ---
            # 这里演示如何针对你提供的那个巨大 JSON 返回体进行测试
            try:
                (response
                 .assert_http_ok()
                 .assert_field_exists("releaseVersion")
                 .assert_field_equals("translationService", "bingA")
                 .assert_field_equals("sensitiveConfig.maskConfig.maskPassword", True))
            except AssertionError as e:
                # 从异常信息中提取实际值
                error_msg = str(e)
                success = task_store.set_stop_signal(data['taskId'])
                print(error_msg)
                print(f"断言失败: {error_msg}")

            # --- 场景 3：获取数据做业务处理 ---
            # 如果断言都通过了，我们可以取值做其他事情
            version = response.get_value("releaseVersion")
            openai_models = response.get_value("translationServices.openai.models")

            print(f"\n✨ 测试成功!")
            print(f"当前版本: {version}")
            print(f"OpenAI 支持的模型: {openai_models}")
            return True

        except AssertionError as e:
            print(f"\n❌ 测试失败: {e}")
            return False
        except Exception as e:
            print(f"\n💥 系统错误: {e}")
            return False