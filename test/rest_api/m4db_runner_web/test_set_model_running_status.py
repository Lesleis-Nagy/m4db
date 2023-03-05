import pytest
import unittest
import xmlrunner

import requests.exceptions

from m4db.rest_api.m4db_runner_web.set_model_running_status import set_model_running_status

from m4db.orm.schema import Model

from m4db.sessions import get_session


######################################################################################################################
# Test wrapper API for setting model running statuses                                                                #
######################################################################################################################

class TestSetModelRunningStatus(unittest.TestCase):

    def test_set_model_quants(self):
        unique_id = "1d73da1c-ea5f-4690-a170-4f6eb442d8e2"

        session = get_session()

        result = set_model_running_status(
            unique_id=unique_id,
            running_status="crashed")

        model = session.query(Model).filter(Model.unique_id == unique_id).one()

        assert model.running_status.name == "crashed"

    def test_get_model_initial_magnetization_noexist(self):
        unique_id = "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"

        with pytest.raises(requests.exceptions.HTTPError):
            response = set_model_running_status(unique_id, "crashed")


if __name__ == "__main__":
    with open("test-set-model-running-status.xml", "wb") as fout:
        unittest.main(
            testRunner=xmlrunner.XMLTestRunner(output=fout),
            failfast=False, buffer=False, catchbreak=False
        )
