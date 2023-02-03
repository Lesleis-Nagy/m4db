from m4db_database.orm.latest import Model
from m4db_database.orm.latest import Metadata
from m4db_database.orm.latest import ModelRunData
from m4db_database.orm.latest import ModelReportData

from m4db_database.db.geometry.retrieve import retrieve_geometry
from m4db_database.db.model_material_associations.create import create_model_material_associations
from m4db_database.db.model_materials_text.create import create_model_materials_text
from m4db_database.db.initial_magnetization.create import create_initial_magnetization
from m4db_database.db.external_field.create import create_external_field
from m4db_database.db.running_status.retrieve import retrieve_not_run_status
from m4db_database.db.db_user.retrieve import retrieve_db_user
from m4db_database.db.project.retrieve import retrieve_project
from m4db_database.db.software.retrieve import retrieve_software


def create_model(session, json_model_dict, user_name, project_name, software_name, software_version, max_evals=100000,
                 reps=1):
    r"""
    Adds a new model to m4db.
    :param session: the database session
    :param json_model_dict: dictionary containing the new model data.
    :param user_name: the database use that the model belongs to.
    :param project_name: the project that the model belongs to.
    :param software_name: the software that will execute the model.
    :param software_version: the software that will execute the model.
    :param max_evals: the maximum number of evaluations.
    :param reps: the number of repetitions of the same model (useful with random initial field).
    :return: a list of the unique ids of the model's we've added to the database.
    """

    # These fields need to be completed for a new model
    geometry = retrieve_geometry(session, json_model_dict)
    running_status = retrieve_not_run_status(session)
    db_user = retrieve_db_user(user_name, session)
    project = retrieve_project(session, project_name)
    software = retrieve_software(session, software_name, software_version)

    models = []
    for rep in range(reps):
        start_magnetization = create_initial_magnetization(session, json_model_dict)
        external_field = create_external_field(session, json_model_dict)

        # Create a new metadata object
        metadata = Metadata(
            db_user=db_user,
            software=software,
            project=project
        )

        # Create model material text data
        mma = create_model_materials_text(json_model_dict)

        # Build the new model and save it to the database
        model = Model(
            geometry=geometry,
            start_magnetization=start_magnetization,
            external_field=external_field,
            running_status=running_status,
            mdata=metadata,
            model_materials_text=mma,
            model_run_data=ModelRunData(),
            model_report_data=ModelReportData(),
            max_energy_evaluations=max_evals
        )

        # Add materials
        model_material_associations = create_model_material_associations(session, json_model_dict)
        for mma in model_material_associations:
            model.materials.append(mma)

        # Add the model to the database.
        session.add(model)

        # Append model to models
        models.append(model)

    # Commit the session
    session.commit()

    # Process build a list of unique model ids that we've just added.
    unique_id_list = list([model.unique_id for model in models])

    # Return the list of unique model ids.
    return unique_id_list
