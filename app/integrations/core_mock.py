import time

from app.utils.service.service import ApiService

service = ApiService()

class CoreMocking:
    def create_customer_mock(self, name, mobile):
        try:
            # --- 场景 1：调用复杂配置接口 ---
            # 这一步会自动读取 payloads/complex_req.json 并封装进 bizcode
            response = service.execute_interface("get_app_config")

            # --- 场景 2：链式断言测试 ---
            # 这里演示如何针对你提供的那个巨大 JSON 返回体进行测试
            (response
             .assert_http_ok()  # 1. 判断网络和 HTTP 200
             .assert_field_exists("releaseVersion")  # 2. 判断是否有版本号
             .assert_field_equals("translationService", "bing")  # 3. 判断默认翻译服务是否为 bing
             .assert_field_equals("sensitiveConfig.maskConfig.maskPassword", True)  # 4. 深度嵌套断言
             )

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