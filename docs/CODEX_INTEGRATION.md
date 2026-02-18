# Codex 集成指南

> **状态:** ✅ 可用（实验性）
> **适用版本:** Memory MCP Server v1.0.0+

---

## 核心说明

本项目对 Codex 的集成方式是 **MCP 标准接入**，不是额外封装 Codex API。

你需要做的只有两件事：

1. 启动本 MCP Server（stdio）
2. 在 Codex 的 MCP 配置中注册该服务

---

## 快速接入

### 1) 安装并配置项目

```bash
cd memory-mcp-server
./install.sh
```

`install.sh` 会尝试自动注册用户级 Codex MCP（写入 `~/.codex/config.toml`）。

编辑 `.env`：

```env
MEM0_BASE_URL=https://api.mem0.ai
MEM0_API_KEY=m0-your-api-key-here
MEMORY_DEFAULT_USER_ID=your-user-id
LOG_LEVEL=INFO
```

### 2) 验证用户级注册

```bash
codex mcp list
codex mcp get memory
```

### 3) 手动注册（仅自动注册失败时）

```bash
codex mcp add memory \
  --env MEM0_BASE_URL=https://api.mem0.ai \
  --env MEM0_API_KEY=m0-your-api-key-here \
  --env MEMORY_DEFAULT_USER_ID=your-user-id \
  --env LOG_LEVEL=INFO \
  -- /完整路径/memory-mcp-server/codex-launcher.sh
```

---

## 工具列表

接入成功后，Codex 应可看到以下工具：

- `memory_add`
- `memory_search`
- `memory_list`
- `memory_delete`

---

## 验证流程

建议按顺序验证：

1. 添加记忆：`memory_add`
2. 搜索记忆：`memory_search`
3. 列出记忆：`memory_list`
4. 删除记忆：`memory_delete`

---

## 常见问题

### 看不到工具

- 确认 Codex 已重启
- 确认 `codex mcp list` 中包含 `memory`
- 确认 `codex-launcher.sh` 有执行权限

```bash
chmod +x codex-launcher.sh
```

### 报 API Key 错误

- 检查 `MEM0_API_KEY` 是否有效
- 检查是否把配置写到了正确的配置文件

### 搜不到记忆

- 检查 `MEMORY_DEFAULT_USER_ID` 是否与写入时一致
- 用更通用关键词再试一次

---

## 兼容性说明

- 该接入方式不影响现有 Claude Code 配置
- 该接入方式不影响 OpenClaw 同步流程
- Codex、Claude Code 可同时指向同一个 Memory MCP Server
