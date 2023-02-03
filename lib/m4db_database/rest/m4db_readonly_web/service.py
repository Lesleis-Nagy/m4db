import falcon

from m4db_database.configuration import read_config_from_environ
from m4db_database.sessions import get_session
from m4db_database.utilities_logging import get_logger

from m4db_database.rest.middleware import SQLAlchemySessionManager
from m4db_database.rest.middleware import ConfigurationManager
from m4db_database.rest.middleware import LoggerManager

from m4db_database.rest.m4db_readonly_web.get_model_file import GetAllModelDataZip
from m4db_database.rest.m4db_readonly_web.get_model_file import GetModelJSONZip
from m4db_database.rest.m4db_readonly_web.get_model_file import GetModelTecplotZip

from m4db_database.rest.m4db_readonly_web.get_neb_file import GetAllNEBDataZip

from m4db_database.rest.m4db_readonly_web.get_running_statuses import GetRunningStatuses

from m4db_database.rest.m4db_readonly_web.get_software_items import GetSoftwareItems

from m4db_database.rest.m4db_readonly_web.get_projects import GetProjects

from m4db_database.rest.m4db_readonly_web.get_geometry import GetAllGeometryNames
from m4db_database.rest.m4db_readonly_web.get_geometry import GetGeometrySizes

Session = get_session(scoped=True, echo=False)
config = read_config_from_environ()
logger = get_logger()
app = falcon.App(
    middleware=[
        SQLAlchemySessionManager(Session),
        ConfigurationManager(config),
        LoggerManager(logger)
    ]
)

# Service to get a model data.zip.
get_all_model_data_zip = GetAllModelDataZip()
app.add_route(
    "/model/all/{unique_id}.zip", get_all_model_data_zip
)

# Service to get an archived version of the model data as JSON
get_model_json_zip = GetModelJSONZip()
app.add_route(
    "/model/json/{unique_id}.zip", get_model_json_zip
)

# Service to get an archived version of the model data as tecplot
get_model_tecplot_zip = GetModelTecplotZip()
app.add_route(
    "/model/tecplot/{unique_id}.zip", get_model_tecplot_zip
)

# Service to get an NEB data.zip.
get_all_neb_data_zip = GetAllNEBDataZip()
app.add_route(
    "/neb/all/{unique_id}.zip", get_all_neb_data_zip
)

# Service to get running statuses
get_running_statuses = GetRunningStatuses()
app.add_route(
    "/running-statuses", get_running_statuses
)

# Service to get software items.
get_software_items = GetSoftwareItems()
app.add_route(
    "/software-items", get_software_items
)

# Service to get projects.
get_projects = GetProjects()
app.add_route(
    "/projects", get_projects
)

# Service to get geometry names.
get_all_geometry_names = GetAllGeometryNames()
app.add_route(
    "/get-all-geometry-names", get_all_geometry_names
)

# Service to get geometry sizes.
get_geometry_sizes = GetGeometrySizes()
app.add_route(
    "/geometry-sizes/{geometry_name}", get_geometry_sizes
)
