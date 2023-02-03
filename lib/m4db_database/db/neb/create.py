r"""
A set of routines to create new NEB paths.
"""
from m4db_database.configuration import read_config_from_environ

from m4db_database.orm.latest import Software
from m4db_database.orm.latest import Project
from m4db_database.orm.latest import DBUser
from m4db_database.orm.latest import Metadata
from m4db_database.orm.latest import Model
from m4db_database.orm.latest import UniformField
from m4db_database.orm.latest import Unit
from m4db_database.orm.latest import NEBRunData
from m4db_database.orm.latest import NEBReportData
from m4db_database.orm.latest import RunningStatus
from m4db_database.orm.latest import NEB
from m4db_database.orm.latest import NEBCalculationType

from m4db_database.db.neb.check_endpoint_exists import parent_path_with_models_exists


class PathExternalFieldKWArgs:
    kw_external_field_x = "external_field_x"
    kw_external_field_y = "external_field_y"
    kw_external_field_z = "external_field_z"
    kw_external_field_strength = "external_field_strength"
    kw_external_field_unit = "external_field_unit"

    def __init__(self, **kwargs):
        self.ext_field_complete = False
        self.ext_field_empty = False
        self.ext_field_x = None
        if FSPathWithNEBChildKWArgs.kw_external_field_x in kwargs.keys():
            self.ext_field_x = kwargs[FSPathWithNEBChildKWArgs.kw_external_field_x]

        self.ext_field_y = None
        if FSPathWithNEBChildKWArgs.kw_external_field_y in kwargs.keys():
            self.ext_field_y = kwargs[FSPathWithNEBChildKWArgs.kw_external_field_y]

        self.ext_field_z = None
        if FSPathWithNEBChildKWArgs.kw_external_field_z in kwargs.keys():
            self.ext_field_z = kwargs[FSPathWithNEBChildKWArgs.kw_external_field_z]

        self.ext_field_strength = None
        if FSPathWithNEBChildKWArgs.kw_external_field_strength in kwargs.keys():
            self.ext_field_strength = kwargs[FSPathWithNEBChildKWArgs.kw_external_field_strength]

        self.ext_field_unit = "mT"
        if FSPathWithNEBChildKWArgs.kw_external_field_unit in kwargs.keys():
            self.ext_field_unit = kwargs[FSPathWithNEBChildKWArgs.kw_external_field_unit]

        self.ext_field_complete = self.ext_field_x is not None \
                                  and self.ext_field_y is not None \
                                  and self.ext_field_z is not None \
                                  and self.ext_field_strength is not None

        self.ext_field_empty = self.ext_field_x is None \
                               and self.ext_field_y is None \
                               and self.ext_field_z is None \
                               and self.ext_field_strength is None


class FSNEBPathKWArgs(PathExternalFieldKWArgs):
    kw_model_unique_id_one = "model_unique_id_one"
    kw_model_unique_id_two = "model_unique_id_two"
    kw_no_of_points = "no_of_points"
    kw_max_energy_evaluations = "max_energy_evaluations"
    kw_max_path_evaluations = "max_path_evaluations"
    kw_project = "project"
    kw_db_user = "db_user"
    kw_software = "software"
    kw_software_version = "software_version"

    def __init__(self, **kwargs):
        # Initialize external field data.
        super().__init__(**kwargs)

        config = read_config_from_environ()

        if FSNEBPathKWArgs.kw_model_unique_id_one not in kwargs.keys():
            raise ValueError("'model_unique_id_one' is missing")
        self.model_unique_id_one = kwargs[FSNEBPathKWArgs.kw_model_unique_id_one]

        if FSNEBPathKWArgs.kw_model_unique_id_two not in kwargs.keys():
            raise ValueError("'model_unique_id_two' is missing")
        self.model_unique_id_two = kwargs[FSNEBPathKWArgs.kw_model_unique_id_two]

        self.no_of_points = 100
        if FSNEBPathKWArgs.kw_no_of_points in kwargs.keys():
            self.no_of_points = kwargs[FSNEBPathKWArgs.kw_no_of_points]

        self.max_energy_evaluations = 10000
        if FSNEBPathKWArgs.kw_max_energy_evaluations in kwargs.keys():
            self.max_energy_evaluations = kwargs[FSNEBPathKWArgs.kw_max_energy_evaluations]

        self.max_path_evaluations = 5000
        if FSNEBPathKWArgs.kw_max_path_evaluations in kwargs.keys():
            self.max_path_evaluations = kwargs[FSNEBPathKWArgs.kw_max_path_evaluations]

        self.project = config["m4db_serverside"]["default_m4db_project"]
        if FSNEBPathKWArgs.kw_project in kwargs.keys():
            self.project = kwargs[FSNEBPathKWArgs.kw_project]

        self.db_user = config["m4db_serverside"]["default_m4db_user"]
        if FSNEBPathKWArgs.kw_db_user in kwargs.keys():
            self.db_user = kwargs[FSNEBPathKWArgs.kw_db_user]

        self.software = config["m4db_serverside"]["default_micromag_software"]
        if FSNEBPathKWArgs.kw_software in kwargs.keys():
            self.software = kwargs[FSNEBPathKWArgs.kw_software]

        self.software_version = config["m4db_serverside"]["default_micromag_software_version"]
        if FSNEBPathKWArgs.kw_software_version in kwargs.keys():
            self.software_version = kwargs[FSNEBPathKWArgs.kw_software_version]


