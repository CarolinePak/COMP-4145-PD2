import tempfile
import unittest

from config import config
from modules import profile


class ProfilePreferenceTests(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.original_users_dir = config.USERS_DIR
        self.original_analyses_dir = config.ANALYSES_DIR
        config.USERS_DIR = self.temporary_directory.name + "/users"
        config.ANALYSES_DIR = self.temporary_directory.name + "/analyses"

    def tearDown(self):
        config.USERS_DIR = self.original_users_dir
        config.ANALYSES_DIR = self.original_analyses_dir
        self.temporary_directory.cleanup()

    def test_last_activated_profile_is_remembered(self):
        first = profile.create_user("Alice", ["Improve hydration"])
        second = profile.create_user("Bob", ["Reduce redness"])

        profile._activate_user(second)

        self.assertEqual(profile.load_last_user_id(), second["user_id"])
        self.assertEqual(
            [user["user_id"] for user in profile.list_users()],
            [first["user_id"], second["user_id"]],
        )

    def test_deleting_last_profile_clears_preference(self):
        user = profile.create_user("Alice", ["Improve hydration"])
        profile._activate_user(user)

        profile.delete_user(user["user_id"])

        self.assertIsNone(profile.load_last_user_id())


if __name__ == "__main__":
    unittest.main()
