r"""
A set of utilities that check whether an neb path with the given start/end model unique_ids exists.
"""

from sqlalchemy.orm import aliased

from m4db_database.orm.schema import Model
from m4db_database.orm.schema import NEB


def parent_path_with_models_exists(session, model_unique_id_one, model_unique_id_two):
    r"""
    Check to see whether a parent NEB with the given start/end unique IDs already exists in the NEB table; a parent
    NEB is an NEB that has no parent itself.
    :param session: the database session object.
    :param model_unique_id_one: a model unique ID.
    :param model_unique_id_two: a second model unique ID.
    :return: the unique ID of the NEB if it already exists, otherwise return None
    """

    StartModel = aliased(Model, name="StartModel")
    EndModel = aliased(Model, name="EndModel")

    # Check that `model_unique_id_one` and `model_unique_id_two` are not the start/end respectively.
    result = session.query(NEB).\
        join(StartModel, StartModel.id == NEB.start_model_id).\
        join(EndModel, EndModel.id == NEB.end_model_id).\
        filter(StartModel.unique_id == model_unique_id_one).\
        filter(EndModel.unique_id == model_unique_id_two).\
        filter(NEB.parent_neb == None).\
        one_or_none()

    if result:
        return result.unique_id

    # Check that `model_unique_id_two` and `model_unique_id_one` are not the start/end respectively.
    result = session.query(NEB). \
        join(StartModel, StartModel.id == NEB.start_model_id). \
        join(EndModel, EndModel.id == NEB.end_model_id). \
        filter(StartModel.unique_id == model_unique_id_two). \
        filter(EndModel.unique_id == model_unique_id_one). \
        filter(NEB.parent_neb == None). \
        one_or_none()

    if result:
        return result.unique_id
    else:
        return None
