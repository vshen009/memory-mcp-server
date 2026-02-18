# Claude Code 完整指南

> **状态:** ✅ 完成
> **适用版本:** v1.0.0+

---

## 快速开始 (3 分钟)

### 步骤 1: 安装 Memory MCP Server

```bash
git clone https://github.com/vshen009/memory-mcp-server.git
cd memory-mcp-server
./install.sh
```

### 步骤 2: 配置环境变量

```bash
cp .env.example .env
nano .env
```

填入你的 API Key:
```env
MEM0_API_KEY=m0-your-api-key-here
MEMORY_DEFAULT_USER_ID=your-user-id
```

### 步骤 3: 配置 Claude Code

编辑 `~/.claude.json`:

```json
{
  "mcpServers": {
    "memory": {
      "type": "stdio",
      "command": "/完整路径/claude-code-launcher.sh",
      "env": {
        "MEM0_API_KEY": "m0-your-key",
        "MEMORY_DEFAULT_USER_ID": "your-user-id",
        "LOG_LEVEL": "INFO"
      }
    }
  }
}
```

### 步骤 4: 重启 Claude Code

完全退出并重启 Claude Code。

---

## 使用示例

### 让 AI 记住信息

**你:**
```
记住: 我喜欢用 Python 和 TypeScript 开发,擅长后端和 DevOps。
```

**Claude:** (自动调用 memory_add)

### 询问记忆

**你:**
```
我擅长什么编程语言?
```

**Claude:** (自动调用 memory_search)
```
根据你的记忆,你喜欢用 Python 和 TypeScript 开发,擅长后端和 DevOps。
```

### 查看所有记忆

**你:**
```
列出我所有的记忆
```

**Claude:** (自动调用 memory_list)

---

## 工具详解

### memory_add

添加新记忆。

**参数:**
- `text` (必需): 记忆内容
- `user_id` (可选): 用户ID,默认从环境变量读取
- `scope` (可选): 类别,默认 "general"
- `source` (可选): 来源,默认 "mcp-server"

**示例:**
```json
{
  "text": "用户喜欢 Python",
  "scope": "preferences"
}
```

### memory_search

搜索记忆。

**参数:**
- `query` (必需): 搜索查询
- `user_id` (可选): 用户ID
- `top_k` (可选): 返回数量,默认 5
- `scope` (可选): 类别过滤

**示例:**
```json
{
  "query": "喜欢什么编程语言?",
  "top_k": 3
}
```

### memory_list

列出所有记忆。

**参数:**
- `user_id` (可选): 用户ID
- `scope` (可选): 类别过滤
- `limit` (可选): 数量限制,默认 20

### memory_delete

删除记忆。

**参数:**
- `memory_ids` (必需): 记忆ID列表
- `user_id` (可选): 用户ID

---

## 高级用法

### 记忆分类

使用 `scope` 参数组织记忆:

```json
{
  "text": "生日是 1月9日",
  "scope": "personal-details"
}
```

常用分类:
- `personal-details`: 个人信息
- `preferences`: 偏好设置
- `work`: 工作相关
- `project-patterns`: 项目模式
- `project-continuity`: 项目连续性

### 批量操作

列出最近 50 条记忆:
```json
{
  "limit": 50
}
```

### 记忆去重

搜索相似记忆:
```json
{
  "query": "Python 开发",
  "top_k": 10
}
```

然后删除重复的 ID。

---

## 故障排查

### 工具未出现

**检查:**
1. Claude Code 是否重启
2. 配置文件语法是否正确
3. 启动脚本是否有执行权限

**验证:**
```bash
cat ~/.claude.json | python3 -m json.tool
```

### 记忆未保存

**检查:**
1. API Key 是否有效
2. 网络连接是否正常
3. 查看服务器日志

**测试:**
```bash
source venv/bin/activate
python src/server.py
```

### 搜索结果为空

**原因:**
- user_id 不匹配
- 记忆还未被索引
- 搜索关键词不准确

**解决:**
- 确认 `MEMORY_DEFAULT_USER_ID`
- 等待几秒后重试
- 使用更通用的关键词

---

## 最佳实践

### 1. 定期备份

```bash
# 使用测试脚本导出
./list_memory.sh > backup-$(date +%Y%m%d).txt
```

### 2. 记忆命名规范

使用清晰的 `scope`:
- `personal-details`: 个人信息
- `user-preferences`: 用户偏好
- `work-context`: 工作上下文
- `family`: 家庭信息

### 3. 批量导入

从文件导入记忆:
```bash
while read line; do
  ./add_memory.sh "$line"
done < memories.txt
```

---

## 相关资源

- [Memory MCP Server GitHub](https://github.com/vshen009/memory-mcp-server)
- [Mem0 官方文档](https://docs.mem0.ai/)
- [Claude Code 文档](https://code.anthropic.com/)
- [OpenClaw 集成指南](./OPENCLOW_INTEGRATION.md)
