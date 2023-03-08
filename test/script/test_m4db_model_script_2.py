import os
import unittest
import shutil
import tempfile
import xmlrunner

from m4db.orm.schema import Model
from m4db.orm.schema import RunningStatusEnum

from m4db.utilities.directories import model_directory

from m4db.sessions import get_session

from m4db import GLOBAL

SCRIPT_NAME = "test_m4db_model_script_2"

class TestM4DBRunCommand1(unittest.TestCase):

    def test_check_model_1d73da1c_ea5f_4690_a170_4f6eb442d8e2(self):
        r"""
        This check tests to see if we managed to schedule/run model id 1d73da1c-ea5f-4690-a170-4f6eb442d8e2.
        """

        session = get_session()

        # Simply check that we've got a complete set of data for the specified model.
        model = session.query(Model).filter(Model.unique_id == "1d73da1c-ea5f-4690-a170-4f6eb442d8e2").one()

        self.assertEqual(model.running_status.name, RunningStatusEnum.finished.value)
        self.assertIsNotNone(model.mx_tot)
        self.assertIsNotNone(model.my_tot)
        self.assertIsNotNone(model.mz_tot)
        self.assertIsNotNone(model.vx_tot)
        self.assertIsNotNone(model.vy_tot)
        self.assertIsNotNone(model.vz_tot)
        self.assertIsNotNone(model.h_tot)
        self.assertIsNotNone(model.rh_tot)
        self.assertIsNotNone(model.adm_tot)
        self.assertIsNotNone(model.e_typical)
        self.assertIsNotNone(model.e_anis)
        self.assertIsNotNone(model.e_ext)
        self.assertIsNotNone(model.e_demag)
        self.assertIsNotNone(model.e_exch1)
        self.assertIsNotNone(model.e_exch2)
        self.assertIsNotNone(model.e_exch3)
        self.assertIsNotNone(model.e_exch4)
        self.assertIsNotNone(model.e_tot)

        # Check that the zip file exists.
        old_wd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp_dir:
            os.chdir(tmp_dir)

            data_zip_abs_path = os.path.join(model_directory(model.unique_id), GLOBAL.DATA_ZIP)

            # Make sure that the zip file exists.
            self.assertTrue(os.path.isfile(data_zip_abs_path))

            shutil.unpack_archive(data_zip_abs_path, extract_dir=tmp_dir)

            # After unzipping, there should be 6 files.
            self.assertEqual(len(os.listdir(tmp_dir)), 6)

            # After unzipping, each of these files should exist.
            self.assertTrue(os.path.isfile("energy.log"))
            self.assertTrue(os.path.isfile("magnetization.dat"))
            self.assertTrue(os.path.isfile("magnetization.tec"))
            self.assertTrue(os.path.isfile("model_script.merrill"))
            self.assertTrue(os.path.isfile("model_stderr.txt"))
            self.assertTrue(os.path.isfile("model_stdout.txt"))
        os.chdir(old_wd)

    def test_check_model_01bd340e_4e7a_44e0_b327_d61670d93a6f(self):
        r"""
        This check tests to see if we managed to schedule/run model id 01bd340e-4e7a-44e0-b327-d61670d93a6f.
        """

        session = get_session()

        # Simply check that we've got a complete set of data for the specified model.
        model = session.query(Model).filter(Model.unique_id == "01bd340e-4e7a-44e0-b327-d61670d93a6f").one()

        self.assertEqual(model.running_status.name, RunningStatusEnum.finished.value)
        self.assertIsNotNone(model.mx_tot)
        self.assertIsNotNone(model.my_tot)
        self.assertIsNotNone(model.mz_tot)
        self.assertIsNotNone(model.vx_tot)
        self.assertIsNotNone(model.vy_tot)
        self.assertIsNotNone(model.vz_tot)
        self.assertIsNotNone(model.h_tot)
        self.assertIsNotNone(model.rh_tot)
        self.assertIsNotNone(model.adm_tot)
        self.assertIsNotNone(model.e_typical)
        self.assertIsNotNone(model.e_anis)
        self.assertIsNotNone(model.e_ext)
        self.assertIsNotNone(model.e_demag)
        self.assertIsNotNone(model.e_exch1)
        self.assertIsNotNone(model.e_exch2)
        self.assertIsNotNone(model.e_exch3)
        self.assertIsNotNone(model.e_exch4)
        self.assertIsNotNone(model.e_tot)

        # Check that the zip file exists.
        old_wd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp_dir:
            os.chdir(tmp_dir)

            data_zip_abs_path = os.path.join(model_directory(model.unique_id), GLOBAL.DATA_ZIP)

            # Make sure that the zip file exists.
            self.assertTrue(os.path.isfile(data_zip_abs_path))

            shutil.unpack_archive(data_zip_abs_path, extract_dir=tmp_dir)

            # After unzipping, there should be 6 files.
            self.assertEqual(len(os.listdir(tmp_dir)), 6)

            # After unzipping, each of these files should exist.
            self.assertTrue(os.path.isfile("energy.log"))
            self.assertTrue(os.path.isfile("magnetization.dat"))
            self.assertTrue(os.path.isfile("magnetization.tec"))
            self.assertTrue(os.path.isfile("model_script.merrill"))
            self.assertTrue(os.path.isfile("model_stderr.txt"))
            self.assertTrue(os.path.isfile("model_stdout.txt"))
        os.chdir(old_wd)


if __name__ == "__main__":
    with open(f"{SCRIPT_NAME}.xml", "wb") as fout:
        unittest.main(
            testRunner=xmlrunner.XMLTestRunner(output=fout),
            failfast=False, buffer=False, catchbreak=False
        )
