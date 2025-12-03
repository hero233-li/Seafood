import time

class TaskStore:
    def __init__(self):
        # 模拟数据库存储
        self._data = {}

    def init_task(self, task_id, form_data, steps, display_info):
        self._data[task_id] = {
            "taskId": task_id,
            "status": "PROCESSING",
            "step": 0,
            "stop_signal": False,
            "data": form_data,
            "steps": steps,
            "displayInfo": display_info,
            "logs": [],
            "startTime": time.time() # 【新增】记录入库时间，用于排序
        }

    def get(self, task_id):
        return self._data.get(task_id)

    # 【新增】支持分页和搜索的历史记录查询
    def get_history(self, page=1, size=10, keyword=""):
        # 1. 转换为列表并按时间倒序 (模拟 Order By create_time desc)
        all_tasks = list(self._data.values())
        all_tasks.sort(key=lambda x: x.get("startTime", 0), reverse=True)

        # 2. 搜索过滤 (模拟 SQL Like %keyword%)
        if keyword:
            kw = keyword.lower()
            all_tasks = [
                t for t in all_tasks
                if kw in t["taskId"].lower() or
                   kw in str(t["data"].get("name", "")).lower()
            ]

        # 3. 计算分页 (模拟 Limit Offset)
        total = len(all_tasks)
        start_idx = (page - 1) * size
        end_idx = start_idx + size
        page_data = all_tasks[start_idx:end_idx]

        return {
            "total": total,
            "page": page,
            "size": size,
            "items": page_data
        }

    def update_progress(self, task_id, step_index, status="PROCESSING"):
        if task_id in self._data:
            self._data[task_id]["step"] = step_index
            self._data[task_id]["status"] = status

    def update_display_item(self, task_id, key, value):
        if task_id in self._data:
            self._data[task_id]["displayInfo"][key] = value

    def set_stop_signal(self, task_id):
        if task_id in self._data:
            self._data[task_id]["stop_signal"] = True
            return True
        return False

task_store = TaskStore()