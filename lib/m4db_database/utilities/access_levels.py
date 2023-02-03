r"""
A selection of routines to deal with access levels.
"""


class AccessLevel:
    # Anyone can access a service with this access level.
    ANY = 0

    # Only users with 'READ' can access services with this access level.
    READ = 1

    # Only users with 'WRITE' can access services with this access level.
    WRITE = 2

    # Only users with 'ADMIN' can access services with this access level.
    ADMIN = 4


def allowed_access_levels():
    r"""
    Return a list of representations of access levels.
    :return: a list of access level representations
    """
    return ["any", "read", "write", "admin"]


def string_to_access_level(str_level:str):
    r"""
    Converts a string to an access level.
    :param str_level: the access level string.
    :return: an access level.
    """
    if str_level.upper() == "ANY":
        return AccessLevel.ANY
    elif str_level.upper() == "READ":
        return AccessLevel.READ
    elif str_level.upper() == "WRITE":
        return AccessLevel.WRITE
    elif str_level.upper() == "ADMIN":
        return AccessLevel.ADMIN
    else:
        raise ValueError("Requested enumeration for unknown access level: '{}'".format(str_level))


def access_level_to_string(access_level:AccessLevel):
    r"""
    Converts an access level to a string representation.
    :param access_level: the access level.
    :return: a string representation of the input access level
    """
    if access_level == AccessLevel.ANY:
        return "ANY"
    if access_level == AccessLevel.READ:
        return "READ"
    if access_level == AccessLevel.WRITE:
        return "WRITE"
    if access_level == AccessLevel.ADMIN:
        return "ADMIN"
    else:
        raise ValueError("Unknown access level enumeration value {}".format(access_level))
