# Memory MCP Server API 参考

> **版本:** v1.0.0
> **协议:** MCP (Model Context Protocol)

---

## 概述

Memory MCP Server 提供 4 个核心工具,通过 MCP 协议与 AI 客户端通信。

---

## 工具列表

### 1. memory_add

添加新记忆到 Mem0 Cloud。

**端点:** MCP Tool
**描述:** 添加新记忆。当用户提供关于自己、偏好、或任何未来可能有用的信息时调用此方法。

#### 参数

| 参数 | 类型 | 必需 | 默认值 | 说明 |
|------|------|------|--------|------|
| `text` | string | ✅ | - | 要记住的文本内容 |
| `user_id` | string | ❌ | 环境变量 | 用户ID (MEMORY_DEFAULT_USER_ID) |
| `scope` | string | ❌ | "general" | 记忆范围/类别 |
| `source` | string | ❌ | "mcp-server" | 来源标识 |

#### 返回值

```json
{
  "success": true,
  "result": {
    "id": "uuid",
    "memory": "记忆内容",
    "user_id": "vincent-main",
    "metadata": {...}
  },
  "message": "记忆添加成功"
}
```

#### 示例

**调用:**
```json
{
  "text": "Vincent 喜欢用 Python 开发",
  "scope": "preferences",
  "user_id": "vincent-main"
}
```

**响应:**
```json
{
  "success": true,
  "result": {
    "id": "1df7b95a-4518-4968-bb74-74c1e521fb7a",
    "memory": "Vincent 喜欢用 Python 开发",
    "user_id": "vincent-main"
  },
  "message": "记忆添加成功"
}
```

---

### 2. memory_search

语义搜索已存储的记忆。

**端点:** MCP Tool
**描述:** 搜索已存储的记忆。每次用户提问时都应该调用此方法来查找相关信息。

#### 参数

| 参数 | 类型 | 必需 | 默认值 | 说明 |
|------|------|------|--------|------|
| `query` | string | ✅ | - | 搜索查询（自然语言问题） |
| `user_id` | string | ❌ | 环境变量 | 用户ID |
| `top_k` | integer | ❌ | 5 | 返回结果数量 |
| `scope` | string | ❌ | "" | 可选的范围过滤 |

#### 返回值

```json
{
  "success": true,
  "results": [
    {
      "id": "uuid",
      "memory": "记忆内容",
      "score": 0.95,
      "metadata": {...}
    }
  ],
  "count": 1,
  "message": "找到 1 条相关记忆"
}
```

#### 示例

**调用:**
```json
{
  "query": "Vincent 喜欢什么编程语言?",
  "user_id": "vincent-main",
  "top_k": 3
}
```

**响应:**
```json
{
  "success": true,
  "results": [
    {
      "id": "1df7b95a-4518-4968-bb74-74c1e521fb7a",
      "memory": "Vincent 喜欢用 Python 开发",
      "score": 0.92
    }
  ],
  "count": 1
}
```

---

### 3. memory_list

列出用户的所有记忆。

**端点:** MCP Tool
**描述:** 列出用户的所有记忆。用于查看或批量处理记忆。

#### 参数

| 参数 | 类型 | 必需 | 默认值 | 说明 |
|------|------|------|--------|------|
| `user_id` | string | ❌ | 环境变量 | 用户ID |
| `scope` | string | ❌ | "" | 可选的范围过滤 |
| `limit` | integer | ❌ | 20 | 返回结果数量限制 |

#### 返回值

```json
{
  "success": true,
  "results": [
    {
      "id": "uuid",
      "memory": "记忆内容",
      "created_at": "2026-02-18T...",
      "metadata": {...}
    }
  ],
  "count": 20,
  "message": "共 20 条记忆"
}
```

#### 示例

**调用:**
```json
{
  "user_id": "vincent-main",
  "limit": 50
}
```

---

### 4. memory_delete

删除指定的记忆。

**端点:** MCP Tool
**描述:** 删除指定的记忆。提供记忆 ID 列表来删除特定记忆。

#### 参数

| 参数 | 类型 | 必需 | 默认值 | 说明 |
|------|------|------|--------|------|
| `memory_ids` | array | ✅ | - | 要删除的记忆 ID 列表 |
| `user_id` | string | ❌ | 环境变量 | 用户ID |

#### 返回值

```json
{
  "success": true,
  "deleted_count": 2,
  "errors": [],
  "message": "成功删除 2 条记忆"
}
```

#### 示例

**调用:**
```json
{
  "memory_ids": [
    "1df7b95a-4518-4968-bb74-74c1e521fb7a",
    "4adc3fe4-9c32-46ce-83de-3987f2c7690a"
  ],
  "user_id": "vincent-main"
}
```

---

## 环境变量

### MEM0_API_KEY

**必需:** 是 (Cloud 模式)
**说明:** Mem0 Cloud API 密钥
**获取:** https://platform.mem0.ai
**示例:** `m0-keuN7KwXeYWGuYQZgkXIY5ALoWbXJj3f4dckSwjJ`

### MEM0_BASE_URL

**必需:** 否
**默认:** `https://api.mem0.ai`
**说明:** Mem0 API 地址
**选项:**
- Cloud: `https://api.mem0.ai`
- Local: `http://localhost:8000`

### MEM0_API_MODE

**必需:** 否
**默认:** `auto`
**说明:** API 模式
**选项:**
- `cloud`: Mem0 云服务
- `oss`: 本地/自托管
- `auto`: 自动检测

### MEMORY_DEFAULT_USER_ID

**必需:** 否
**默认:** `default`
**说明:** 默认用户ID
**示例:** `vincent-main`

### LOG_LEVEL

**必需:** 否
**默认:** `INFO`
**说明:** 日志级别
**选项:** `DEBUG`, `INFO`, `WARNING`, `ERROR`

---

## 错误处理

### 错误响应格式

```json
{
  "success": false,
  "error": "错误描述",
  "message": "操作失败"
}
```

### 常见错误

| 错误 | 原因 | 解决方案 |
|------|------|---------|
| `API error 401` | API Key 无效 | 检查 MEM0_API_KEY |
| `API error 429` | 速率限制 | 减少请求频率 |
| `network_error` | 网络问题 | 检查网络连接 |
| `ModuleNotFoundError` | 依赖缺失 | 运行 `pip install -r requirements.txt` |

---

## 最佳实践

### 1. 用户ID 管理

使用有意义的 user_id:
```
vincent-main     # 主用户
vincent-work     # 工作账户
vincent-personal # 个人账户
```

### 2. 记忆分类

使用规范的 scope:
```
personal-details   # 个人信息
user-preferences   # 用户偏好
work-context       # 工作上下文
family            # 家庭信息
project-patterns  # 项目模式
```

### 3. 批量操作

避免频繁调用,使用批量参数:
```json
{
  "limit": 50  // 一次获取更多
}
```

### 4. 错误重试

对网络错误实现指数退避重试:
```
第1次: 立即
第2次: 1秒后
第3次: 2秒后
第4次: 4秒后
```

---

## 相关资源

- [MCP 协议规范](https://modelcontextprotocol.io/)
- [Mem0 API 文档](https://docs.mem0.ai/)
- [Claude Code 集成指南](./CLAUDE_CODE_GUIDE.md)
- [OpenClaw 集成指南](./OPENCLOW_INTEGRATION.md)
