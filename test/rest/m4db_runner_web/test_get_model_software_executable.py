import unittest
import json
import xmlrunner
import textwrap

import falcon
from falcon import testing

from m4db_database.rest.m4db_runner_web.service import app

from m4db_database_test.setup_dataset_1 import setup_dataset_1


######################################################################################################################
# Service to get the service that retrieves software associated with a model.                                        #
######################################################################################################################


class TestGetModelSoftwareExecutable(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        setup_dataset_1()

    def setUp(self) -> None:
        # Set up the test falcon service.
        self.client = testing.TestClient(app)

    def test_get_model_software_executable(self):

        expected_dict = {
            "return": "/home/m4dbdev/Install/merrill/1.8.1/bin/merrill"
        }

        response = self.client.simulate_get("/get-model-software-executable/1d73da1c-ea5f-4690-a170-4f6eb442d8e2")

        response_doc = response.text

        response_dict = json.loads(response_doc)

        print(response_dict)

        assert expected_dict == response_dict

    def test_get_model_software_executable_noexist(self):

        response = self.client.simulate_get("/get-model-software-executable/uid-that-doesnt-exist")

        assert response.status == falcon.HTTP_404


if __name__ == "__main__":
    with open("test-get-model-software-executable.xml", "wb") as fout:
        unittest.main(
            testRunner=xmlrunner.XMLTestRunner(output=fout),
            failfast=False, buffer=False, catchbreak=False
        )
