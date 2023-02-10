import typer

from m4db_database.orm.latest import DBUser

from m4db_database.sessions import get_session

from m4db_database.db.db_user.create import create_db_user

from m4db_database.utilities.access_levels import string_to_access_level

app = typer.Typer()


@app.command()
def list():
    r"""
    Create a new model from input piped from stdin.
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
            for user in users:
                print("Print details for user: {}".format(user.user_name))
                print("   First name: {}".format(user.first_name))
                print("   Initials:   {}".format(user.initials))
                print("   Surname:    {}".format(user.surname))
                print("   Email:      {}".format(user.email))
                print("   Telephone:  {}".format(user.telephone))
                print("")
    finally:
        session.close()


@app.command()
def add(user_name: str, first_name: str, surname: str, email: str, initials: str = None, telephone: str = None):
    r"""
    Adds a new database user.
    :user_name: the username to identify the new user.
    :first_name: the first name of the new user.
    :surname: the surname of the new user.
    :email: the email of the new user.
    :initial: initials of the new user.
    :telephone: the telephone number of the new user.
    """
    session = get_session(nullpool=True)

    access_level = string_to_access_level("ADMIN")
    ticket_length = 1000

    try:
        db_user = create_db_user(
            user_name,
            first_name,
            surname,
            email,
            access_level,
            ticket_length,
            session,
            initials,
            telephone)
        session.add(db_user)
        session.commit()
    except ValueError as exception_obj:
        print(str(exception_obj))
    finally:
        session.close()


def entry_point():
    app()


if __name__ == "__main__":
    app()