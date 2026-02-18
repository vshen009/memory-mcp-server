# Memory MCP Server

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![MCP](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io/)

统一的内存管理 MCP 服务器，支持 Mem0 Cloud API，可为多个 AI 客户端提供持久化记忆功能。

## 功能特性

- ✅ **添加记忆** - 存储用户信息、偏好和上下文
- ✅ **搜索记忆** - 语义搜索已有记忆
- ✅ **列出记忆** - 查看所有存储的记忆
- ✅ **删除记忆** - 删除指定的记忆
- ✅ **跨平台** - 支持 Claude Code、OpenClaw 等支持 MCP 的客户端
- ✅ **Mem0 Cloud** - 使用云端 API，无需本地数据库
- ✅ **一键安装** - 自动配置依赖和环境

## 一键安装

### Linux/macOS

```bash
# 克隆或下载项目
cd memory-mcp-server

# 运行安装脚本
chmod +x install.sh
./install.sh
```

安装脚本会自动:
- ✅ 检查 Python 环境
- ✅ 创建虚拟环境
- ✅ 安装依赖
- ✅ 生成配置文件
- ✅ 测试服务器

### 配置

安装完成后,编辑 `.env` 文件:

```bash
nano .env
```

填入你的配置:

```env
MEM0_BASE_URL=https://api.mem0.ai
MEM0_API_KEY=m0-your-api-key-here
MEMORY_DEFAULT_USER_ID=your-user-id
LOG_LEVEL=INFO
```

> 💡 你可以从 [platform.mem0.ai](https://platform.mem0.ai) 获取 API Key

## Claude Code 集成

编辑 `~/.claude.json`,添加以下配置:

```json
{
  "mcpServers": {
    "memory": {
      "type": "stdio",
      "command": "/完整路径/memory-mcp-server/claude-code-launcher.sh",
      "env": {
        "MEM0_API_KEY": "m0-your-api-key-here",
        "MEMORY_DEFAULT_USER_ID": "your-user-id",
        "LOG_LEVEL": "INFO"
      }
    }
  }
}
```

**获取完整路径:**

```bash
pwd
```

假设输出是 `/home/username/memory-mcp-server`,则命令为:

```
/home/username/memory-mcp-server/claude-code-launcher.sh
```

重启 Claude Code 即可使用。

> 📖 **详细指南:** [Claude Code 完整指南](docs/CLAUDE_CODE_GUIDE.md)

---

## 📚 文档

- **[Claude Code 指南](docs/CLAUDE_CODE_GUIDE.md)** - Claude Code 集成详细教程
- **[OpenClaw 集成](docs/OPENCLOW_INTEGRATION.md)** - OpenClaw 深度集成指南
- **[Codex 集成](docs/CODEX_INTEGRATION.md)** - Codex AI 助手集成(开发中)
- **[API 参考](docs/API_REFERENCE.md)** - 完整 API 文档
- **[故障排查](docs/TROUBLESHOOTING.md)** - 常见问题解决

---

## 可用工具

### memory_add

添加新记忆。

**参数：**
- `text` (必需): 要记住的文本内容
- `user_id` (可选): 用户ID，默认从环境变量读取
- `scope` (可选): 记忆范围/类别，默认 "general"
- `source` (可选): 来源标识，默认 "mcp-server"

**示例：**
```python
memory_add(
    text="用户喜欢编程，主要使用 Python 和 TypeScript",
    user_id="vincent",
    scope="preferences"
)
```

### memory_search

搜索已存储的记忆。

**参数：**
- `query` (必需): 搜索查询（自然语言问题）
- `user_id` (可选): 用户ID，默认从环境变量读取
- `top_k` (可选): 返回结果数量，默认 5
- `scope` (可选): 可选的范围过滤

**示例：**
```python
memory_search(
    query="用户喜欢什么编程语言？",
    user_id="vincent",
    top_k=3
)
```

### memory_list

列出用户的所有记忆。

**参数：**
- `user_id` (可选): 用户ID，默认从环境变量读取
- `scope` (可选): 可选的范围过滤
- `limit` (可选): 返回结果数量限制，默认 20

### memory_delete

删除指定的记忆。

**参数：**
- `memory_ids` (必需): 要删除的记忆 ID 列表
- `user_id` (可选): 用户ID，默认从环境变量读取

## 配置选项

| 环境变量 | 说明 | 默认值 |
|---------|------|--------|
| `MEM0_BASE_URL` | Mem0 API 地址 | `https://api.mem0.ai` |
| `MEM0_API_KEY` | Mem0 API Key | - |
| `MEM0_API_MODE` | API 模式 (cloud/oss/auto) | `auto` |
| `MEMORY_DEFAULT_USER_ID` | 默认用户ID | `default` |
| `LOG_LEVEL` | 日志级别 | `INFO` |

## 项目结构

```
memory-mcp-server/
├── src/
│   ├── server.py              # MCP 服务器主文件
│   └── mem0_wrapper.py        # Mem0 客户端包装器
├── venv/                      # 虚拟环境 (安装后生成)
├── .env                       # 配置文件 (安装后生成)
├── .env.example               # 配置文件模板
├── requirements.txt           # Python 依赖
├── install.sh                 # 一键安装脚本
├── claude-code-launcher.sh    # Claude Code 启动脚本
├── add_memory.sh              # 添加记忆测试脚本
├── list_memory.sh             # 列出记忆测试脚本
├── search_memory.sh           # 搜索记忆测试脚本
└── README.md                  # 本文件
```

## 手动安装 (如安装脚本失败)

### 1. 安装依赖

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. 配置环境变量

```bash
cp .env.example .env
nano .env  # 编辑配置
```

### 3. 测试运行

```bash
source venv/bin/activate
python src/server.py
```

## 测试脚本

项目包含三个测试脚本,方便测试功能:

```bash
# 添加记忆
./add_memory.sh "我喜欢编程"

# 搜索记忆
./search_memory.sh "编程"

# 列出所有记忆
./list_memory.sh
```

## 故障排查

### 问题 1: Python 版本过低

需要 Python 3.8 或更高版本:

```bash
python3 --version
```

### 问题 2: 虚拟环境创建失败

安装 python3-venv:

```bash
# Ubuntu/Debian
sudo apt install python3-venv

# CentOS/RHEL
sudo yum install python3-venv

# macOS
brew install python3
```

### 问题 3: MCP 服务器未启动

检查日志:

```bash
# 查看服务器日志
source venv/bin/activate
python src/server.py
```

检查 Claude Code 配置:

```bash
cat ~/.claude.json | grep -A 10 memory
```

### 问题 4: 记忆未保存到云端

1. 检查 API Key 是否正确
2. 检查网络连接
3. 查看 `.env` 中的配置

## 多设备部署

要在多台电脑上共享记忆:

1. 在每台电脑上安装此服务器
2. **使用相同的 API Key**
3. **使用相同的 user_id**
4. 所有记忆将自动同步到云端

## 开发路线图

- [ ] 添加 SSE/HTTP 传输模式（支持远程连接）
- [ ] 添加记忆统计工具
- [ ] 添加记忆导出/导入功能
- [ ] Docker 镜像打包
- [ ] NPX 包发布

## License

MIT

## Credits

基于 OpenClaw 的 mem0_client.py 改造

## 支持

遇到问题? 检查:
1. Python 版本 >= 3.8
2. 虚拟环境已激活
3. `.env` 配置正确
4. API Key 有效
