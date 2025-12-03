from app.integrations.risk_system import RiskSystem
from app.integrations.core_banking import CoreBanking

# 实例化外部系统
risk_sys = RiskSystem()
bank_sys = CoreBanking()

def step_risk_check(data):
    # 这里可能包含5-6个风控相关的接口调用
    return risk_sys.check_blacklist(data['idCard'])

def step_create_profile(data):
    # 这里可能包含建档、OCR识别、实名认证等接口
    return bank_sys.create_customer_profile(data['name'], data['mobile'])

def step_finance_audit(data):
    # 模拟财务人工复核耗时
    bank_sys.create_loan_account("temp_id", data['amount'])