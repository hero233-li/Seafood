import time

class RiskSystem:
    def check_blacklist(self, id_card):
        print(f"  -> [外部接口] 调用风控黑名单校验: {id_card}")
        time.sleep(1) # 模拟网络耗时
        return False # 假设没在黑名单