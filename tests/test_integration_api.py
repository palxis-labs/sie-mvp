import unittest


class TestIntegrationApi(unittest.TestCase):
    def test_public_exports(self):
        import integrations as api

        self.assertTrue(callable(api.evaluate_skill))
        self.assertTrue(callable(api.parse_sie_runtime_config))
        self.assertTrue(callable(api.enforce_skill_from_openclaw_config))
        self.assertTrue(callable(api.load_skill_text_with_sie))


if __name__ == "__main__":
    unittest.main()
