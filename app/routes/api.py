from flask import Blueprint, request, jsonify
import threading
import time
from app.core.store import task_store
from app.domains.loan.orchestrator import LoanOrchestrator

api_bp = Blueprint('api', __name__, url_prefix='/api')


# ... (保留原有的 /loan/apply, /status, /stop 接口，代码不变) ...

@api_bp.route('/loan/apply', methods=['POST'])
def loan_apply():
    # ... (保持原样) ...
    data = request.json
    task_id = f"T-{int(time.time())}"

    steps = [
        {"title": "创建项目", "user": "曲丽丽"},
        {"title": "部门初审", "user": "周毛毛"},
        {"title": "财务复核", "user": "财务处"},
        {"title": "完成", "user": "系统"}
    ]

    amount_str = f"¥ {int(data.get('amount', 0)):,}"
    display_info = {
        "受理单号": task_id,
        "用户姓名": data.get('name'),
        "身份证号": data.get('idCard'),
        "联系方式": data.get('mobile'),
        "申请金额": amount_str,
        "分期期数": data.get('terms'),
        "是否加急": "是" if data.get('isUrgent') else "否",
        "当前状态": "审核中..."
    }

    task_store.init_task(task_id, data, steps, display_info)

    orchestrator = LoanOrchestrator(task_id)
    t = threading.Thread(target=orchestrator.execute, args=(data,))
    t.daemon = True
    t.start()

    return jsonify({'code': 200, 'taskId': task_id})


@api_bp.route('/status', methods=['GET'])
def get_status():
    # ... (保持原样) ...
    task_id = request.args.get('taskId')
    task = task_store.get(task_id)
    if not task: return jsonify({'code': 404, 'msg': 'Task not found'})
    return jsonify({
        'code': 200,
        'status': task['status'],
        'currentStepIndex': task['step'],
        'steps': task['steps'],
        'displayInfo': task['displayInfo']
    })


@api_bp.route('/stop', methods=['POST'])
def stop_task():
    # ... (保持原样) ...
    task_id = request.json.get('taskId')
    success = task_store.set_stop_signal(task_id)
    return jsonify({'code': 200, 'success': success})


# 【新增】历史记录接口
@api_bp.route('/history', methods=['GET'])
def get_history_list():
    page = int(request.args.get('page', 1))
    size = int(request.args.get('size', 10))
    keyword = request.args.get('keyword', '')

    result = task_store.get_history(page, size, keyword)

    return jsonify({
        'code': 200,
        'data': result
    })