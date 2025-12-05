# app/domains/loan/orchestrator.py
from app.core.engine import BaseWorkflowEngine
from app.domains.loan import steps
import time

from app.domains.loan.steps import step_mock_customer


class LoanOrchestrator(BaseWorkflowEngine):

    def run(self, data):
        # === 阶段 0: 创建项目 ===
        self.check_stop()
        self.update_ui_step(0)
        self.set_status_text("正在初始化项目...")  # <--- 更新状态文字
        time.sleep(1)

        # === 阶段 1: 部门初审 ===
        self.check_stop()
        step_mock_customer(data)
        self.update_ui_step(1)

        # 动作1: 风控
        self.set_status_text("正在进行大数据风控校验...")  # <--- 动态变化
        steps.step_risk_check(data)

        self.check_stop()

        # 动作2: 建档
        self.set_status_text("校验通过，正在核心系统建档...")  # <--- 动态变化
        steps.step_create_profile(data)

        # === 阶段 2: 财务复核 ===
        self.check_stop()
        self.update_ui_step(2)

        # 动作3: 财务
        self.set_status_text("等待财务人工复核...")  # <--- 动态变化
        steps.step_finance_audit(data)
        self.check_stop()

        self.set_status_text("财务复核通过，准备放款...")
        time.sleep(1.5)

        # === 阶段 3: 完成 (由基类 execute 处理) ===