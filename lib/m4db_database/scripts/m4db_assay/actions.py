r"""
Perform actions for the 'm4db_assay' scripts.
"""
import pandas as pd
from tabulate import tabulate


from m4db_database.sessions import get_session

from m4db_database.orm.latest import RunningStatus
from m4db_database.orm.latest import Model
from m4db_database.orm.latest import NEB


def model_general_action():
    r"""
    Display general m4db assay statistics for models.
    :return: None
    """
    session = get_session(nullpool=True)

    # Retrieve all running statuses.
    statuses = session.query(RunningStatus).all()

    # For each running status do a count.
    tot_nmodels = 0

    model_stats = {
        "Running status": [],
        "No. of models": []
    }
    for status in statuses:
        nmodels = session.query(Model).filter(Model.running_status_id == status.id).count()
        tot_nmodels += nmodels

        model_stats["Running status"].append(status.name)
        model_stats["No. of models"].append(nmodels)

    df = pd.DataFrame.from_dict(model_stats)
    print("Model data")
    print(tabulate(df, headers='keys', tablefmt='psql'))
    print("Total no. of models: {}".format(tot_nmodels))


def neb_general_action():
    r"""
    Display general m4db assay statistics for NEBs.
    :return: None
    """
    session = get_session(nullpool=True)

    # Retrieve all running statuses.
    statuses = session.query(RunningStatus).all()

    # For each running status do a count.
    tot_nnebs = 0

    neb_stats = {
        "Running status": [],
        "No. of NEBs": []
    }
    for status in statuses:
        nnebs = session.query(NEB).filter(NEB.running_status_id == status.id).count()
        tot_nnebs += nnebs

        neb_stats["Running status"].append(status.name)
        neb_stats["No. of NEBs"].append(nnebs)
    df = pd.DataFrame.from_dict(neb_stats)
    print("NEB data")
    print(tabulate(df, headers="keys", tablefmt="psql"))
    print(f"Total no. of NEBs: {tot_nnebs}")


