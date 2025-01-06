__all__ = ["ConfigTest"]
from unittest import TestCase

from tg_bot.utils import Config, load_config


class ConfigTest(TestCase):
    def setUp(self):
        self.config: Config = load_config("test_data/test.env")

    def test_token(self):
        self.assertEqual(self.config.token, "abc")

    def test_database_path(self):
        self.assertEqual(self.config.database_path, "database/test_database.db")

    def test_models_path(self):
        self.assertEqual(self.config.models_path, "test_data.models")