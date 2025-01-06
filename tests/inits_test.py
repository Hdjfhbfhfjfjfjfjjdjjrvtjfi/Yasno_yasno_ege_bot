__all__ = ["InitDatabaseTest"]
from unittest import IsolatedAsyncioTestCase

from asyncio import run

from tg_bot.utils import init_database


class InitDatabaseTest(IsolatedAsyncioTestCase):

    def setUp(self):
        self.database_path = "test_data/test_database.db"
        self.models_path = "test_data.test_models"
        open(self.database_path, "w").close()

    def test_init_database(self):
        self.assertIsNone(run(init_database(self.database_path, self.models_path)))
