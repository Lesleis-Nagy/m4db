import unittest
import json
import xmlrunner

import falcon
from falcon import testing

from m4db_database.orm.schema import Model
from m4db_database.rest.m4db_runner_web.service import app
from m4db_database.rest.m4db_runner_web.set_model_quants import SetModelQuantsJSONSchema

from m4db_database.sessions import get_session


class TestSetModelQuants(unittest.TestCase):

    def setUp(self) -> None:
        # Set up the test falcon service.
        self.client = testing.TestClient(app)

    ######################################################################################################################
    # Service to set the quants of a given model.                                                                        #
    ######################################################################################################################

    def test_set_model_quants(self):

        unique_id = "1d73da1c-ea5f-4690-a170-4f6eb442d8e2"

        session = get_session()

        response_data = SetModelQuantsJSONSchema()
        response_data.unique_id = unique_id
        response_data.mx_tot = 1.0
        response_data.my_tot = 2.0
        response_data.mz_tot = 3.0
        response_data.vx_tot = 4.0
        response_data.vy_tot = 5.0
        response_data.vz_tot = 6.0
        response_data.h_tot = 7.0
        response_data.rh_tot = 8.0
        response_data.adm_tot = 9.0
        response_data.e_typical = 10.0
        response_data.e_anis = 11.0
        response_data.e_ext = 12.0
        response_data.e_demag = 13.0
        response_data.e_exch1 = 14.0
        response_data.e_exch2 = 15.0
        response_data.e_exch3 = 16.0
        response_data.e_exch4 = 17.0
        response_data.e_tot = 18.0

        response = self.client.simulate_post("/set-model-quants", json=json.dumps(response_data.to_primitive()))

        model = session.query(Model).filter(Model.unique_id == unique_id).one()

        assert model.mx_tot == 1.0
        assert model.my_tot == 2.0
        assert model.mz_tot == 3.0
        assert model.vx_tot == 4.0
        assert model.vy_tot == 5.0
        assert model.vz_tot == 6.0
        assert model.h_tot == 7.0
        assert model.rh_tot == 8.0
        assert model.adm_tot == 9.0
        assert model.e_typical == 10.0
        assert model.e_anis == 11.0
        assert model.e_ext == 12.0
        assert model.e_demag == 13.0
        assert model.e_exch1 == 14.0
        assert model.e_exch2 == 15.0
        assert model.e_exch3 == 16.0
        assert model.e_exch4 == 17.0
        assert model.e_tot == 18.0

    def test_set_model_quants_noexist(self):

        unique_id = "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"

        expected_response = {
            "error": f"Missing model with unique id: '{unique_id}'."
        }

        response_data = SetModelQuantsJSONSchema()
        response_data.unique_id = unique_id

        response = self.client.simulate_post("/set-model-quants", json=json.dumps(response_data.to_primitive()))
        response_result = json.loads(response.text)

        assert response.status == falcon.HTTP_404
        assert expected_response == response_result


if __name__ == "__main__":
    with open("test-set-model-quants.xml", "wb") as fout:
        unittest.main(
            testRunner=xmlrunner.XMLTestRunner(output=fout),
            failfast=False, buffer=False, catchbreak=False
        )
