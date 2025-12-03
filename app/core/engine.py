# app/core/engine.py
import time
from app.core.store import task_store


class StopTaskException(Exception):
    pass


class BaseWorkflowEngine:
    def __init__(self, task_id):
        self.task_id = task_id

    def check_stop(self):
        """检查停止信号"""
        task = task_store.get(self.task_id)
        if not task or task.get("stop_signal"):
            raise StopTaskException("用户手动停止")

    def update_ui_step(self, step_index):
        """更新进度条节点"""
        # print(f"[{self.task_id}] 更新进度 -> 节点 {step_index}")
        task_store.update_progress(self.task_id, step_index)

    # 【新增】更新详情面板里的“当前状态”文字
    def set_status_text(self, text):
        # 注意：这里的 key "当前状态" 必须和你 api.py 里初始化的 key 保持一致
        task_store.update_display_item(self.task_id, "当前状态", text)

    def execute(self, *args, **kwargs):
        """线程入口"""
        try:
            self.run(*args, **kwargs)

            self.check_stop()
            task_store.update_progress(self.task_id, 3, "SUCCESS")
            self.set_status_text("流程已完成")  # 完成时更新文字

        except StopTaskException:
            print(f"[{self.task_id}] 任务已停止")
            task_store.update_progress(self.task_id, self.current_step_index(), "STOPPED")
            self.set_status_text("用户强制终止")  # 停止时更新文字
        except Exception as e:
            print(f"[{self.task_id}] 任务出错: {e}")
            task_store.update_progress(self.task_id, 0, "ERROR")
            self.set_status_text(f"系统异常: {str(e)}")  # 报错时更新文字

    def current_step_index(self):
        task = task_store.get(self.task_id)
        return task["step"] if task else 0

    def run(self, data):
        raise NotImplementedError