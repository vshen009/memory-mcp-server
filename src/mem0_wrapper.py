#!/usr/bin/env python3
"""
Mem0 客户端包装器
基于 OpenClaw 的 mem0_client.py，简化为 MCP 服务器专用版本
"""

import json
import os
import sys
import urllib.request
import urllib.error
import urllib.parse
from pathlib import Path


class Mem0Client:
    """简化的 Mem0 客户端"""

    def __init__(self):
        """初始化客户端，从环境变量读取配置"""
        self.api_base = self._load_env_var("MEM0_BASE_URL", "https://api.mem0.ai").rstrip("/")
        self.api_key = self._load_env_var("MEM0_API_KEY", "")
        self.api_mode = self._detect_mode()

        # 验证配置
        if "api.mem0.ai" in self.api_base and not self.api_key:
            print("ERROR: MEM0_API_KEY is required for Mem0 Cloud endpoint.", file=sys.stderr)
            sys.exit(2)

    def _load_env_file(self):
        """加载 .env 文件"""
        env_paths = [
            Path.cwd() / ".env",
            Path.home() / ".openclaw" / "workspace" / ".env",
            Path(__file__).parent.parent / ".env",
        ]

        for env_path in env_paths:
            if env_path.exists():
                self._parse_env_file(env_path)
                break

    def _parse_env_file(self, env_path):
        """解析 .env 文件"""
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            if key.startswith("export "):
                key = key[len("export "):].strip()
            # 解析引号
            value = value.strip()
            if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
                value = value[1:-1]

            os.environ.setdefault(key, value)

    def _load_env_var(self, key, default=""):
        """加载环境变量（支持 .env 文件）"""
        if not os.getenv(key):
            self._load_env_file()
        return os.getenv(key, default).strip()

    def _detect_mode(self):
        """检测 API 模式（cloud 或 oss）"""
        mode = self._load_env_var("MEM0_API_MODE", "auto").strip().lower()
        if mode in {"cloud", "oss"}:
            return mode
        if mode != "auto":
            print(f"WARN: unknown MEM0_API_MODE, fallback to auto", file=sys.stderr)
        return "cloud" if "api.mem0.ai" in self.api_base else "oss"

    def _call(self, path, payload=None, method="POST", query=None):
        """
        调用 Mem0 API

        Args:
            path: API 路径
            payload: 请求体（字典）
            method: HTTP 方法
            query: 查询参数（字典）

        Returns:
            (status_code, response_text, error_message)
        """
        body = None

        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Token {self.api_key}"

        if payload is not None:
            body = json.dumps(payload, ensure_ascii=False).encode("utf-8")

        url = f"{self.api_base}{path}"
        if query:
            url = f"{url}?{urllib.parse.urlencode(query)}"

        req = urllib.request.Request(url, data=body, headers=headers, method=method)

        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                text = resp.read().decode("utf-8", errors="replace")
                return resp.status, text, None
        except urllib.error.HTTPError as e:
            text = e.read().decode("utf-8", errors="replace")
            return e.code, text, None
        except urllib.error.URLError as e:
            reason = getattr(e, "reason", e)
            return None, "", f"network_error: {reason}"
        except Exception as e:
            return None, "", f"unexpected_error: {type(e).__name__}: {e}"

    def add(self, text: str, user_id: str = "default", metadata: dict = None):
        """
        添加记忆

        Args:
            text: 记忆内容
            user_id: 用户ID
            metadata: 元数据字典

        Returns:
            API 响应结果
        """
        payload = {
            "messages": [{"role": "user", "content": text}],
            "user_id": user_id,
            "metadata": metadata or {},
        }

        add_path = "/v1/memories/" if self.api_mode == "cloud" else "/memories"
        code, text, err = self._call(add_path, payload)

        if err:
            raise Exception(err)

        if code >= 400:
            raise Exception(f"API error {code}: {text}")

        return json.loads(text)

    def search(self, query: str, user_id: str = "default", top_k: int = 5, scope: str = ""):
        """
        搜索记忆

        Args:
            query: 搜索查询
            user_id: 用户ID
            top_k: 返回结果数量
            scope: 保留参数（暂不用于过滤，会存储在 metadata 中）

        Returns:
            搜索结果列表
        """
        if self.api_mode == "cloud":
            payload = {
                "query": query,
                "filters": {"AND": [{"user_id": user_id}]},
                "top_k": top_k,
            }
            # 注意：scope 参数暂不用于 Cloud API 过滤
            code, text, err = self._call("/v2/memories/search/", payload)
        else:
            payload = {
                "query": query,
                "user_id": user_id,
                "top_k": top_k,
            }
            if scope:
                payload["scope"] = scope
            code, text, err = self._call("/memories/search", payload)

        if err:
            raise Exception(err)

        if code >= 400:
            raise Exception(f"API error {code}: {text}")

        result = json.loads(text)

        # 返回结果列表
        if "results" in result:
            return result["results"]
        return result

    def list(self, user_id: str = "default", scope: str = "", limit: int = 20):
        """
        列出记忆

        Args:
            user_id: 用户ID
            scope: 保留参数（暂不用于过滤）
            limit: 返回结果数量限制

        Returns:
            记忆列表
        """
        if self.api_mode == "cloud":
            payload = {
                "filters": {"AND": [{"user_id": user_id}]},
                "page": 1,
                "page_size": limit,
            }
            # 注意：scope 参数暂不用于 Cloud API 过滤
            code, text, err = self._call("/v2/memories/", payload)
        else:
            query = {"user_id": user_id, "limit": limit}
            if scope:
                query["scope"] = scope
            code, text, err = self._call("/memories", payload=None, method="GET", query=query)

        if err:
            raise Exception(err)

        if code >= 400:
            raise Exception(f"API error {code}: {text}")

        result = json.loads(text)

        # 返回结果列表
        if "results" in result:
            return result["results"]
        return result

    def delete(self, memory_id: str):
        """
        删除记忆

        Args:
            memory_id: 记忆ID
        """
        if self.api_mode == "cloud":
            delete_path = f"/v1/memories/{memory_id}/"
        else:
            delete_path = f"/memories/{memory_id}"

        code, text, err = self._call(delete_path, payload=None, method="DELETE")

        if err:
            raise Exception(err)

        if code >= 400:
            raise Exception(f"API error {code}: {text}")

        return json.loads(text) if text else {"success": True}
