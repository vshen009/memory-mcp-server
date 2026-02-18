#!/usr/bin/env python3
"""
Memory MCP Server - 最小可用版本
统一的内存管理 MCP 服务器，支持 Mem0 Cloud API
"""

import asyncio
import json
import logging
import os
import sys
from pathlib import Path
from datetime import datetime

# MCP SDK imports
from mcp.server.fastmcp import FastMCP

# 导入 mem0 客户端
sys.path.insert(0, str(Path(__file__).parent))
from mem0_wrapper import Mem0Client

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 创建 MCP 服务器
mcp = FastMCP("memory-mcp-server")

# 全局 mem0 客户端
_mem0_client = None

def get_default_user_id():
    """从环境变量获取默认用户ID"""
    return os.getenv("MEMORY_DEFAULT_USER_ID", "default")

def get_mem0_client():
    """获取或创建 mem0 客户端实例"""
    global _mem0_client
    if _mem0_client is None:
        _mem0_client = Mem0Client()
    return _mem0_client


@mcp.tool(description="添加新记忆。当用户提供关于自己、偏好、或任何未来可能有用的信息时调用此方法。用户也可以主动要求记住某些事情。")
async def memory_add(
    text: str,
    user_id: str = None,
    scope: str = "general",
    source: str = "mcp-server"
) -> str:
    # 使用环境变量中的默认用户ID
    if user_id is None:
        user_id = get_default_user_id()
    """
    添加一条新的记忆

    Args:
        text: 要记住的文本内容
        user_id: 用户ID（默认: default）
        scope: 记忆范围/类别（默认: general）
        source: 来源标识（默认: mcp-server）

    Returns:
        JSON 格式的响应结果
    """
    try:
        client = get_mem0_client()
        result = client.add(
            text=text,
            user_id=user_id,
            metadata={
                "scope": scope,
                "source": source,
                "timestamp": datetime.now().isoformat()
            }
        )
        return json.dumps({
            "success": True,
            "result": result,
            "message": "记忆添加成功"
        }, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"添加记忆失败: {e}")
        return json.dumps({
            "success": False,
            "error": str(e),
            "message": "记忆添加失败"
        }, ensure_ascii=False, indent=2)


@mcp.tool(description="搜索已存储的记忆。每次用户提问时都应该调用此方法来查找相关信息。")
async def memory_search(
    query: str,
    user_id: str = None,
    top_k: int = 5,
    scope: str = ""
) -> str:
    # 使用环境变量中的默认用户ID
    if user_id is None:
        user_id = get_default_user_id()
    """
    搜索记忆

    Args:
        query: 搜索查询（自然语言问题）
        user_id: 用户ID（默认: default）
        top_k: 返回结果数量（默认: 5）
        scope: 可选的范围过滤

    Returns:
        JSON 格式的搜索结果
    """
    try:
        client = get_mem0_client()
        result = client.search(
            query=query,
            user_id=user_id,
            top_k=top_k,
            scope=scope
        )
        return json.dumps({
            "success": True,
            "results": result,
            "count": len(result) if isinstance(result, list) else 0,
            "message": f"找到 {len(result) if isinstance(result, list) else 0} 条相关记忆"
        }, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"搜索记忆失败: {e}")
        return json.dumps({
            "success": False,
            "error": str(e),
            "message": "搜索记忆失败"
        }, ensure_ascii=False, indent=2)


@mcp.tool(description="列出用户的所有记忆。用于查看或批量处理记忆。")
async def memory_list(
    user_id: str = None,
    scope: str = "",
    limit: int = 20
) -> str:
    # 使用环境变量中的默认用户ID
    if user_id is None:
        user_id = get_default_user_id()
    """
    列出所有记忆

    Args:
        user_id: 用户ID（默认: default）
        scope: 可选的范围过滤
        limit: 返回结果数量限制（默认: 20）

    Returns:
        JSON 格式的记忆列表
    """
    try:
        client = get_mem0_client()
        result = client.list(
            user_id=user_id,
            scope=scope,
            limit=limit
        )
        return json.dumps({
            "success": True,
            "results": result,
            "count": len(result) if isinstance(result, list) else 0,
            "message": f"共 {len(result) if isinstance(result, list) else 0} 条记忆"
        }, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"列出记忆失败: {e}")
        return json.dumps({
            "success": False,
            "error": str(e),
            "message": "列出记忆失败"
        }, ensure_ascii=False, indent=2)


@mcp.tool(description="删除指定的记忆。提供记忆 ID 列表来删除特定记忆。")
async def memory_delete(
    memory_ids: list[str],
    user_id: str = None
) -> str:
    # 使用环境变量中的默认用户ID
    if user_id is None:
        user_id = get_default_user_id()
    """
    删除记忆

    Args:
        memory_ids: 要删除的记忆 ID 列表
        user_id: 用户ID（默认: default）

    Returns:
        JSON 格式的删除结果
    """
    try:
        client = get_mem0_client()
        deleted_count = 0
        errors = []

        for memory_id in memory_ids:
            try:
                client.delete(memory_id)
                deleted_count += 1
            except Exception as e:
                errors.append(f"{memory_id}: {str(e)}")

        return json.dumps({
            "success": True,
            "deleted_count": deleted_count,
            "errors": errors,
            "message": f"成功删除 {deleted_count} 条记忆"
        }, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"删除记忆失败: {e}")
        return json.dumps({
            "success": False,
            "error": str(e),
            "message": "删除记忆失败"
        }, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    logger.info("🚀 Memory MCP Server 启动中...")
    logger.info(f"📝 Mem0 API Base: {os.getenv('MEM0_BASE_URL', 'https://api.mem0.ai')}")
    logger.info(f"👤 默认用户: {os.getenv('MEMORY_DEFAULT_USER_ID', 'default')}")

    # 使用 stdio 传输（FastMCP 会自动检测）
    mcp.run()
