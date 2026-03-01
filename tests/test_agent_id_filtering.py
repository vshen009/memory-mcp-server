import importlib.util
import json
import pathlib
import unittest


def load_mem0_client_class():
    repo_root = pathlib.Path(__file__).resolve().parents[1]
    module_path = repo_root / "src" / "memory_mcp_server" / "mem0_wrapper.py"
    spec = importlib.util.spec_from_file_location("mem0_wrapper_for_test", module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module.Mem0Client


Mem0Client = load_mem0_client_class()


class Mem0ClientAgentIdFilteringTests(unittest.TestCase):
    def _client(self):
        c = Mem0Client.__new__(Mem0Client)
        c.api_mode = "cloud"
        c.api_base = "https://api.mem0.ai"
        c.api_key = "dummy"
        return c

    def test_search_filters_by_agent_id_and_scope(self):
        client = self._client()

        def fake_call(path, payload=None, method="POST", query=None):
            body = {
                "results": [
                    {"id": "1", "metadata": {"scope": "general", "agent_id": "trinity-main"}},
                    {"id": "2", "metadata": {"scope": "general", "agent_id": "other-agent"}},
                    {"id": "3", "metadata": {"scope": "ops", "agent_id": "trinity-main"}},
                ]
            }
            return 200, json.dumps(body), None

        client._call = fake_call

        items = client.search(
            query="test",
            user_id="vincent-main",
            top_k=5,
            scope="general",
            agent_id="trinity-main",
        )

        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["id"], "1")

    def test_list_filters_by_agent_id(self):
        client = self._client()

        def fake_call(path, payload=None, method="POST", query=None):
            body = {
                "results": [
                    {"id": "a", "metadata": {"agent_id": "trinity-main"}},
                    {"id": "b", "metadata": {"agent_id": "vincent-agent"}},
                    {"id": "c", "metadata": {"agent_id": "trinity-main"}},
                ]
            }
            return 200, json.dumps(body), None

        client._call = fake_call

        items = client.list(user_id="vincent-main", agent_id="trinity-main", limit=10)
        self.assertEqual([i["id"] for i in items], ["a", "c"])


if __name__ == "__main__":
    unittest.main()
