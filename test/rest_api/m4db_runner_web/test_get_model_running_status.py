import unittest
import xmlrunner
import pytest

import requests.exceptions

from m4db.rest_api.m4db_runner_web.get_model_running_status import get_model_running_status


######################################################################################################################
# Test wrapper API for model prerequisites.                                                                          #
######################################################################################################################

class TestGetModelRunningStatus(unittest.TestCase):

    def test_get_model_running_status(self):
        unique_id = "1d73da1c-ea5f-4690-a170-4f6eb442d8e2"

        expected_value = "not-run"

        result = get_model_running_status(unique_id)

        assert expected_value == result

    def test_get_model_initial_magnetization_noexist(self):
        unique_id = "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"

        with pytest.raises(requests.exceptions.HTTPError):
            result = get_model_running_status(unique_id)


if __name__ == "__main__":
    with open("test-get-model-running-status.xml", "wb") as fout:
        unittest.main(
            testRunner=xmlrunner.XMLTestRunner(output=fout),
            failfast=False, buffer=False, catchbreak=False
        )
