#!/usr/bin/env python3
"""
Memory MCP Server 测试脚本
直接测试 Mem0 客户端功能，不通过 MCP
"""

import sys
import json
from pathlib import Path

# 添加 src 目录到路径
sys.path.insert(0, str(Path(__file__).parent / "src"))

from mem0_wrapper import Mem0Client


def test_mem0_client():
    """测试 Mem0 客户端基本功能"""
    print("=" * 60)
    print("Memory MCP Server - 客户端测试")
    print("=" * 60)

    # 初始化客户端
    print("\n1. 初始化客户端...")
    client = Mem0Client()
    print(f"   ✓ API Base: {client.api_base}")
    print(f"   ✓ API Mode: {client.api_mode}")

    # 测试用户 ID
    test_user_id = "test-user-cli"

    # 测试添加记忆
    print("\n2. 测试添加记忆...")
    test_memory = {
        "text": "这是一个测试记忆：用户喜欢使用 Claude 和 OpenAI 的 AI 模型进行开发工作",
        "user_id": test_user_id,
        "metadata": {
            "scope": "test",
            "source": "test-script",
            "category": "preferences"
        }
    }

    try:
        result = client.add(**test_memory)
        print(f"   ✓ 添加成功")
        print(f"   结果: {json.dumps(result, ensure_ascii=False, indent=2)}")

        # 保存记忆 ID（如果有）
        if "results" in result and len(result["results"]) > 0:
            memory_id = result["results"][0].get("id")
            if memory_id:
                print(f"   记忆 ID: {memory_id}")
    except Exception as e:
        print(f"   ✗ 添加失败: {e}")
        return False

    # 测试搜索记忆
    print("\n3. 测试搜索记忆...")
    try:
        results = client.search(
            query="用户喜欢什么 AI 模型？",
            user_id=test_user_id,
            top_k=3
        )
        print(f"   ✓ 搜索成功，找到 {len(results)} 条结果")
        for i, r in enumerate(results, 1):
            memory_text = r.get("memory", r.get("text", "N/A"))
            score = r.get("score", 0)
            print(f"   {i}. [{score:.2f}] {memory_text}")
    except Exception as e:
        print(f"   ✗ 搜索失败: {e}")
        return False

    # 测试列出记忆
    print("\n4. 测试列出记忆...")
    try:
        memories = client.list(
            user_id=test_user_id,
            limit=10
        )
        print(f"   ✓ 列出成功，共 {len(memories)} 条记忆")
        for i, m in enumerate(memories[:5], 1):
            memory_text = m.get("memory", m.get("text", "N/A"))
            print(f"   {i}. {memory_text[:60]}...")
    except Exception as e:
        print(f"   ✗ 列出失败: {e}")
        return False

    # 测试不同 scope 的记忆
    print("\n5. 测试添加不同 scope 的记忆...")
    scopes = ["work", "personal", "coding"]
    for scope in scopes:
        try:
            client.add(
                text=f"这是 {scope} 范围的记忆：用户在 {scope} 方面有特定偏好",
                user_id=test_user_id,
                metadata={"scope": scope}
            )
            print(f"   ✓ 已添加 '{scope}' 记忆")
        except Exception as e:
            print(f"   ✗ 添加 '{scope}' 失败: {e}")

    # 测试范围搜索
    print("\n6. 测试范围搜索...")
    try:
        results = client.search(
            query="用户的偏好",
            user_id=test_user_id,
            scope="coding",
            top_k=5
        )
        print(f"   ✓ 范围搜索成功，找到 {len(results)} 条 coding 范围的记忆")
        for i, r in enumerate(results, 1):
            memory_text = r.get("memory", r.get("text", "N/A"))
            print(f"   {i}. {memory_text}")
    except Exception as e:
        print(f"   ✗ 范围搜索失败: {e}")

    print("\n" + "=" * 60)
    print("✓ 所有测试完成！")
    print("=" * 60)
    return True


if __name__ == "__main__":
    try:
        success = test_mem0_client()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n测试中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n测试出错: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
