import falcon
from falcon import testing
import msgpack
import pytest
import json
import textwrap

from m4db_database.rest.m4db_runner_web.service import app


@pytest.fixture
def client():
    return testing.TestClient(app)


######################################################################################################################
# Service to get initial magnetization of a model.                                                                   #
######################################################################################################################


def test_get_model_initial_magnetization(client):

    unique_id = "1d73da1c-ea5f-4690-a170-4f6eb442d8e2"

    expected_dict = {
        "return": {
            "type": "random"
        }
    }

    response = client.simulate_get(f"/get-model-initial-magnetization/{unique_id}")

    response_dict = json.loads(response.text)

    assert expected_dict == response_dict


def test_get_model_initial_magnetization_noexist(client):

    unique_id = "missing"

    response = client.simulate_get(f"/get-model-initial-magnetization/{unique_id}")

    assert response.status == falcon.HTTP_404
