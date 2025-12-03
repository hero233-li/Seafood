import time


class CoreBanking:
    def create_customer_profile(self, name, mobile):
        print(f"  -> [外部接口] 核心系统建档: {name}")
        time.sleep(1.5)
        return "CUST_001"

    def create_loan_account(self, cust_id, amount):
        print(f"  -> [外部接口] 创建贷款账户: {amount}")
        time.sleep(1.5)
        return "LOAN_ACC_999"