class ChildNEBKWArgs(PathExternalFieldKWArgs):
    kw_parent_unique_id = "parent_unique_id"
    kw_spring_constant = "spring_constant"
    kw_curvature_weight = "curvature_weight"
    kw_no_of_points = "no_of_points"
    kw_max_energy_evaluations = "max_energy_evaluations"
    kw_max_path_evaluations = "max_path_evaluations"
    kw_project = "project"
    kw_db_user = "db_user"
    kw_software = "software"
    kw_software_version = "software_version"
    kw_use_parent_external_field = "use-parent-external-field"

    def __init__(self, **kwargs):
        # Initialize external field data.
        super().__init__(**kwargs)

        config = read_config_from_environ()

        if ChildNEBKWArgs.kw_parent_unique_id not in kwargs.keys():
            raise ValueError(f"'{ChildNEBKWArgs.kw_parent_unique_id}' is missing")
        self.parent_unique_id = kwargs[ChildNEBKWArgs.kw_parent_unique_id]

        self.spring_constant = None
        if ChildNEBKWArgs.kw_spring_constant in kwargs.keys():
            self.spring_constant = kwargs[ChildNEBKWArgs.kw_spring_constant]

        self.curvature_weight = None
        if ChildNEBKWArgs.kw_curvature_weight in kwargs.keys():
            self.curvature_weight = kwargs[ChildNEBKWArgs.kw_curvature_weight]

        self.no_of_points = 100
        if ChildNEBKWArgs.kw_no_of_points in kwargs.keys():
            self.no_of_points = kwargs[ChildNEBKWArgs.kw_no_of_points]

        self.max_energy_evaluations = 10000
        if ChildNEBKWArgs.kw_max_energy_evaluations in kwargs.keys():
            self.max_energy_evaluations = kwargs[ChildNEBKWArgs.kw_max_energy_evaluations]

        self.max_path_evaluations = 5000
        if ChildNEBKWArgs.kw_max_path_evaluations in kwargs.keys():
            self.max_path_evaluations = kwargs[ChildNEBKWArgs.kw_max_path_evaluations]

        self.project = config["m4db_serverside"]["default_m4db_project"]
        if ChildNEBKWArgs.kw_project in kwargs.keys():
            self.project = kwargs[ChildNEBKWArgs.kw_project]

        self.db_user = config["m4db_serverside"]["default_m4db_user"]
        if ChildNEBKWArgs.kw_db_user in kwargs.keys():
            self.db_user = kwargs[ChildNEBKWArgs.kw_db_user]

        self.software = config["m4db_serverside"]["default_micromag_software"]
        if ChildNEBKWArgs.kw_software in kwargs.keys():
            self.software = kwargs[ChildNEBKWArgs.kw_software]

        self.software_version = config["m4db_serverside"]["default_micromag_software_version"]
        if ChildNEBKWArgs.kw_software_version in kwargs.keys():
            self.software_version = kwargs[ChildNEBKWArgs.kw_software_version]

        self.use_parent_external_field = False
        if ChildNEBKWArgs.kw_use_parent_external_field in kwargs.keys():
            self.use_parent_external_field = kwargs[ChildNEBKWArgs.kw_use_parent_external_field]


