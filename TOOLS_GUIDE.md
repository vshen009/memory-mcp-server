# Memory MCP Server - 工具脚本使用指南

## 便捷脚本

项目包含几个便捷的脚本来管理记忆，无需手动编写 Python 代码。

### 1. add_memory.sh - 添加记忆

**用法：**
```bash
./add_memory.sh "要记住的内容"
```

**示例：**
```bash
cd /home/trinity/happpy/memory-mcp-server
./add_memory.sh "我喜欢喝咖啡，特别是意式浓缩"
```

**说明：**
- 自动使用 user_id: `your-user-id`
- 自动添加时间戳
- 内容需要用引号包裹

---

### 2. search_memory.sh - 搜索记忆

**用法：**
```bash
./search_memory.sh "搜索关键词" [返回数量]
```

**示例：**
```bash
# 基本搜索
./search_memory.sh "Vincent 的偏好"

# 指定返回数量
./search_memory.sh "编程" 10
```

**说明：**
- 默认返回 5 条结果
- 使用语义搜索，不需要精确匹配
- 结果按相关性排序

---

### 3. list_memory.sh - 列出所有记忆

**用法：**
```bash
./list_memory.sh [数量限制]
```

**示例：**
```bash
# 列出最近 20 条（默认）
./list_memory.sh

# 列出最近 50 条
./list_memory.sh 50
```

**说明：**
- 默认显示 20 条
- 按时间倒序排列
- 显示创建时间和内容摘要

---

### 4. start.sh - 启动 MCP 服务器

**用法：**
```bash
./start.sh
```

**说明：**
- 检查依赖和配置
- 启动 MCP 服务器
- 用于手动测试或非 Claude Code 场景

---

### 5. claude-code-launcher.sh - Claude Code 启动器

**说明：**
- 这个脚本由 Claude Code 自动调用
- 不要手动运行
- 配置在 `~/.claude.json` 中

---

## 完整使用示例

### 场景 1：添加一条新记忆

```bash
cd /home/trinity/happpy/memory-mcp-server
./add_memory.sh "我正在学习 Rust 编程语言"
```

输出：
```
✓ 记忆添加成功！
内容: 我正在学习 Rust 编程语言

API 响应:
[
  {
    "message": "Memory processing has been queued for background execution",
    "status": "PENDING",
    "event_id": "..."
  }
]
```

### 场景 2：搜索刚才添加的记忆

**注意：** Mem0 Cloud 使用异步处理，需要等待 5-10 秒后再搜索。

```bash
# 等待 10 秒
sleep 10

# 搜索
./search_memory.sh "Rust 编程" 5
```

输出：
```
找到 5 条相关记忆:
============================================================
1. [0.92] 我正在学习 Rust 编程语言
2. [0.75] Vincent is evaluating and implementing imageModel...
3. ...
```

### 场景 3：查看所有记忆

```bash
./list_memory.sh 20
```

输出：
```
共 18 条记忆 (最新 18 条):
============================================================
1. [2026-02-18] Vincent's birthday is January 9th and his zodiac sign is Capricorn.
2. [2026-02-17] Vincent prefers to watch a concise investment news summary every morning.
3. ...
```

---

## 故障排查

### 问题 1：命令找不到

**错误：** `bash: ./add_memory.sh: No such file or directory`

**原因：** 没有切换到正确的目录

**解决：**
```bash
cd /home/trinity/happpy/memory-mcp-server
./add_memory.sh "测试"
```

### 问题 2：权限被拒绝

**错误：** `Permission denied`

**解决：**
```bash
chmod +x *.sh
```

### 问题 3：搜索不到刚添加的记忆

**原因：** Mem0 Cloud 异步处理需要时间

**解决：** 等待 5-10 秒后再搜索

---

## 集成到 Claude Code

重启 Claude Code 后，Memory MCP Server 会自动加载，你可以直接使用：

```
你：请记住，我喜欢 TypeScript
我：[自动调用 memory_add] 已记录

你：我喜欢什么编程语言？
我：[自动调用 memory_search] 根据记忆，你喜欢 TypeScript...
```

---

## 与 OpenClaw 同步

所有记忆自动同步到 Mem0 Cloud，OpenClaw 也能访问：

- OpenClaw 添加的记忆，Claude Code 可以搜索
- Claude Code 添加的记忆，OpenClaw 也能访问
- 完全自动化，无需手动操作

---

**更新时间：** 2026-02-18 09:25
