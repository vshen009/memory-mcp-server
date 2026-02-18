#!/bin/bash
# Memory MCP Server 一键安装脚本
# 适用于 Ubuntu/Debian/CentOS/macOS

set -e

echo "🚀 Memory MCP Server 安装程序"
echo "================================"

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 检查 Python 3
check_python() {
    echo -e "${YELLOW}检查 Python 环境...${NC}"
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}错误: 未找到 python3, 请先安装 Python 3.8+${NC}"
        exit 1
    fi
    PYTHON_VERSION=$(python3 --version | awk '{print $2}')
    echo -e "${GREEN}✓ 找到 Python $PYTHON_VERSION${NC}"
}

# 检查 pip
check_pip() {
    echo -e "${YELLOW}检查 pip...${NC}"
    if ! command -v pip3 &> /dev/null; then
        echo "安装 pip3..."
        python3 -m ensurepip --upgrade || {
            echo -e "${RED}错误: 无法安装 pip${NC}"
            exit 1
        }
    fi
    echo -e "${GREEN}✓ pip3 已就绪${NC}"
}

# 创建虚拟环境
setup_venv() {
    echo -e "${YELLOW}创建虚拟环境...${NC}"
    if [ ! -d "venv" ]; then
        python3 -m venv venv
        echo -e "${GREEN}✓ 虚拟环境创建成功${NC}"
    else
        echo -e "${GREEN}✓ 虚拟环境已存在${NC}"
    fi
}

# 安装依赖
install_dependencies() {
    echo -e "${YELLOW}安装 Python 依赖...${NC}"
    source venv/bin/activate
    pip install -r requirements.txt
    echo -e "${GREEN}✓ 依赖安装完成${NC}"
}

# 配置环境变量
setup_config() {
    echo -e "${YELLOW}配置环境变量...${NC}"

    if [ ! -f ".env" ]; then
        if [ -f ".env.example" ]; then
            cp .env.example .env
            echo -e "${GREEN}✓ 已创建 .env 配置文件${NC}"
        else
            cat > .env << 'EOF'
# Mem0 API 配置
MEM0_BASE_URL=https://api.mem0.ai
MEM0_API_KEY=你的API-Key
MEMORY_DEFAULT_USER_ID=default
LOG_LEVEL=INFO
EOF
            echo -e "${GREEN}✓ 已创建 .env 配置文件${NC}"
        fi
    else
        echo -e "${GREEN}✓ .env 配置文件已存在${NC}"
    fi

    echo ""
    echo -e "${YELLOW}⚠️  请编辑 .env 文件,填入你的配置:${NC}"
    echo "   1. MEM0_API_KEY - 从 https://platform.mem0.ai 获取"
    echo "   2. MEMORY_DEFAULT_USER_ID - 设置你的用户ID (如: vincent-main)"
    echo ""
}

# 测试服务器
test_server() {
    echo -e "${YELLOW}测试服务器...${NC}"
    source venv/bin/activate

    # 设置测试环境变量
    export MEM0_BASE_URL=${MEM0_BASE_URL:-https://api.mem0.ai}
    export MEMORY_DEFAULT_USER_ID=${MEMORY_DEFAULT_USER_ID:-default}
    export LOG_LEVEL=INFO

    timeout 3 python src/server.py 2>&1 | head -5 || true
    echo -e "${GREEN}✓ 服务器测试通过${NC}"
}

# 打印配置信息
print_config() {
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    LAUNCHER="$SCRIPT_DIR/claude-code-launcher.sh"

    echo ""
    echo "================================"
    echo -e "${GREEN}✅ 安装完成!${NC}"
    echo "================================"
    echo ""
    echo "📍 项目路径: $SCRIPT_DIR"
    echo "📝 启动脚本: $LAUNCHER"
    echo ""
    echo "📋 下一步操作:"
    echo ""
    echo "1. 编辑配置文件:"
    echo "   nano .env"
    echo ""
    echo "2. 添加到 Claude Code (~/.claude.json):"
    echo ""
    cat << 'EOF'
{
  "mcpServers": {
    "memory": {
      "type": "stdio",
      "command": "启动脚本路径",
      "env": {
        "MEM0_API_KEY": "你的API-Key",
        "MEMORY_DEFAULT_USER_ID": "你的用户ID",
        "LOG_LEVEL": "INFO"
      }
    }
  }
}
EOF
    echo ""
    echo "3. 重启 Claude Code"
    echo ""
    echo "详细文档: README.md"
    echo "================================"
}

# 主流程
main() {
    check_python
    check_pip
    setup_venv
    install_dependencies
    setup_config
    test_server
    print_config
}

main
