# Memory MCP Server - 部署到新电脑

## 快速部署步骤

### 1. 复制项目

```bash
# 方法 A：使用 rsync（推荐）
rsync -avz /home/trinity/happpy/memory-mcp-server/ user@new-computer:/path/to/memory-mcp-server/

# 方法 B：使用 scp
scp -r /home/trinity/happpy/memory-mcp-server user@new-computer:/path/to/

# 方法 C：打包后传输
cd /home/trinity/happpy
tar czf memory-mcp-server.tar.gz memory-mcp-server/
# 然后复制 memory-mcp-server.tar.gz 到新电脑并解压
```

### 2. 在新电脑上设置

```bash
# 进入项目目录
cd /path/to/memory-mcp-server

# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

### 3. 配置环境变量

```bash
# 复制配置模板
cp .env.example .env

# 编辑配置
nano .env  # 或使用其他编辑器
```

**重要配置项：**
```env
# 方案 1：共享记忆（使用相同的 API Key 和 user_id）
MEM0_API_KEY=m0-your-api-key-here
MEMORY_DEFAULT_USER_ID=your-user-id

# 方案 2：独立记忆（使用不同的 user_id）
MEM0_API_KEY=m0-your-api-key-here
MEMORY_DEFAULT_USER_ID=vicnet-work
```

### 4. 测试

```bash
# 确保虚拟环境已激活
source venv/bin/activate

# 运行测试
python test_client.py
```

### 5. 配置 AI 客户端

#### Claude Code (Linux/Mac)

编辑 `~/.claude_code_config.json`：

```json
{
  "mcpServers": {
    "memory": {
      "command": "python",
      "args": ["/path/to/memory-mcp-server/src/server.py"],
      "env": {
        "MEM0_API_KEY": "m0-your-api-key-here",
        "MEMORY_DEFAULT_USER_ID": "your-user-id"
      }
    }
  }
}
```

#### Claude Code (Windows)

编辑 `%USERPROFILE%\.claude_code_config.json`：

```json
{
  "mcpServers": {
    "memory": {
      "command": "python",
      "args": ["C:\\path\\to\\memory-mcp-server\\src\\server.py"],
      "env": {
        "MEM0_API_KEY": "m0-your-api-key-here",
        "MEMORY_DEFAULT_USER_ID": "your-user-id"
      }
    }
  }
}
```

---

## 部署模式

### 模式 1：完全共享记忆

**配置：** 所有电脑使用相同的 `user_id`

**特点：**
- ✅ 所有设备看到相同的记忆
- ✅ 在任何设备添加的记忆，其他设备都能访问
- ❌ 无法区分不同设备

**适用场景：** 个人多设备使用

### 模式 2：设备隔离记忆

**配置：** 每台设备使用不同的 `user_id`

**特点：**
- ✅ 每台设备有独立的记忆空间
- ✅ 可以选择性共享特定记忆
- ❌ 需要手动管理不同设备的记忆

**适用场景：** 工作/个人电脑分离

### 模式 3：混合模式

**配置：** 使用不同的 `user_id` + 共享 API Key

**特点：**
- ✅ 可以搜索所有记忆（需要修改工具）
- ✅ 可以添加到特定用户
- ⚠️ 需要自定义实现

**适用场景：** 高级用户

---

## 环境检查清单

在部署到新电脑前，确认：

- [ ] Python 3.8+ 已安装
- [ ] pip 可用
- [ ] 网络连接正常（需要访问 Mem0 Cloud API）
- [ ] 有 Mem0 API Key
- [ ] AI 客户端支持 MCP（Claude Code 0.6+）

---

## 常见问题

### Q1: Windows 上 Python 路径不同

**解决方法：** 在配置中使用 `python.exe` 而不是 `python`

```json
{
  "command": "python.exe",
  "args": ["C:\\path\\to\\src\\server.py"]
}
```

### Q2: 虚拟环境激活失败

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

### Q3: MCP 服务器无法启动

**检查：**
1. 虚拟环境是否激活
2. 依赖是否安装：`pip list | grep mcp`
3. 配置文件是否存在：`ls .env`
4. 手动运行测试：`python test_client.py`

### Q4: 记忆不同步

**原因：**
- 使用了不同的 `user_id`
- Mem0 Cloud 异步处理延迟（通常 5-10 秒）

**解决方法：**
- 确认所有设备使用相同的 `user_id`
- 等待几秒后重新搜索

---

## 一键部署脚本

创建 `deploy.sh`（适用于 Linux/Mac）：

```bash
#!/bin/bash
set -e

echo "Memory MCP Server - 一键部署"
echo "================================"

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到 python3"
    exit 1
fi

echo "✓ Python 版本: $(python3 --version)"

# 创建虚拟环境
echo ""
echo "创建虚拟环境..."
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
echo ""
echo "安装依赖..."
pip install -r requirements.txt

# 检查配置
if [ ! -f ".env" ]; then
    echo ""
    echo "警告: 未找到 .env 文件"
    echo "请复制 .env.example 为 .env 并配置"
    echo ""
    echo "  cp .env.example .env"
    echo "  nano .env"
    exit 1
fi

echo "✓ 配置文件存在"

# 测试
echo ""
echo "运行测试..."
python test_client.py

echo ""
echo "================================"
echo "✓ 部署完成！"
echo ""
echo "下一步：配置 AI 客户端"
echo "  Claude Code: 编辑 ~/.claude_code_config.json"
```

使用方法：
```bash
chmod +x deploy.sh
./deploy.sh
```

---

## 下一步

部署完成后，查看 [USAGE.md](./USAGE.md) 了解如何使用。
