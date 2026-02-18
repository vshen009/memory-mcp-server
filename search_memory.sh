#!/bin/bash
# 搜索记忆的便捷脚本
# 用法: ./search_memory.sh "搜索关键词" [返回数量]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 激活虚拟环境
source venv/bin/activate

# 设置默认返回数量
TOP_K=${2:-5}

# 搜索记忆
python3 -c "
import sys
sys.path.insert(0, 'src')
from mem0_wrapper import Mem0Client
import json

client = Mem0Client()

if len(sys.argv) < 2:
    print('用法: ./search_memory.sh \"搜索关键词\" [返回数量]')
    print('示例: ./search_memory.sh \"Vincent 的偏好\" 10')
    sys.exit(1)

query = sys.argv[1]
top_k = int(sys.argv[2]) if len(sys.argv) > 2 else 5

results = client.search(
    query=query,
    user_id='vincent-main',
    top_k=top_k
)

print(f'找到 {len(results)} 条相关记忆:')
print('=' * 60)

for i, r in enumerate(results, 1):
    memory = r.get('memory', r.get('text', 'N/A'))
    score = r.get('score', 0)
    print(f'{i}. [{score:.2f}] {memory}')

print('=' * 60)
" "$@"
