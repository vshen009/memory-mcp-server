#!/bin/bash
# Memory MCP Server 启动脚本

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "================================"
echo "Memory MCP Server"
echo "================================"
echo ""

# 检查 Python 版本
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到 python3"
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
echo "Python 版本: $PYTHON_VERSION"

# 检查依赖
echo ""
echo "检查依赖..."
if ! python3 -c "import mcp" 2>/dev/null; then
    echo "未找到 MCP 依赖，正在安装..."
    pip install -r requirements.txt
fi

echo "✓ 依赖检查完成"

# 检查配置
if [ ! -f ".env" ]; then
    echo ""
    echo "警告: 未找到 .env 文件"
    echo "请复制 .env.example 为 .env 并配置你的 API Key"
    echo ""
    echo "  cp .env.example .env"
    echo ""
    echo "然后编辑 .env 文件，设置 MEM0_API_KEY"
    exit 1
fi

echo ""
echo "启动 MCP Server..."
echo ""

# 启动服务器
python3 src/server.py
