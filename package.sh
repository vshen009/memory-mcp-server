#!/bin/bash
# 打包脚本 - 创建发布包

set -e

VERSION="1.0.0"
PACKAGE_NAME="memory-mcp-server-${VERSION}"
DIST_DIR="dist"

echo "📦 打包 Memory MCP Server v${VERSION}"

# 清理旧的打包
rm -rf "$DIST_DIR"
mkdir -p "$DIST_DIR"

# 创建临时目录
TMP_DIR="$DIST_DIR/$PACKAGE_NAME"
rm -rf "$TMP_DIR"
mkdir -p "$TMP_DIR"

echo "📋 复制文件..."

# 复制必要文件
cp -r src "$TMP_DIR/"
cp requirements.txt "$TMP_DIR/"
cp .env.example "$TMP_DIR/"
cp install.sh "$TMP_DIR/"
cp claude-code-launcher.sh "$TMP_DIR/"
cp codex-launcher.sh "$TMP_DIR/"
cp add_memory.sh "$TMP_DIR/"
cp list_memory.sh "$TMP_DIR/"
cp search_memory.sh "$TMP_DIR/"
cp README.md "$TMP_DIR/"
cp deploy.md "$TMP_DIR/" 2>/dev/null || true
cp TOOLS_GUIDE.md "$TMP_DIR/" 2>/dev/null || true

# 添加执行权限
chmod +x "$TMP_DIR/install.sh"
chmod +x "$TMP_DIR/claude-code-launcher.sh"
chmod +x "$TMP_DIR/codex-launcher.sh"
chmod +x "$TMP_DIR/add_memory.sh"
chmod +x "$TMP_DIR/list_memory.sh"
chmod +x "$TMP_DIR/search_memory.sh"

# 创建压缩包
echo "🗜️  创建压缩包..."
cd "$DIST_DIR"
tar -czf "${PACKAGE_NAME}.tar.gz" "$PACKAGE_NAME"
cd - > /dev/null

# 计算校验和
echo "🔐 计算校验和..."
cd "$DIST_DIR"
sha256sum "${PACKAGE_NAME}.tar.gz" > "${PACKAGE_NAME}.tar.gz.sha256"
cd - > /dev/null

echo ""
echo "✅ 打包完成!"
echo ""
echo "📁 发布文件:"
echo "   $DIST_DIR/${PACKAGE_NAME}.tar.gz"
echo "   $DIST_DIR/${PACKAGE_NAME}.tar.gz.sha256"
echo ""
echo "📊 文件大小:"
du -h "$DIST_DIR/${PACKAGE_NAME}.tar.gz" | awk '{print "   " $1}'
echo ""
echo "📋 SHA256 校验和:"
cat "$DIST_DIR/${PACKAGE_NAME}.tar.gz.sha256" | awk '{print "   " $1 "  " $2}'
echo ""
echo "💡 发送文件:"
echo "   邮件附件: $DIST_DIR/${PACKAGE_NAME}.tar.gz"
echo "   或者用以下命令发送:"
echo "   echo \"见附件\" | mail -a $DIST_DIR/${PACKAGE_NAME}.tar.gz -s \"Memory MCP Server v${VERSION}\" recipient@example.com"
