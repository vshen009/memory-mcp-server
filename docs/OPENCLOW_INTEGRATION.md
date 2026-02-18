# OpenClaw 集成指南

> **状态:** 草稿 - 待完善
> **最后更新:** 2026-02-18
> **适用版本:** Memory MCP Server v1.0.0+

---

## 目录

- [概述](#概述)
- [为什么选择 OpenClaw](#为什么选择-openclaw)
- [架构说明](#架构说明)
- [双向同步机制](#双向同步机制)
- [集成步骤](#集成步骤)
- [Cron 定时任务配置](#cron-定时任务配置)
- [故障排查](#故障排查)
- [最佳实践](#最佳实践)
- [API 参考](#api-参考)

---

## 概述

OpenClaw 是一个强大的 AI 工作流系统,Memory MCP Server 可以与其深度集成,实现:

- ✅ **双向记忆同步**: OpenClaw ⟷ Mem0 Cloud
- ✅ **定时自动采集**: 每日自动推送/拉取记忆
- ✅ **结构化存储**: memory/YYYY-MM-DD.md + KANBAN.md
- ✅ **智能检索**: 语义搜索 + 关键词过滤

---

## 为什么选择 OpenClaw

### OpenClaw 优势

1. **工程化记忆层**
   - 每日自动采集脚本 (daily_capture)
   - 每周巡检脚本 (weekly_report)
   - 可维护的目录结构

2. **双向同步**
   - 推送: OpenClaw → Mem0 (memory + KANBAN 快照)
   - 拉取: Mem0 → OpenClaw (新增关键记忆)
   - 去重状态文件: memory/mem0-sync-state.json

3. **与 Workspace 深度集成**
   - scripts/mem0_client.py - 官方 REST API 客户端
   - scripts/mem0/daily_capture.py - 每日双向同步
   - scripts/mem0/weekly_report.py - 每周报告
   - projects/mem0-integration/ - 项目文档

---

## 架构说明

### OpenClaw Workspace 结构

```
~/.openclaw/workspace/
├── .env                          # 环境变量 (MEM0_API_KEY)
├── memory/
│   ├── YYYY-MM-DD.md             # 每日记忆文件
│   ├── mem0-sync-state.json      # 同步状态
│   └── USER.md                   # 用户画像
├── KANBAN.md                     # 任务看板
├── scripts/
│   ├── mem0_client.py            # REST API 客户端
│   └── mem0/
│       ├── daily_capture.py      # 每日同步
│       ├── weekly_report.py      # 每周报告
│       └── README.md             # 脚本说明
└── projects/
    └── mem0-integration/
        ├── DEV_BRIEF.md          # 开发简报
        └── DOCKER_DEPLOYMENT.md  # Docker 部署
```

### 数据流

```
┌─────────────┐
│  OpenClaw   │
│  Workspace  │
└──────┬──────┘
       │
       │ 1. daily_capture.py (cron)
       │    - 读取 memory/*.md
       │    - 读取 KANBAN.md
       │    - 推送到 Mem0
       │
       ▼
┌─────────────┐
│ Memory MCP  │
│   Server    │
└──────┬──────┘
       │
       │ 2. Mem0 Cloud API
       │    - POST /v1/memories/
       │    - POST /v2/memories/search/
       │    - POST /v2/memories/
       │
       ▼
┌─────────────┐
│  Mem0 Cloud │
│   (API)     │
└─────────────┘
       │
       │ 3. 拉取新增记忆
       │    - 按关键词搜索
       │    - 写回 memory/*.md
       │
       ▼
┌─────────────┐
│  OpenClaw   │
│  (更新)     │
└─────────────┘
```

---

## 双向同步机制

### 推送 (OpenClaw → Mem0)

**时机:** 每日 00:10 (cron)

**内容:**
- 当日/昨日 memory/YYYY-MM-DD.md
- KANBAN.md 末尾内容
- USER.md 用户画像摘要

**限制:**
- 单条长度 2000-3000 字
- 自动添加元数据: `channel=system`, `priority=normal`

### 拉取 (Mem0 → OpenClaw)

**时机:** 每日 00:10 (推送后立即拉取)

**关键词:**
- 生日/星座/纪念日
- 个人信息/偏好
- family/details

**去重:**
- 状态文件: `memory/mem0-sync-state.json`
- 记录已同步的记忆 ID
- 避免重复写入

---

## 集成步骤

### 前置要求

1. OpenClaw Workspace 已配置
2. Mem0 API Key 已获取
3. Memory MCP Server 已安装

### 步骤 1: 配置环境变量

在 `~/.openclaw/workspace/.env` 添加:

```bash
# Mem0 API 配置
MEM0_API_KEY=m0-your-api-key-here
MEM0_BASE_URL=https://api.mem0.ai
MEM0_API_MODE=auto
MEMORY_DEFAULT_USER_ID=your-user-id

# (可选) 组织和项目
# MEM0_ORG_ID=...
# MEM0_PROJECT_ID=...
```

### 步骤 2: 验证连接

```bash
cd ~/.openclaw/workspace
USER_ID="${MEMORY_DEFAULT_USER_ID:-your-user-id}"

# 测试添加
python3 scripts/mem0_client.py add \
  --text "OpenClaw 集成测试" \
  --user-id "${USER_ID}" \
  --scope project-continuity \
  --source openclaw-manual

# 测试搜索
python3 scripts/mem0_client.py search \
  --query "OpenClaw 集成" \
  --user-id "${USER_ID}" \
  --top-k 5

# 测试列表
python3 scripts/mem0_client.py list \
  --user-id "${USER_ID}" \
  --page-size 20
```

### 步骤 3: 手动运行同步

```bash
# 每日同步
python3 scripts/mem0/daily_capture.py

# 每周报告
python3 scripts/mem0/weekly_report.py
```

### 步骤 4: 配置 Cron 任务

在 OpenClaw cron 配置中添加:

```yaml
mem0-daily-capture:
  schedule: "0 10 * * *"  # 每天 00:10
  command: "python3 scripts/mem0/daily_capture.py"
  user_id: "${USER_ID}"

mem0-weekly-report:
  schedule: "0 23 * * 0"  # 每周日 23:00
  command: "python3 scripts/mem0/weekly_report.py"
  user_id: "${USER_ID}"
```

---

## Cron 定时任务配置

### 每日同步任务

**时间:** 每天 00:10
**脚本:** `scripts/mem0/daily_capture.py`
**功能:**
- 推送昨日记忆到 Mem0
- 拉取新增记忆回 OpenClaw
- 更新同步状态文件

### 每周报告任务

**时间:** 每周日 23:00
**脚本:** `scripts/mem0/weekly_report.py`
**功能:**
- 生成记忆统计报告
- 输出到 `generated/mem0-weekly-YYYY-MM-DD.md`
- 包含命中条数、关键记忆、疑似重复

### OpenClaw Cron 配置示例

```json
{
  "cron": {
    "mem0-daily": {
      "schedule": "0 10 * * *",
      "action": "exec",
      "command": "python3 scripts/mem0/daily_capture.py",
      "enabled": true
    },
    "mem0-weekly": {
      "schedule": "0 23 * * 0",
      "action": "exec",
      "command": "python3 scripts/mem0/weekly_report.py",
      "enabled": true
    }
  }
}
```

---

## 故障排查

### 问题 1: ModuleNotFoundError: No module named 'mem0'

**原因:** Python 环境不完整

**解决:**
```bash
source .venv-mem0/bin/activate
pip install python-dotenv
pip install mem0ai
```

### 问题 2: API 返回 401/403

**原因:** API Key 无效或过期

**解决:**
1. 检查 `.env` 中的 `MEM0_API_KEY`
2. 访问 https://platform.mem0.ai 重新生成
3. 确认 Key 格式: `m0-xxxx`

### 问题 3: 同步状态文件损坏

**原因:** `memory/mem0-sync-state.json` 格式错误

**解决:**
```bash
# 备份
cp memory/mem0-sync-state.json memory/mem0-sync-state.json.bak

# 重置
echo '{"synced_ids": []}' > memory/mem0-sync-state.json
```

### 问题 4: Cron 任务未执行

**检查:**
```bash
# 查看 cron 日志
tail -f /var/log/cron

# 手动测试
python3 scripts/mem0/daily_capture.py
```

---

## 最佳实践

### 1. 定期备份

```bash
# 备份记忆目录
tar -czf memory-backup-$(date +%Y%m%d).tar.gz memory/
```

### 2. 监控同步状态

```bash
# 查看最后同步时间
cat memory/mem0-sync-state.json | grep last_sync
```

### 3. 定期清理

```bash
# 删除 30 天前的旧记忆
find memory/ -name "*.md" -mtime +30 -delete
```

### 4. 版本控制

```bash
# 提交关键配置
git add .env.example scripts/mem0/
git commit -m "chore: update mem0 integration"
```

---

## API 参考

### mem0_client.py

```bash
# 添加记忆
python3 scripts/mem0_client.py add \
  --text "记忆内容" \
  --user-id "${USER_ID}" \
  --scope personal \
  --source manual

# 搜索记忆
python3 scripts/mem0_client.py search \
  --query "搜索关键词" \
  --user-id "${USER_ID}" \
  --top-k 10

# 列出记忆
python3 scripts/mem0_client.py list \
  --user-id "${USER_ID}" \
  --page-size 20

# 查询事件状态
python3 scripts/mem0_client.py event \
  --event-id abc123 \
  --event-path-template "/v1/events/{event_id}/"
```

### Memory MCP Server

```json
{
  "mcpServers": {
    "memory": {
      "type": "stdio",
      "command": "/path/to/claude-code-launcher.sh",
      "env": {
        "MEM0_API_KEY": "m0-your-key",
        "MEMORY_DEFAULT_USER_ID": "your-user-id"
      }
    }
  }
}
```

---

## 相关资源

- [Memory MCP Server GitHub](https://github.com/vshen009/memory-mcp-server)
- [Mem0 官方文档](https://docs.mem0.ai/)
- [OpenClaw 文档](../.openclaw/workspace/)
- [MCP 协议规范](https://modelcontextprotocol.io/)

---

**TODO:**
- [ ] 添加更多故障排查案例
- [ ] 补充性能优化建议
- [ ] 添加视频教程链接
- [ ] 编写自动化测试用例
