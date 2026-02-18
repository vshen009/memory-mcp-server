# 故障排查指南

> **版本:** v1.0.0
> **更新:** 2026-02-18

---

## 目录

- [安装问题](#安装问题)
- [配置问题](#配置问题)
- [连接问题](#连接问题)
- [记忆问题](#记忆问题)
- [性能问题](#性能问题)
- [常见错误](#常见错误)

---

## 安装问题

### Python 版本过低

**错误:**
```
Python 3.7 is not supported
```

**原因:** Memory MCP Server 需要 Python 3.8+

**解决方案:**
```bash
# 检查版本
python3 --version

# 安装 Python 3.8+
# Ubuntu/Debian
sudo apt install python3.8

# macOS
brew install python@3.8

# CentOS/RHEL
sudo yum install python38
```

---

### 虚拟环境创建失败

**错误:**
```
Error: Command 'python3 -m venv venv' failed
```

**原因:** 缺少 python3-venv 模块

**解决方案:**
```bash
# Ubuntu/Debian
sudo apt install python3-venv

# CentOS/RHEL
sudo yum install python3-venv

# macOS
brew install python3
```

---

### 依赖安装失败

**错误:**
```
ERROR: Could not find a version that satisfies the requirement mcp
```

**原因:** pip 版本过低或网络问题

**解决方案:**
```bash
# 升级 pip
source venv/bin/activate
pip install --upgrade pip setuptools wheel

# 使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

---

## 配置问题

### API Key 无效

**错误:**
```
API error 401: Unauthorized
```

**原因:**
- API Key 错误
- API Key 过期
- API Key 格式不正确

**解决方案:**
```bash
# 1. 检查 .env 文件
cat .env | grep MEM0_API_KEY

# 2. 确认格式: m0-xxxx
# 正确: m0-your-api-key-here
# 错误: m0-keuN7KwXe... (被截断)

# 3. 重新生成 API Key
# 访问: https://platform.mem0.ai
```

---

### Claude Code 找不到工具

**症状:** 重启 Claude Code 后看不到 memory_* 工具

**检查清单:**
```bash
# 1. 验证配置文件
cat ~/.claude.json | python3 -m json.tool

# 2. 检查路径
ls -la /path/to/claude-code-launcher.sh

# 3. 测试启动脚本
/path/to/claude-code-launcher.sh
```

**解决方案:**
```json
// 确保配置格式正确
{
  "mcpServers": {
    "memory": {
      "type": "stdio",
      "command": "/绝对路径/claude-code-launcher.sh",  // 使用绝对路径
      "env": {
        "MEM0_API_KEY": "m0-your-key",
        "MEMORY_DEFAULT_USER_ID": "your-id"
      }
    }
  }
}
```

---

### user_id 不匹配

**症状:** 搜索结果为空

**原因:** user_id 与存储时不一致

**检查:**
```bash
# 查看 .env 中的配置
grep MEMORY_DEFAULT_USER_ID .env

# 查看记忆中的 user_id
./list_memory.sh | grep "user_id"
```

**解决方案:**
```bash
# 确保使用相同的 user_id
# 方式1: 修改 .env
MEMORY_DEFAULT_USER_ID=your-user-id

# 方式2: 调用时指定
./search_memory.sh "query" --user-id your-user-id
```

---

## 连接问题

### 网络超时

**错误:**
```
network_error: timeout
```

**原因:** 无法连接到 Mem0 Cloud API

**检查:**
```bash
# 1. 测试网络连接
ping api.mem0.ai

# 2. 测试 HTTPS
curl -I https://api.mem0.ai

# 3. 检查防火墙
sudo iptables -L | grep 443
```

**解决方案:**
```bash
# 配置代理（如果需要）
export https_proxy=http://proxy.example.com:8080

# 或使用本地 Mem0
MEM0_BASE_URL=http://localhost:8000
```

---

### SSL 证书错误

**错误:**
```
SSL: CERTIFICATE_VERIFY_FAILED
```

**原因:** SSL 证书问题

**解决方案:**
```bash
# 更新 ca-certificates
sudo apt install ca-certificates

# 或临时禁用验证（不推荐）
export PYTHONHTTPSVERIFY=0
```

---

## 记忆问题

### 记忆未保存

**症状:** 调用 memory_add 后搜索不到

**检查:**
```bash
# 1. 查看服务器日志
tail -f /path/to/memory-mcp-server.log

# 2. 验证 API 调用
curl -X POST https://api.mem0.ai/v1/memories/ \
  -H "Authorization: Token m0-your-key" \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "测试"}], "user_id": "test"}'
```

**可能原因:**
- API 调用失败
- 记忆还在处理中(PENDING)
- 搜索关键词不准确

---

### 搜索结果为空

**症状:** memory_search 返回 0 条结果

**检查:**
```bash
# 1. 列出所有记忆
./list_memory.sh | head -20

# 2. 使用更通用的关键词
./search_memory.sh "记忆"  # 而不是 "某件具体的事"
```

**优化搜索:**
```json
{
  "query": "Python 编程 开发",  // 多个关键词
  "top_k": 20,                  // 增加返回数量
  "scope": ""                   // 不过滤类别
}
```

---

### 记忆重复

**症状:** 搜索到多条相似的记忆

**解决方案:**
```bash
# 1. 列出所有记忆
./list_memory.sh > all-memories.txt

# 2. 查找重复
grep "相似内容" all-memories.txt

# 3. 删除重复的记忆ID
./delete_memory.sh id1,id2,id3
```

---

## 性能问题

### 搜索慢

**症状:** memory_search 响应时间 > 5秒

**优化:**
```json
{
  "top_k": 5,   // 减少返回数量
  "scope": "personal-details"  // 缩小搜索范围
}
```

---

### 内存占用高

**症状:** 服务器进程内存持续增长

**检查:**
```bash
# 查看进程内存
ps aux | grep server.py

# 查看内存限制
ulimit -a | grep memory
```

**解决方案:**
```bash
# 重启服务器
pkill -f "python.*server.py"
# Claude Code 会自动重启
```

---

## 常见错误

### error 400: Bad Request

**原因:** 请求参数错误

**检查:**
- `user_id` 是否为空
- `text` 是否包含特殊字符
- JSON 格式是否正确

---

### error 429: Too Many Requests

**原因:** 超过速率限制

**解决方案:**
```python
import time

# 实现退避重试
for attempt in range(3):
    try:
        result = client.search(...)
        break
    except Exception as e:
        if "429" in str(e):
            time.sleep(2 ** attempt)  # 1s, 2s, 4s
        else:
            raise
```

---

### error 500: Internal Server Error

**原因:** Mem0 Cloud 服务器错误

**解决方案:**
1. 等待几秒后重试
2. 查看 Mem0 状态页: https://status.mem0.ai
3. 报告问题: https://github.com/mem0ai/mem0/issues

---

## 调试技巧

### 启用详细日志

```bash
# 修改 .env
LOG_LEVEL=DEBUG

# 重启服务器
pkill -f "python.*server.py"
```

### 测试 API 连接

```bash
# 使用测试脚本
python test_client.py
```

### 查看原始请求

```bash
# 使用 tcpdump
sudo tcpdump -i any -A 'tcp port 443 and host api.mem0.ai'

# 或使用 curl
curl -v https://api.mem0.ai/v1/memories/
```

---

## 获取帮助

如果以上方法都无法解决问题:

1. **查看日志:**
   ```bash
   tail -100 ~/.claude-code/logs/mcp-*.log
   ```

2. **提交 Issue:**
   https://github.com/vshen009/memory-mcp-server/issues

3. **提供信息:**
   - 操作系统版本
   - Python 版本
   - 错误信息
   - 复现步骤

---

**相关文档:**
- [API 参考](./API_REFERENCE.md)
- [Claude Code 指南](./CLAUDE_CODE_GUIDE.md)
- [OpenClaw 集成](./OPENCLOW_INTEGRATION.md)
