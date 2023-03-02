import unittest
import json
import xmlrunner

import falcon
from falcon import testing

from m4db_database.rest.m4db_runner_web.service import app

from m4db_database_test.setup_dataset_1 import setup_dataset_1


class TestGetSoftwareExecutable(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        setup_dataset_1()

    def setUp(self) -> None:
        # Set up the test falcon service.
        self.client = testing.TestClient(app)

    ###################################################################################################################
    # Service to get the executable for a given software.                                                             #
    ###################################################################################################################

    def test_get_software_executable(self):
        expected_dict = {
            "return": "/home/m4dbdev/Install/merrill/1.8.1/bin/merrill"
        }

        response = self.client.simulate_get("/get-software-executable/merrill/1.8.1")

        response_doc = response.text

        response_dict = json.loads(response_doc)

        assert expected_dict == response_dict

    def test_get_software_executable_noexist(self):

        response = self.client.simulate_get("/get-software-executable/noexist/noexist")

        assert response.status == falcon.HTTP_404

    def test_get_software_executable_software_is_empty(self):
        expected_dict = {
            "return": None
        }

        response = self.client.simulate_get("/get-software-executable/emptysw/0.1.0")

        response_doc = response.text

        response_dict = json.loads(response_doc)

        assert expected_dict == response_dict


if __name__ == "__main__":
    with open("test-get-software-executable.xml", "wb") as fout:
        unittest.main(
            testRunner=xmlrunner.XMLTestRunner(output=fout),
            failfast=False, buffer=False, catchbreak=False
        )
