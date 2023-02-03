r"""
Decorators used in this package.
"""


def static(**kwargs):
    r"""
    :params **kwargs: key value pairs to add as static variables.
    :return: None
    """
    def wrap(func):
        for key, value in kwargs.items():
            setattr(func, key, value)
        return func
    return wrap
