import unittest
import falcon
from falcon import testing
import xmlrunner
import json

from m4db_database.orm.schema import Model
from m4db_database.rest.m4db_runner_web.service import app

from m4db_database.rest.m4db_runner_web.set_model_running_status import SetModelRunningStatusJSONSchema
from m4db_database.sessions import get_session


class TestSetModelRunningStatus(unittest.TestCase):

    def setUp(self) -> None:
        # Set up the test falcon service.
        self.client = testing.TestClient(app)

######################################################################################################################
# Service to set the running status of a given model.                                                                #
######################################################################################################################

    def test_set_model_running_status(self):
        r"""
        Prior to this test, we must populate with data set 2
            $> populate-dataset-2

        Args:
            client:

        Returns:

        """
        unique_id = "1d73da1c-ea5f-4690-a170-4f6eb442d8e2"

        session = get_session()

        response_data = SetModelRunningStatusJSONSchema()
        response_data.unique_id = unique_id
        response_data.new_running_status = "crashed"

        response = self.client.simulate_post("/set-model-running-status", json=json.dumps(response_data.to_primitive()))

        model = session.query(Model).filter(Model.unique_id == unique_id).one()

        assert model.running_status.name == "crashed"

    def test_set_model_running_status_noexist(self):

        unique_id = "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"

        expected_response = {
            "error": f"Missing model with unique id: '{unique_id}'."
        }

        response_data = SetModelRunningStatusJSONSchema()
        response_data.unique_id = unique_id
        response_data.new_running_status = "crashed"

        response = self.client.simulate_post("/set-model-running-status", json=json.dumps(response_data.to_primitive()))
        response_result = json.loads(response.text)

        assert response.status == falcon.HTTP_404
        assert expected_response == response_result

if __name__ == "__main__":
    with open("test-set-model-running-status.xml", "wb") as fout:
        unittest.main(
            testRunner=xmlrunner.XMLTestRunner(output=fout),
            failfast=False, buffer=False, catchbreak=False
        )
