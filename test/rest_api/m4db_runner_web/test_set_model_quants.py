import pytest
import unittest
import xmlrunner

import requests.exceptions

from m4db_database.rest_api.m4db_runner_web.set_model_quants import set_model_quants

from m4db_database.orm.schema import Model

from m4db_database.sessions import get_session


######################################################################################################################
# Test wrapper API for setting model quants.                                                                         #
######################################################################################################################

class TestSetModelQuants(unittest.TestCase):

    def test_set_model_quants(self):
        unique_id = "1d73da1c-ea5f-4690-a170-4f6eb442d8e2"

        session = get_session()

        result = set_model_quants(
            unique_id=unique_id,
            mx_tot=1.0,
            my_tot=2.0,
            mz_tot=3.0,
            vx_tot=4.0,
            vy_tot=5.0,
            vz_tot=6.0,
            h_tot=7.0,
            rh_tot=8.0,
            adm_tot=9.0,
            e_typical=10.0,
            e_anis=11.0,
            e_ext=12.0,
            e_demag=13.0,
            e_exch1=14.0,
            e_exch2=15.0,
            e_exch3=16.0,
            e_exch4=17.0,
            e_tot=18.0)

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

    def test_get_model_initial_magnetization_noexist(self):
        unique_id = "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"

        with pytest.raises(requests.exceptions.HTTPError):
            response = set_model_quants(unique_id)


if __name__ == "__main__":
    with open("test-set-model-quants.xml", "wb") as fout:
        unittest.main(
            testRunner=xmlrunner.XMLTestRunner(output=fout),
            failfast=False, buffer=False, catchbreak=False
        )
