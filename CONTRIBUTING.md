# 贡献指南

感谢你对 Memory MCP Server 的关注!

## 如何贡献

### 报告 Bug

1. 在 Issues 中搜索是否已有相关问题
2. 如果没有,创建新 Issue,包含:
   - 清晰的标题
   - 详细的问题描述
   - 复现步骤
   - 预期行为
   - 实际行为
   - 环境信息(OS, Python 版本等)

### 提交功能请求

1. 在 Issues 中描述你希望添加的功能
2. 说明使用场景和原因
3. 如果可能,提供实现思路

### 提交代码

1. Fork 本仓库
2. 创建你的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

### 代码规范

- 遵循 PEP 8 Python 代码风格
- 添加必要的注释和文档字符串
- 确保代码通过测试
- 更新相关文档

## 开发环境设置

```bash
# 克隆仓库
git clone https://github.com/your-username/memory-mcp-server.git
cd memory-mcp-server

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件
```

## 测试

```bash
# 测试服务器启动
python src/server.py

# 使用测试脚本
./add_memory.sh "测试记忆"
./search_memory.sh "测试"
./list_memory.sh
```

## 提交检查清单

提交 PR 前,请确保:

- [ ] 代码符合项目风格
- [ ] 已添加必要的测试
- [ ] 文档已更新
- [ ] 所有测试通过
- [ ] 没有合并冲突
- [ ] 提交信息清晰明确

## 行为准则

- 尊重他人
- 接受建设性批评
- 关注对社区最有利的事情
- 对不同观点表示同理心

## 许可证

通过贡献代码,你同意你的贡献将使用与项目相同的 MIT 许可证。
