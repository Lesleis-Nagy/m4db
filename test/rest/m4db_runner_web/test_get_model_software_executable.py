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
# Service to get the service that retrieves software associated with a model.                                        #
######################################################################################################################


def test_get_model_software_executable(client):

    expected_dict = {
        "return": "/home/m4dbdev/Install/merrill/1.8.1/bin/merrill"
    }

    response = client.simulate_get("/get-model-software-executable/1d73da1c-ea5f-4690-a170-4f6eb442d8e2")

    response_doc = response.text

    response_dict = json.loads(response_doc)

    print(response_dict)

    assert expected_dict == response_dict


def test_get_model_software_executable_noexist(client):

    response = client.simulate_get("/get-model-software-executable/uid-that-doesnt-exist")

    assert response.status == falcon.HTTP_404

