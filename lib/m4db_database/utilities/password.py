r"""
A selection of utility routines for dealing with passwords.
"""

from hashlib import md5

from m4db_database.configuration import read_config_from_environ
from m4db_database import global_vars


def password_hash(password):
    r"""
    Take the password and produce a salted hash from it.
    :param password: the input password
    :return: the salted hash of the password.
    """

    config = read_config_from_environ()

    salted_password = global_vars.SALTED_PASSWORD_FORMAT.format(
        password=password,
        salt=config.password_salt
    )

    return md5(salted_password.encode('ascii')).hexdigest()


def random_password(length=15, with_specials=True):
    r"""
    Generate a random password for a user.
    :param length: the length of the password.
    :param with_specials: if True use special characters.
    :return: None.
    """
    chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    specials = "!@#$%^&*()_+=-{}[]"

    if with_specials:
        choose_chars = [ch for ch in chars + specials]
    else:
        choose_chars = [ch for ch in chars]

    random.shuffle(choose_chars)

    return "".join(choose_chars[0:length])
