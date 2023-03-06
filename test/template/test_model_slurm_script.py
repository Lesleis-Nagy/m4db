import unittest
import xmlrunner
import textwrap


from m4db.template import model_slurm_script

class TestModelSlurmScript(unittest.TestCase):

    def test_generate_slurm_script_1(self):
        r"""
        This test generates a simple slurm script and checks that it is of the correct format.
        """
        expected_script = textwrap.dedent(r"""
        #!/bin/bash

        #SBATCH --job-name=1d73da1c-ea5f-4690-a170-4f6eb442d8e2

        #SBATCH -N 1 # No. of nodes
        #SBATCH -n 1 # No. of tasks
        #SBATCH -c 1 # No. of cores per task

        #SBATCH --time=99:99:99
        #SBATCH --chdir=/quick-data/m4dbdev

        # Load modules
        export MODULEPATH=/home/m4dbdev/Modules

        module load m4db/0.1.0


        # Run model
        srun -N 1 m4db-run-model 1d73da1c-ea5f-4690-a170-4f6eb442d8e2
        """).strip()

        slurm_script = model_slurm_script("1d73da1c-ea5f-4690-a170-4f6eb442d8e2")

        self.assertEqual(expected_script, slurm_script)


if __name__ == "__main__":
    with open("test-model-slurm-script.xml", "wb") as fout:
        unittest.main(
            testRunner=xmlrunner.XMLTestRunner(output=fout),
            failfast=False, buffer=False, catchbreak=False
        )
