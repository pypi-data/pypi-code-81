import json
import unittest


class AuthentificationTests(unittest.TestCase):
    def test_init_bearer_authentification(self):
        """
        Test init bearer authentification
        """
        from elg import Authentification

        scope = "openid"

        auth = Authentification.init(scope=scope)
        self.assertIsInstance(auth, Authentification)

    def test_load_authentification(self):
        """
        Test load authentification
        """
        from elg import Authentification

        filename = "tests/data/tokens.json"

        auth = Authentification.from_json(filename=filename)
        self.assertIsInstance(auth, Authentification)


if __name__ == "__main__":
    unittest.main()