class FSPathWithNEBChildKWArgs(PathExternalFieldKWArgs):
    kw_model_id_one = "model_unique_id_one"
    kw_model_id_two = "model_unique_id_two"
    kw_spring_constant = "spring_constant"
    kw_curvature_weight = "curvature_weight"
    kw_no_of_points = "no_of_points"
    kw_max_energy_evaluations = "max_energy_evaluations"
    kw_max_path_evaluations = "max_path_evaluations"
    kw_project = "project"
    kw_db_user = "db_user"
    kw_software = "software"
    kw_software_version = "software_version"
    kw_force_parent = "force_parent"

    def __init__(self, **kwargs):
        # Initialize external field data.
        super().__init__(**kwargs)

        config = read_config_from_environ()

        if FSPathWithNEBChildKWArgs.kw_model_id_one not in kwargs.keys():
            raise ValueError("'model_unique_id_one' is missing")
        self.model_id_one = kwargs[FSPathWithNEBChildKWArgs.kw_model_id_one]

        self.spring_constant = None
        if FSPathWithNEBChildKWArgs.kw_spring_constant in kwargs.keys():
            self.spring_constant = kwargs[FSPathWithNEBChildKWArgs.kw_spring_constant]

        self.curvature_weight = None
        if FSPathWithNEBChildKWArgs.kw_curvature_weight in kwargs.keys():
            self.curvature_weight = kwargs[FSPathWithNEBChildKWArgs.kw_curvature_weight]

        if FSPathWithNEBChildKWArgs.kw_model_id_two not in kwargs.keys():
            raise ValueError("'model_unique_id_two' is missing")
        self.model_id_two = kwargs[FSPathWithNEBChildKWArgs.kw_model_id_two]

        self.no_of_points = 100
        if FSPathWithNEBChildKWArgs.kw_no_of_points in kwargs.keys():
            self.no_of_points = kwargs[FSPathWithNEBChildKWArgs.kw_no_of_points]

        self.max_energy_evaluations = 10000
        if FSPathWithNEBChildKWArgs.kw_max_energy_evaluations in kwargs.keys():
            self.max_energy_evaluations = kwargs[FSPathWithNEBChildKWArgs.kw_max_energy_evaluations]

        self.max_path_evaluations = 5000
        if FSPathWithNEBChildKWArgs.kw_max_path_evaluations in kwargs.keys():
            self.max_path_evaluations = kwargs[FSPathWithNEBChildKWArgs.kw_max_path_evaluations]

        self.project = config["m4db_serverside"]["default_m4db_project"]
        if FSPathWithNEBChildKWArgs.kw_project in kwargs.keys():
            self.project = kwargs[FSPathWithNEBChildKWArgs.kw_project]

        self.db_user = config["m4db_serverside"]["default_m4db_user"]
        if FSPathWithNEBChildKWArgs.kw_db_user in kwargs.keys():
            self.db_user = kwargs[FSPathWithNEBChildKWArgs.kw_db_user]

        self.software = config["m4db_serverside"]["default_micromag_software"]
        if FSPathWithNEBChildKWArgs.kw_software in kwargs.keys():
            self.software = kwargs[FSPathWithNEBChildKWArgs.kw_software]

        self.software_version = config["m4db_serverside"]["default_micromag_software_version"]
        if FSPathWithNEBChildKWArgs.kw_software_version in kwargs.keys():
            self.software_version = kwargs[FSPathWithNEBChildKWArgs.kw_software_version]


