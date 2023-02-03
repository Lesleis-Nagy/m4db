r"""
Package level utilities for templates.
"""

import jinja2

from m4db_database.decorators import static

@static(envs=None)
def template_env(template_type):
    r"""
    Retrieve the template environment for the given template type.
    :param template_type: the template type (one of "merrill", "slurm")
    :return: the template type associated with the input value.
    """
    if template_env.envs is None:
        merrill_loader = jinja2.PackageLoader("m4db_serverside", "templates/merrill")
        slurm_loader = jinja2.PackageLoader("m4db_serverside", "templates/slurm")
        template_env.envs = {
            "merrill": jinja2.Environment(
                loader=merrill_loader,
                autoescape=jinja2.select_autoescape(["jinja2"])),
            "slurm": jinja2.Environment(
                loader=slurm_loader,
                autoescape=jinja2.select_autoescape(["jinja2"]))
        }

    return template_env.envs[template_type]
