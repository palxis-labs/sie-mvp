import unittest

from integrations.upstream_pr_payload import build_pr_payload


class TestUpstreamPrPayload(unittest.TestCase):
    def test_payload_contains_behavior_and_file_list(self):
        manifest = {"fileCount": 2, "files": ["a.py", "b.py"]}
        out = build_pr_payload(manifest)
        self.assertIn("unsigned + warn => allow", out)
        self.assertIn("`a.py`", out)
        self.assertIn("`b.py`", out)


if __name__ == "__main__":
    unittest.main()
