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
# Service to get the prerequisites of a model run.                                                                   #
######################################################################################################################


def test_model_run_prerequisites(client):

    expected_dict = {
        "merrill-script": textwrap.dedent(r"""
            Set MaxMeshNumber 1

            ReadMesh 1 geometry.pat

            Set MaxEnergyEvaluations 10000

            ConjugateGradient
            Set ExchangeCalculator 1


            set subdomain 1 magnetite 20.000



            EnergyLog energy


            Minimize
            WriteMagnetization magnetization
            CloseLogfile

            ReportEnergy

            End""").strip(),
        "geometry-file-abs-path": "/data/m4dbdev/geometry/42/a7/77/ce/14/ff/42/3e/83/78/1f/49/d6/28/f6/17/geometry.pat",
        "model-dir-abs-path": "/data/m4dbdev/model/1d/73/da/1c/ea/5f/46/90/a1/70/4f/6e/b4/42/d8/e2"
    }

    response = client.simulate_get("/get-model-run-prerequisites/1d73da1c-ea5f-4690-a170-4f6eb442d8e2")

    response_dict = json.loads(response.text)

    assert expected_dict == response_dict


def test_get_model_run_prerequisites(client):

    response = client.simulate_get("/get-model-run-prerequisites/noexist")

    assert response.status == falcon.HTTP_404
