r"""
A selection of actions that will schedule a model for execution.
"""
import sys

from subprocess import PIPE, Popen

from tempfile import NamedTemporaryFile

from m4db_database.sessions import get_session
from m4db_database.configuration import read_config_from_environ

from m4db_database.template import template_loader
from m4db_database.db.model.retrieve import get_models
from m4db_database.rest_api.m4db_runner_web.set_model_running_status import set_model_running_status


def schedule_model(unique_id):
    r"""
    Create a scripts and schedule with slurm.
    :param unique_id: the unique_id of the model to schedule.
    :return: None
    """
    config = read_config_from_environ()
    slurm_template = template_loader("slurm").get_template("slurm_model.jinja2")

    sdata = {
        "unique_id": unique_id,
        "N": 1,
        "n": 1,
        "c": 1,
        "time": "99:99:99",
        "working_directory": config["m4db_serverside"]["working_dir"],
        "module_dir": config["m4db_serverside"]["module_dir"],
        "modules": config["m4db_serverside"]["modules"]
    }

    # Open a temporary file.
    with NamedTemporaryFile("w") as fout:
        fout.write(slurm_template.render(sdata=sdata))

        # print(slurm_template.render(sdata=sdata))

        fout.flush()

        cmd = "{} {}".format(config["m4db_serverside"]["slurm_exe"], fout.name)
        proc = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True, universal_newlines=True, text=True)

        stdout, stderr = proc.communicate()

        if stderr != "":
            print("Some error occurred when attempting to schedule job with slurm")
            print("--> {}".format(stderr))
            sys.exit(1)
        else:
            print("Submitted job for unique ID {}".format(unique_id))


def schedule_jobs(**kwargs):
    r"""
    Schedule a selection of jobs based on the input arguments.
    :param kwargs: job arguments
    :return: None
    """
    with get_session(nullpool=True) as session:
        models = get_models(session, **kwargs)
        model_unique_ids = []
        for model in models:
            model_unique_ids.append(model.unique_id)
        session.close()

    if kwargs["list_unique_ids"]:
        print("--------------------------")
        print(" Model unique ids:")
        print("--------------------------")
        for index, model_unique_id in enumerate(model_unique_ids):
            print("{:5d}) {}".format(index+1, model_unique_id))
        print()

    nmodels = len(model_unique_ids)
    if (kwargs["real_run"]):
        print("Scheduling {} model(s).".format(nmodels))
        for model_unique_id in model_unique_ids:
            schedule_model(model_unique_id)
            set_model_running_status(model_unique_id, "scheduled")
    else:
        print("{} model(s) found, use --real-run to schedule them for execution.".format(nmodels))

