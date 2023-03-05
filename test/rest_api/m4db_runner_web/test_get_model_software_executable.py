import os
import unittest
import xmlrunner

import pytest

import requests.exceptions

from m4db.rest_api.m4db_runner_web.get_model_software_executable import get_model_software_executable


######################################################################################################################
# Test wrapper API for software executables.                                                                         #
######################################################################################################################


class TestGetModelSoftwareExecutable(unittest.TestCase):

    def test_get_software_executable(self):
        user = os.getenv("USER", None)

        unique_id = "1d73da1c-ea5f-4690-a170-4f6eb442d8e2"

        expected = f"/home/{user}/Install/merrill/1.8.1/bin/merrill"

        result = get_model_software_executable(unique_id)

        assert expected == result

    def test_get_model_software_noexist(self):
        unique_id = "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"

        with pytest.raises(requests.exceptions.HTTPError):
            result = get_model_software_executable(unique_id)


if __name__ == "__main__":
    with open("test-get-model-software-executable.xml", "wb") as fout:
        unittest.main(
            testRunner=xmlrunner.XMLTestRunner(output=fout),
            failfast=False, buffer=False, catchbreak=False
        )
