import typer

import pandas as pd

from tabulate import tabulate

from m4db_database.orm.latest import DBUser

from m4db_database.sessions import get_session

from m4db_database.db.db_user.create import create_db_user

from m4db_database.utilities.access_levels import string_to_access_level

app = typer.Typer()

USERNAME = "Username"
FIRST_NAME = "First name"
INITIALS = "Initials"
SURNAME = "Surname"
EMAIL = "Email"
TELEPHONE = "Telephone"


@app.command()
def list(csv_file: str = None):
    r"""
    List the users in the system.

    :param csv_file: save output to csv file instead of stdout.

    :return: None.
    """
    session = get_session(nullpool=True)
    try:
        users = session.query(DBUser).all()

        # If there are no m4db users ...
        if len(users) == 0:
            # ... tell the user
            print("There are currently no database users.")
        else:
            # ... otherwise print user information
            df_dict = {USERNAME: [],
                       FIRST_NAME: [],
                       INITIALS: [],
                       SURNAME: [],
                       EMAIL: [],
                       TELEPHONE: []}
            for user in users:
                df_dict[USERNAME].append(user.user_name)
                df_dict[FIRST_NAME].append(user.first_name)
                df_dict[INITIALS].append(user.initials)
                df_dict[SURNAME].append(user.surname)
                df_dict[EMAIL].append(user.email)
                df_dict[TELEPHONE].append(user.telephone)
            df = pd.DataFrame(df_dict)
            if csv_file:
                df.to_csv(csv_file, index=False)
            else:
                print(tabulate(df, headers="keys", tablefmt="psql", showindex=False))
    finally:
        session.close()


@app.command()
def add(user_name: str, first_name: str, surname: str, email: str, initials: str = None, telephone: str = None):
    r"""
    Adds a new database user.
    :param user_name: the username to identify the new user.
    :param first_name: the first name of the new user.
    :param surname: the surname of the new user.
    :param email: the email of the new user.
    :param initials: initials of the new user.
    :param telephone: the telephone number of the new user.
    """
    session = get_session(nullpool=True)

    try:
        create_db_user(session, user_name, first_name, surname, email, initials, telephone)

    except ValueError as e:
        print("User not created - something went wrong.")

    finally:
        session.close()


def entry_point():
    app()


if __name__ == "__main__":
    app()