def create_fs_path(session, **kwargs):
    r"""
    Create a new FS NEB model parent NEB model.
    :param session: the database session object.
    :param kwargs: keyword argument parameters.
    :return: a tuple of a unique_id and a boolean which is True if the path was just created of False if it already
             existed
    """
    args = FSNEBPathKWArgs(**kwargs)

    # If the user is adding an external field
    if args.ext_field_complete:
        print(f"FS path external field information follows")
        print(f"   x direction : {args.ext_field_x}")
        print(f"   y direction : {args.ext_field_y}")
        print(f"   z direction : {args.ext_field_z}")
        print(f"   magnitude   : {args.ext_field_strength} {args.ext_field_unit}")
        unit = session.query(Unit).filter(Unit.symbol == args.ext_field_unit).one()
        external_field = UniformField(dx=args.ext_field_x,
                                      dy=args.ext_field_y,
                                      dz=args.ext_field_z,
                                      magnitude=args.ext_field_strength,
                                      unit=unit)
    elif args.ext_field_empty:
        external_field = None
    else:
        raise ValueError("Field is partially defined, please define x, y, z direction and strength (in mT by default)")

    project = session.query(Project).filter(Project.name == args.project).one()
    db_user = session.query(DBUser).filter(DBUser.user_name == args.db_user).one()
    software = session.query(Software). \
        filter(Software.name == args.software). \
        filter(Software.version == args.software_version). \
        one()

    model_one = session.query(Model).filter(Model.unique_id == args.model_unique_id_one).one()
    model_two = session.query(Model).filter(Model.unique_id == args.model_unique_id_two).one()

    running_status = session.query(RunningStatus).filter(RunningStatus.name == "not-run").one()

    calculation_type = session.query(NEBCalculationType).filter(NEBCalculationType.name == "fs_heuristic").one()

    neb = NEB(
        no_of_points=args.no_of_points,
        max_energy_evaluations=args.max_energy_evaluations,
        max_path_evaluations=args.max_path_evaluations,
        external_field=external_field,
        start_model=model_one,
        end_model=model_two,
        parent_neb=None,
        neb_calculation_type=calculation_type,
        neb_run_data=NEBRunData(),
        neb_report_data=NEBReportData(),
        running_status=running_status,
        mdata=Metadata(
            project=project,
            db_user=db_user,
            software=software
        )
    )

    session.add(neb)
    session.commit()

    return neb.unique_id, True


def create_neb_child_path(session, **kwargs):
    args = ChildNEBKWArgs(**kwargs)

    # Retrieve the parent NEB.
    parent_neb = session.query(NEB).filter(NEB.unique_id == args.parent_unique_id).one()

    if args.use_parent_external_field:
        # If the parent had an external field, re-use it
        ext_field_inherited_from_parent = "yes"
        external_field = UniformField(
            dx=parent_neb.external_field.dir_x,
            dy=parent_neb.external_field.dir_y,
            dz=parent_neb.external_field.dir_z,
            magnitude=parent_neb.external_field.magnitude,
            unit=parent_neb.external_field.unit
        )
    else:
        # If we are given a complete external field then use it.
        ext_field_inherited_from_parent = "no"
        if args.ext_field_complete:
            ext_field_inherited_from_parent = "no"
            unit = session.query(Unit).filter(Unit.symbol == args.ext_field_unit).one()
            external_field = UniformField(
                dx=args.ext_field_x,
                dy=args.ext_field_y,
                dz=args.ext_field_z,
                magnitude=args.ext_field_strength,
                unit=unit
            )
        elif args.ext_field_empty:
            external_field = None
        else:
            raise ValueError("Field is partially defined, please define x, y, z direction and strength (in mT by default)")

    print(f"Child NEB path (parent '{parent_neb.unique_id}') external field information follows")
    if external_field is not None:
        print(f"    inherited? : {ext_field_inherited_from_parent}")
        print(f"   x direction : {args.ext_field_x}")
        print(f"   y direction : {args.ext_field_y}")
        print(f"   z direction : {args.ext_field_z}")
        print(f"   magnitude   : {args.ext_field_strength} {args.ext_field_unit}")
    else:
        print("   there is no external field")

    running_status = session.query(RunningStatus).filter(RunningStatus.name == "not-run").one()

    calculation_type = session.query(NEBCalculationType).filter(NEBCalculationType.name == "neb").one()

    neb = NEB(
        spring_constant=args.spring_constant,
        curvature_weight=args.curvature_weight,
        no_of_points=args.no_of_points,
        max_energy_evaluations=args.max_energy_evaluations,
        max_path_evaluations=args.max_path_evaluations,
        external_field=external_field,
        start_model=parent_neb.start_model,
        end_model=parent_neb.end_model,
        parent_neb=parent_neb,
        neb_calculation_type=calculation_type,
        neb_run_data=NEBRunData(),
        neb_report_data=NEBReportData(),
        running_status=running_status,
        mdata=Metadata(
            project=parent_neb.mdata.project,
            db_user=parent_neb.mdata.db_user,
            software=parent_neb.mdata.software
        )
    )

    session.add(neb)
    session.commit()

    return neb.unique_id


def create_fs_path_with_neb_child(session, **kwargs):
    parent_unique_id, _ = create_fs_path(session, **kwargs)
    child_unique_id = create_neb_child_path(session, parent_unique_id=parent_unique_id, **kwargs)

    return parent_unique_id, child_unique_id
