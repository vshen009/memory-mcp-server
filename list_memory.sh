#!/bin/bash
# 列出所有记忆的便捷脚本
# 用法: ./list_memory.sh [数量限制]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 激活虚拟环境
source venv/bin/activate

# 设置默认数量限制
LIMIT=${1:-20}

# 列出记忆
python3 -c "
import sys
sys.path.insert(0, 'src')
from mem0_wrapper import Mem0Client
import json

client = Mem0Client()

limit = int(sys.argv[1]) if len(sys.argv) > 1 else 20

results = client.list(
    user_id='vincent-main',
    limit=limit
)

print(f'共 {len(results)} 条记忆 (最新 {min(limit, len(results))} 条):')
print('=' * 60)

for i, r in enumerate(results[:limit], 1):
    memory = r.get('memory', r.get('text', 'N/A'))
    created_at = r.get('created_at', 'N/A')[:10]
    print(f'{i}. [{created_at}] {memory[:80]}...' if len(memory) > 80 else f'{i}. [{created_at}] {memory}')

print('=' * 60)
" "$@"
