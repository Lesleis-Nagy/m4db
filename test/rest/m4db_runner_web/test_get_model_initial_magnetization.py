import unittest
import falcon
import json
import xmlrunner

from falcon import testing

from m4db_database.rest.m4db_runner_web.service import app


class TestGetModelInitialMagnetization(unittest.TestCase):

    def setUp(self) -> None:
        # Set up the test falcon service.
        self.client = testing.TestClient(app)

    def test_get_model_initial_magnetization(self):

        unique_id = "1d73da1c-ea5f-4690-a170-4f6eb442d8e2"

        expected_dict = {
            "return": {
                "type": "random"
            }
        }

        response = self.client.simulate_get(f"/get-model-initial-magnetization/{unique_id}")

        response_dict = json.loads(response.text)

        assert expected_dict == response_dict

    def test_get_model_initial_magnetization_noexist(self):

        unique_id = "missing"

        response = self.client.simulate_get(f"/get-model-initial-magnetization/{unique_id}")

        assert response.status == falcon.HTTP_404


if __name__ == "__main__":
    with open("test-get-model-initial-magnetization-result.xml", "wb") as fout:
        unittest.main(
            testRunner=xmlrunner.XMLTestRunner(output=fout),
            failfast=False, buffer=False, catchbreak=False
        )
