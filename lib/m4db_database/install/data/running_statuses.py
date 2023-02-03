r"""
Add supported running statuses to the database.
"""

from m4db_database.orm.latest import RunningStatus


def populate_running_statuses(session):
    r"""
    Create running statues.
    Args:
        session: the session to the database to which we add running statues.

    Returns: None

    """
    session.add(RunningStatus(name="not-run", description="a model that has not been run yet"))
    session.add(RunningStatus(name="re-run", description="a model that is scheduled for a re-run"))
    session.add(RunningStatus(name="running", description="a model that is currently running scheduled to run"))
    session.add(RunningStatus(name="finished", description="a model that is finished running"))
    session.add(RunningStatus(name="crashed", description="a model that has crashed"))
    session.add(RunningStatus(name="scheduled", description="a job that has been scheduled for running"))
    session.commit()
