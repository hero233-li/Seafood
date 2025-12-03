CREATE DATABASE IF NOT EXISTS findebug_pro DEFAULT CHARSET utf8mb4 COLLATE utf8mb4_general_ci;

USE findebug_pro;

CREATE TABLE `tasks` (
  `task_id` varchar(50) NOT NULL COMMENT '受理单号/任务ID',
  `status` varchar(20) DEFAULT 'PROCESSING' COMMENT '状态: PROCESSING/SUCCESS/STOPPED/ERROR',
  `step` int(11) DEFAULT 0 COMMENT '当前进度节点索引',
  `stop_signal` tinyint(1) DEFAULT 0 COMMENT '停止信号: 0-否, 1-是',
  `start_time` double DEFAULT 0 COMMENT '任务开始时间戳',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `data` longtext COMMENT '原始表单数据 (JSON)',
  `steps` longtext COMMENT '流程步骤定义 (JSON)',
  `display_info` longtext COMMENT '前端展示详情 (JSON)',
  PRIMARY KEY (`task_id`),
  KEY `idx_created_at` (`created_at`) USING BTREE COMMENT '按时间排序查询'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='任务执行流水表';