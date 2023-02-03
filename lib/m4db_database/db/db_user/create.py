r"""
A set of routines for creating m4db database users.
"""
import uuid

from m4db_database.orm.latest import DBUser
from m4db_database.utilities.password import password_hash


def create_db_user(user_name, first_name, surname, email, access_level, ticket_length, session, initials=None,
                   telephone=None):
    r"""
    Create a new db user.
    :param user_name: the user's user name.
    :param first_name: the user's first name
    :param surname: the user's surname.
    :param email: the user's email.
    :param access_level: the access level for the user - determines which services the user can access.
    :param ticket_length: the length (in seconds) for the users issued tickets.
    :param session: the database session.
    :param initials: the user's initials (optional).
    :param telephone: the user's telephone number (optional).
    :return: None
    """
    db_user = session.query(DBUser).filter(DBUser.user_name == user_name).one_or_none()
    if db_user is not None:
        raise ValueError("User with user-name '{}' already exists.".format(user_name))

    # Create a new DBUser object
    db_user = DBUser(
        user_name=user_name,
        password=password_hash(uuid.uuid4()),  # For new user make up any old password
        first_name=first_name,
        surname=surname,
        email=email,
        access_level=access_level,
        ticket_length=ticket_length,
        initials=initials,
        telephone=telephone
    )

    # Return the database user
    return db_user
