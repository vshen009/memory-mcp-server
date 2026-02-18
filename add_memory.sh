#!/bin/bash
# 添加记忆的便捷脚本
# 用法: ./add_memory.sh "记忆内容"

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 激活虚拟环境
source venv/bin/activate

# 添加记忆
python3 -c "
import sys
sys.path.insert(0, 'src')
from mem0_wrapper import Mem0Client
from datetime import datetime
import json

client = Mem0Client()

if len(sys.argv) < 2:
    print('用法: ./add_memory.sh \"记忆内容\"')
    sys.exit(1)

memory_text = sys.argv[1]

result = client.add(
    text=memory_text,
    user_id='vincent-main',
    metadata={
        'scope': 'manual',
        'source': 'add_memory.sh',
        'timestamp': datetime.now().isoformat()
    }
)

print('✓ 记忆添加成功！')
print(f'内容: {memory_text}')
print()
print('API 响应:')
print(json.dumps(result, indent=2, ensure_ascii=False))
" "$@"
