import json
import unittest


class TechnologyTests(unittest.TestCase):

    url = "https://live.european-language-grid.eu/execution/"
    authentification_filename = "tests/data/tokens.json"
    sample_txt_filename = "tests/data/test.txt"
    sample_audio_filename = "tests/data/test.mp3"

    def test_technology_curl(self):
        """
        Test to use a LT with requests in python
        """
        import requests

        service = "processText/cogner"
        mode = "r"
        sample_filename = self.sample_txt_filename

        with open(self.authentification_filename) as f:
            token = json.load(f)["access_token"]
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "text/plain",
        }

        with open(sample_filename, mode) as f:
            file_dict = {"file": f}
            response = requests.post(self.url + service, headers=headers, files=file_dict)

        self.assertEqual(response.status_code, 200)

    def test_load_technology(self):
        """
        Test to load a LT with the Technology class
        """
        from elg import Technology

        id = 476

        tech = Technology(id, self.authentification_filename)
        self.assertIsInstance(tech, Technology)

    def test_run_txt_technology(self):
        """
        Test to run a LT that uses txt input with the Technology class
        """
        from elg import Technology

        id = 476

        tech = Technology(id, self.authentification_filename)
        self.assertIsInstance(tech, Technology)

        result, status_code = tech(self.sample_txt_filename)
        self.assertEqual(status_code, 200)

    def test_run_audio_technology(self):
        """
        Test to run a LT that uses audio input with the Technology class
        """
        from elg import Technology

        id = 489

        tech = Technology(id, self.authentification_filename)
        self.assertIsInstance(tech, Technology)

        result, status_code = tech(self.sample_audio_filename)
        self.assertEqual(status_code, 200)


if __name__ == "__main__":
    unittest.main()
