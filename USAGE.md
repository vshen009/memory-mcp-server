# Memory MCP Server - 快速上手指南

## 项目概述

Memory MCP Server 是一个统一的内存管理系统，通过 MCP (Model Context Protocol) 为 AI 客户端提供持久化记忆功能。

**特点：**
- ✅ 跨平台支持（任何支持 MCP 的客户端）
- ✅ 基于 Mem0 Cloud API（无需本地数据库）
- ✅ 简单配置，开箱即用
- ✅ 支持多用户、多客户端记忆共享

---

## 快速开始

### 1. 安装依赖

```bash
cd /home/trinity/happpy/memory-mcp-server
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. 配置环境变量

```bash
cp .env.example .env
```

编辑 `.env` 文件：
```env
MEM0_API_KEY=m0-your-api-key-here
MEM0_BASE_URL=https://api.mem0.ai
MEMORY_DEFAULT_USER_ID=your-user-id
```

### 3. 测试客户端

```bash
source venv/bin/activate
python test_client.py
```

你应该看到类似输出：
```
============================================================
Memory MCP Server - 客户端测试
============================================================

1. 初始化客户端...
   ✓ API Base: https://api.mem0.ai
   ✓ API Mode: cloud

2. 测试添加记忆...
   ✓ 添加成功

...
```

---

## Claude Code 集成

### 方法 1：直接配置（推荐）

编辑 `~/.claude_code_config.json`：

```json
{
  "mcpServers": {
    "memory": {
      "command": "python",
      "args": ["/home/trinity/happpy/memory-mcp-server/src/server.py"],
      "env": {
        "MEM0_API_KEY": "m0-your-api-key-here",
        "MEMORY_DEFAULT_USER_ID": "your-user-id",
        "LOG_LEVEL": "INFO"
      }
    }
  }
}
```

### 方法 2：使用启动脚本

创建一个启动脚本 `start-mcp-server.sh`：

```bash
#!/bin/bash
cd /home/trinity/happpy/memory-mcp-server
source venv/bin/activate
python src/server.py
```

然后在配置中引用：

```json
{
  "mcpServers": {
    "memory": {
      "command": "/home/trinity/happpy/memory-mcp-server/start-mcp-server.sh"
    }
  }
}
```

### 重启 Claude Code

配置完成后，重启 Claude Code 使配置生效。

---

## 使用示例

在 Claude Code 中，你现在可以使用以下工具：

### 添加记忆

```
请记住：我喜欢用 Python 和 TypeScript 进行开发
```

Claude 会自动调用 `memory_add` 工具。

### 搜索记忆

```
我喜欢用什么编程语言？
```

Claude 会自动调用 `memory_search` 工具查找相关记忆。

### 手动调用工具

你也可以明确要求使用工具：

```
请使用 memory_list 工具列出我所有的记忆
```

```
请使用 memory_add 工具记录：我正在学习 MCP 协议
```

---

## 可用工具

### 1. memory_add

添加新记忆。

**参数：**
- `text` (必需): 要记住的文本内容
- `user_id` (可选): 用户ID，默认从环境变量读取
- `scope` (可选): 记忆类别，默认 "general"
- `source` (可选): 来源标识，默认 "mcp-server"

**示例：**
```python
memory_add(
    text="用户喜欢编程，主要使用 Python",
    user_id="vincent",
    scope="preferences"
)
```

### 2. memory_search

搜索已存储的记忆。

**参数：**
- `query` (必需): 搜索查询（自然语言）
- `user_id` (可选): 用户ID
- `top_k` (可选): 返回结果数量，默认 5

**示例：**
```python
memory_search(
    query="用户喜欢什么编程语言？",
    user_id="vincent",
    top_k=3
)
```

### 3. memory_list

列出所有记忆。

**参数：**
- `user_id` (可选): 用户ID
- `limit` (可选): 返回结果数量限制，默认 20

### 4. memory_delete

删除指定的记忆。

**参数：**
- `memory_ids` (必需): 要删除的记忆 ID 列表
- `user_id` (可选): 用户ID

---

## 项目结构

```
memory-mcp-server/
├── src/
│   ├── server.py           # MCP 服务器主程序
│   └── mem0_wrapper.py     # Mem0 客户端包装器
├── venv/                   # Python 虚拟环境
├── .env                    # 环境变量配置（需创建）
├── .env.example            # 配置示例
├── requirements.txt        # Python 依赖
├── test_client.py          # 测试脚本
├── start.sh                # 启动脚本
├── README.md               # 项目说明
└── USAGE.md                # 本文档
```

---

## 故障排查

### 问题 1：MCP 服务器未启动

**症状：** Claude Code 中无法使用记忆工具

**解决方法：**
1. 检查 `~/.claude_code_config.json` 配置是否正确
2. 手动运行测试：`python test_client.py`
3. 查看 Claude Code 日志

### 问题 2：API Key 无效

**症状：** `ERROR: MEM0_API_KEY is required for Mem0 Cloud endpoint.`

**解决方法：**
1. 从 https://platform.mem0.ai 获取 API Key
2. 确认 `.env` 文件中 `MEM0_API_KEY` 已正确设置
3. 确保 API Key 格式为 `m0-xxxxx`

### 问题 3：记忆未返回结果

**症状：** 搜索时返回 0 条结果

**原因：** Mem0 Cloud 使用异步处理，记忆添加后需要几秒钟才能被搜索到

**解决方法：** 等待 5-10 秒后再次搜索

---

## 下一步

- [ ] 在其他电脑上部署（复制项目 + 配置 API Key）
- [ ] 集成到 OpenClaw
- [ ] 封装为 Docker 镜像
- [ ] 发布为 NPX 包

---

## 相关链接

- [Mem0 平台](https://platform.mem0.ai)
- [MCP 协议文档](https://modelcontextprotocol.io)
- [OpenClaw 文档](https://docs.openclaw.ai)

---

## 许可证

MIT
