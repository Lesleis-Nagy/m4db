import os

import pytest
import unittest
import xmlrunner

import requests.exceptions

from m4db.rest_api.m4db_runner_web.get_software_executable import get_software_executable


######################################################################################################################
# Service to get the executable for a given software.                                                                #
######################################################################################################################

class TestGetSoftwareExecutable(unittest.TestCase):

    def test_get_software_executable_api(self):
        user = os.getenv("USER", None)
        expected = f"/home/{user}/Install/merrill/1.8.1/bin/merrill"

        result = get_software_executable("merrill", "1.8.1")

        assert expected == result

    def test_get_software_executable_noexist(self):
        with pytest.raises(requests.exceptions.HTTPError):
            result = get_software_executable("noexist", "version")

    def test_get_software_executable_software_is_empty(self):
        result = get_software_executable("emptysw", "0.1.0")

        assert result is None


if __name__ == "__main__":
    with open("test-get-software-executable.xml", "wb") as fout:
        unittest.main(
            testRunner=xmlrunner.XMLTestRunner(output=fout),
            failfast=False, buffer=False, catchbreak=False
        )
