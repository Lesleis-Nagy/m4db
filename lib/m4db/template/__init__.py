r"""
Package level utilities for templates.
"""

import jinja2

from m4db.decorators import static

from m4db.configuration import read_config_from_environ


@static(env=None)
def template_loader():
    r"""
    Retrieve an object that can load JINJA2 templates.

    :return: the template loader environment.
    """
    self = template_loader
    if self.env is None:
        self.env = jinja2.Environment(
            loader=jinja2.PackageLoader("m4db", "template"),
            autoescape=jinja2.select_autoescape(["jinja2"]))

    return template_loader.env


def model_slurm_script(unique_id: str, nodes: int = 1, ntasks: int = 1, cpus_per_task: int = 1, time: str = "99:99:99"):
    r"""
    Build a slurm script that runs models and return it as a string.

    :param unique_id: unique id of a model.
    :param nodes: request that a minimum of minnodes nodes be allocated to this job (-N switch).
    :param ntasks: number of tasks (MPI ranks) (-n switch).
    :param cpus_per_task: request ncpus cores per task (-c switch).
    :param time: the maximum running time.

    :return: a text file containing the slurm script populated using the input parameters.
    """
    config = read_config_from_environ()
    template = template_loader().get_template("slurm_model.jinja2")

    return template.render(
        unique_id=unique_id,
        nodes=nodes,
        ntasks=ntasks,
        cpus_per_task=cpus_per_task,
        time=time,
        working_directory=config.database.working_root,
        module_source=config.modules.source,
        module_dir=config.modules.path,
        modules=config.modules.to_load
    )
