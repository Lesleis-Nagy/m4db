r"""
A collection of routines to retrieve users from the database.
"""

from m4db_database.orm.schema import DBUser


def retrieve_db_user(user_name, session):
    r"""
    Retrieve a user from the database.
    :param user_name: the user name of the user to retrieve.
    :param session: a database session.
    :return: A DBUser object.
    """
    # Attempt to retrieve the db_user
    db_user = session.query(DBUser).filter(DBUser.user_name == user_name).one_or_none()

    # If the db_user cannot be found ...
    if db_user is None:
        # ... close session & raise error
        raise ValueError("New model database user '{}' cannot be found.".format(user_name))

    return db_user
