r"""
Package level utilities for templates.
"""

import jinja2

from m4db_database.decorators import static

@static(env=None)
def template_loader():
    r"""
    Retrieve the template environment for the given template type.

    :return: the template loader environment.
    """
    self = template_loader
    if self.env is None:
        self.env = jinja2.Environment(
            loader=jinja2.PackageLoader("m4db_database", "template"),
            autoescape=jinja2.select_autoescape(["jinja2"]))

    return template_loader.env
