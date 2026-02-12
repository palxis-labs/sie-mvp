import unittest
from pathlib import Path

from integrations.upstream_patch_bundle import UPSTREAM_PATCH_FILES, build_manifest


class TestUpstreamPatchBundle(unittest.TestCase):
    def test_manifest_has_no_missing_files(self):
        root = Path(__file__).resolve().parents[1]
        manifest = build_manifest(UPSTREAM_PATCH_FILES, repo_root=root)
        self.assertEqual(manifest["missing"], [], msg=str(manifest))
        self.assertGreater(manifest["fileCount"], 0)


if __name__ == "__main__":
    unittest.main()
