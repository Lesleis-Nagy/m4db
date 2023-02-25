import falcon
from falcon import testing
import msgpack
import pytest
import json

from m4db_database.rest.m4db_runner_web.service import app


@pytest.fixture
def client():
    return testing.TestClient(app)


######################################################################################################################
# Service to get the running status for a given model.                                                               #
######################################################################################################################


def test_get_model_running_status(client):

    expected_dict = {
        "return": "not-run"
    }

    response = client.simulate_get("/get-model-running-status/1d73da1c-ea5f-4690-a170-4f6eb442d8e2")

    response_doc = response.text

    response_dict = json.loads(response_doc)

    assert expected_dict == response_dict


def test_get_model_running_status_noexist(client):

    response = client.simulate_get("/get-software-executable/noexist/noexist")

    assert response.status == falcon.HTTP_404
