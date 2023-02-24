r"""
A collection of routines for retrieving running statuses.
"""

from m4db_database.orm.schema import RunningStatus

from m4db_database import GLOBAL


def retrieve_running_status(session, running_status_name):
    r"""
    Retrieve a running status with the given running status name.
    :param session: a database session.
    :param running_status_name: running status name.
    :return: a RunningStatus object.
    """
    # Attempt to retrieve the running status.
    running_status = session.query(RunningStatus).filter(RunningStatus.name == running_status_name).one_or_none()
    # If the running status cannot be found ...
    if running_status is None:
        # ... raise error
        raise ValueError("Running status '{}' cannot be found.".format(running_status_name))

    return running_status


def retrieve_not_run_status(session):
    r"""
    Retrieve the 'not-run' running status.
    :param session: a database session.
    :return: a RunningStatus object.
    """
    return retrieve_running_status(session, GLOBAL.running_status_not_run)


def retrieve_re_run_running_status(session):
    r"""
    Retrieve the 're-run' running status.
    :param session: a database session.
    :return: a RunningStatus object.
    """
    # Attempt to retrieve the 'rerun' running status.
    return retrieve_running_status(session, GLOBAL.running_status_re_run)


def retrieve_running_running_status(session):
    r"""
    Retrieve the 'running' running status.
    :param session: a database session.
    :return: a RunningStatus object.
    """
    # Attempt to retrieve the 'running' running status.
    return retrieve_running_status(session, GLOBAL.running_status_running)


def retrieve_finished_running_status(session):
    r"""
    Retrieve the 'finished' running status.
    :param session: a database session.
    :return: a RunningStatus object.
    """
    # Attempt to retrieve the 'finished' running status.
    return retrieve_running_status(session, GLOBAL.running_status_finished)


def retrieve_crashed_running_status(session):
    r"""
    Retrieve the 'crashed' running status.
    :param session: a database session.
    :return: a RunningStatus object.
    """
    # Attempt to retrieve the 'crashed' running status.
    return retrieve_running_status(session, GLOBAL.running_status_crashed)


def retrieve_scheduled_running_status(session):
    r"""
    Retrieve the 'scheduled' running status.
    :param session: a database session.
    :return: a RunningStatus object.
    """
    # Attempt to retrieve the 'scheduled' running status.
    return retrieve_running_status(session, GLOBAL.running_status_scheduled)


def retrieve_failed_running_status(session):
    r"""
    Retrieve the 'failed' running status.
    :param session: a database session.
    :return: a RunningStatus object.
    """
    # Attempt to retrieve the 'failed' running status.
    return retrieve_running_status(session, GLOBAL.running_status_failed)