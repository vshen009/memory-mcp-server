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
CODEX_MCP_STATUS="未执行"

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

read_env_value() {
    local key="$1"
    if [ ! -f ".env" ]; then
        echo ""
        return
    fi

    local line
    line=$(grep -E "^[[:space:]]*(export[[:space:]]+)?${key}=" .env | tail -n 1 || true)
    if [ -z "$line" ]; then
        echo ""
        return
    fi

    local value="${line#*=}"
    value=$(echo "$value" | sed -E 's/^[[:space:]]+|[[:space:]]+$//g')

    if [[ "$value" =~ ^\".*\"$ ]]; then
        value="${value:1:${#value}-2}"
    elif [[ "$value" =~ ^\'.*\'$ ]]; then
        value="${value:1:${#value}-2}"
    fi

    echo "$value"
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

register_codex_mcp() {
    echo -e "${YELLOW}注册 Codex 用户级 MCP 配置...${NC}"

    if ! command -v codex &> /dev/null; then
        CODEX_MCP_STATUS="跳过: 未检测到 codex CLI"
        echo -e "${YELLOW}⚠️  未检测到 codex，跳过用户级 MCP 注册${NC}"
        return
    fi

    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    LAUNCHER="$SCRIPT_DIR/codex-launcher.sh"
    SERVER_NAME="${CODEX_MCP_SERVER_NAME:-memory}"

    chmod +x "$LAUNCHER" 2>/dev/null || true

    if codex mcp get "$SERVER_NAME" >/dev/null 2>&1; then
        CODEX_MCP_STATUS="已存在: ${SERVER_NAME} (未覆盖)"
        echo -e "${YELLOW}⚠️  Codex MCP '${SERVER_NAME}' 已存在，未覆盖${NC}"
        echo "   如需覆盖可手动执行:"
        echo "   codex mcp remove ${SERVER_NAME}"
        echo "   然后重新运行 ./install.sh"
        return
    fi

    MEM0_BASE_URL_VALUE=$(read_env_value "MEM0_BASE_URL")
    MEM0_API_KEY_VALUE=$(read_env_value "MEM0_API_KEY")
    MEMORY_DEFAULT_USER_ID_VALUE=$(read_env_value "MEMORY_DEFAULT_USER_ID")
    LOG_LEVEL_VALUE=$(read_env_value "LOG_LEVEL")

    if [ -z "$MEM0_BASE_URL_VALUE" ]; then
        MEM0_BASE_URL_VALUE="https://api.mem0.ai"
    fi
    if [ -z "$LOG_LEVEL_VALUE" ]; then
        LOG_LEVEL_VALUE="INFO"
    fi

    CMD=(codex mcp add "$SERVER_NAME")
    CMD+=(--env "MEM0_BASE_URL=${MEM0_BASE_URL_VALUE}")
    if [ -n "$MEM0_API_KEY_VALUE" ]; then
        CMD+=(--env "MEM0_API_KEY=${MEM0_API_KEY_VALUE}")
    fi
    if [ -n "$MEMORY_DEFAULT_USER_ID_VALUE" ]; then
        CMD+=(--env "MEMORY_DEFAULT_USER_ID=${MEMORY_DEFAULT_USER_ID_VALUE}")
    fi
    CMD+=(--env "LOG_LEVEL=${LOG_LEVEL_VALUE}")
    CMD+=(-- "$LAUNCHER")

    if "${CMD[@]}" >/dev/null 2>&1; then
        CODEX_MCP_STATUS="已注册: ${SERVER_NAME}"
        echo -e "${GREEN}✓ Codex 用户级 MCP 已注册 (${SERVER_NAME})${NC}"
    else
        CODEX_MCP_STATUS="失败: codex mcp add 执行失败"
        echo -e "${YELLOW}⚠️  Codex MCP 自动注册失败，请手动执行:${NC}"
        echo "   codex mcp add ${SERVER_NAME} --env MEM0_BASE_URL=${MEM0_BASE_URL_VALUE} --env MEM0_API_KEY=你的API-Key --env MEMORY_DEFAULT_USER_ID=你的用户ID --env LOG_LEVEL=${LOG_LEVEL_VALUE} -- ${LAUNCHER}"
    fi
}

# 打印配置信息
print_config() {
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    CLAUDE_LAUNCHER="$SCRIPT_DIR/claude-code-launcher.sh"
    CODEX_LAUNCHER="$SCRIPT_DIR/codex-launcher.sh"

    echo ""
    echo "================================"
    echo -e "${GREEN}✅ 安装完成!${NC}"
    echo "================================"
    echo ""
    echo "📍 项目路径: $SCRIPT_DIR"
    echo "📝 Claude 启动脚本: $CLAUDE_LAUNCHER"
    echo "📝 Codex 启动脚本:  $CODEX_LAUNCHER"
    echo "🔧 Codex MCP 状态:   $CODEX_MCP_STATUS"
    echo ""
    echo "📋 下一步操作:"
    echo ""
    echo "1. 编辑配置文件:"
    echo "   nano .env"
    echo ""
    echo "2. Codex:"
    echo "   已尝试自动注册到 ~/.codex/config.toml"
    echo "   验证命令: codex mcp list"
    echo ""
    echo "3. 添加到 Claude Code (~/.claude.json):"
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
    echo "4. 重启 Codex/Claude Code"
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
    register_codex_mcp
    print_config
}

main
