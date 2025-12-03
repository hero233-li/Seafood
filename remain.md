app/
├── routes/                  # 【路由层】
│   ├── __init__.py
│   ├── web.py               #   处理页面访问 (如 /)
│   └── api.py               # 处理接口请求 (如 /api/apply)
│
├── templates/               # 存放 HTML
│   │   └── index.html       # (你之前的 HTML 文件放这里)
│   │
├── core/                    # 【核心引擎层】通用逻辑
│   ├── engine.py            # 负责线程管理、状态更新、停止信号检查的基类
│   └── store.py             # 任务状态存储 (Redis/Memory)
│
├── domains/                 # 【领域业务层】按业务线拆分文件夹
│   ├── loan/                # === 贷款业务域 ===
│   │   ├── __init__.py
│   │   ├── orchestrator.py  # [关键] 贷款流程编排 (定义30个步骤的顺序)
│   │   ├── steps.py         # 具体的步骤逻辑实现
│   │   └── validator.py     # 进件参数校验
│
└── integrations/            # 【集成层】封装那30个外部接口
    ├── __init__.py
    ├── risk_system.py       # 封装风控系统的 HTTP 调用
    ├── core_banking.py      # 封装核心系统的 HTTP 调用
    └── sms_gateway.py       # 封装短信网关