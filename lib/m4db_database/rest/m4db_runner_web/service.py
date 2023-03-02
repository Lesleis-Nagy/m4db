import falcon

from m4db_database.configuration import read_config_from_environ

from m4db_database.utilities.logger import setup_logger, get_logger

from m4db_database.sessions import get_session

from m4db_database.rest.middleware import SQLAlchemySessionManager, LoggerManager

from m4db_database.rest.m4db_runner_web.is_alive import IsAlive

from m4db_database.rest.m4db_runner_web.get_software_executable import GetSoftware

from m4db_database.rest.m4db_runner_web.get_model_merrill_script import GetModelMerrillScript
from m4db_database.rest.m4db_runner_web.get_model_run_prerequisites import GetModelRunPrerequisites
from m4db_database.rest.m4db_runner_web.get_model_running_status import GetModelRunningStatus
from m4db_database.rest.m4db_runner_web.get_model_software_executable import GetModelSoftwareExecutable
from m4db_database.rest.m4db_runner_web.get_model_initial_magnetization import GetModelInitialMagnetization

from m4db_database.rest.m4db_runner_web.set_model_running_status import SetModelRunningStatus
from m4db_database.rest.m4db_runner_web.set_model_quants import SetModelQuants

#
# from m4db_database.rest.m4db_runner_web.set_neb_running_status import SetNEBRunningStatus
# from m4db_database.rest.m4db_runner_web.is_neb_parent_blocking import IsNEBParentBlocking
# from m4db_database.rest.m4db_runner_web.get_neb_merrill_script import GetNEBMerrillScript
# from m4db_database.rest.m4db_runner_web.get_neb_software_executable import GetNEBSoftwareExecutable
# from m4db_database.rest.m4db_runner_web.get_neb_start_end_unique_ids import GetNebStartEndUniqueIds
# from m4db_database.rest.m4db_runner_web.get_neb_partent_unique_id import GetNEBParentUniqueId

config = read_config_from_environ()

setup_logger(config.logging.file, config.logging.level, config.logging.log_to_stdout)
logger = get_logger()

Session = get_session(scoped=True, echo=False)

app = falcon.App(
    middleware=[
        SQLAlchemySessionManager(Session),
        LoggerManager(logger)
    ]
)

# Model: get merrill model scripts.
get_model_merrill_script = GetModelMerrillScript()
app.add_route(
    "/get-model-merrill-script/{unique_id}", get_model_merrill_script
)

# Model: get model running status.
get_model_running_status = GetModelRunningStatus()
app.add_route(
    "/get-model-running-status/{unique_id}", get_model_running_status
)

# Model: get model software executable.
get_model_software_executable = GetModelSoftwareExecutable()
app.add_route(
    "/get-model-software-executable/{unique_id}",
    get_model_software_executable
)

# Model: get model start magnetization.
get_model_initial_magnetization = GetModelInitialMagnetization()
app.add_route(
    "/get-model-initial-magnetization/{unique_id}",get_model_initial_magnetization
)

# Model: get model prerequisites.
get_model_run_prerequisites = GetModelRunPrerequisites()
app.add_route(
    "/get-model-run-prerequisites/{unique_id}", get_model_run_prerequisites
)

# Model: set running status service.
set_model_running_status = SetModelRunningStatus()
app.add_route(
    "/set-model-running-status", set_model_running_status
)

# Model: set quants service.
set_model_quants = SetModelQuants()
app.add_route(
    "/set-model-quants", set_model_quants
)

# Service to verify that the web runner is alive.
is_alive = IsAlive()
app.add_route(
    '/is-alive', is_alive
)

# Service to retrieve a software executable.
get_software_executable = GetSoftware()
app.add_route(
    "/get-software-executable/{name}/{version}",
    get_software_executable
)









#
#
#
# # NEB: set running status service.
# set_neb_running_status = SetNEBRunningStatus()
# app.add_route(
#     "/set_neb_running_status", set_neb_running_status
# )
#
# # NEB: query if an NEB parent is blocking this NEB from running (see above).
# is_neb_parent_blocking = IsNEBParentBlocking()
# app.add_route(
#     "/is_neb_parent_blocking/{unique_id}", is_neb_parent_blocking
# )
#
# # NEB: get merrill neb scripts.
# get_neb_merrill_script = GetNEBMerrillScript()
# app.add_route(
#     "/get_neb_merrill_script/{unique_id}", get_neb_merrill_script
# )
#
# # NEB: get NEB software executable.
# get_neb_software_executable = GetNEBSoftwareExecutable()
# app.add_route(
#     "/get_neb_software_executable/{unique_id}", get_neb_software_executable
# )
#
# # NEB: get start/end model unique ids
# get_neb_start_end_unique_ids = GetNebStartEndUniqueIds()
# app.add_route(
#     "/get_neb_start_end_unique_ids/{unique_id}", get_neb_start_end_unique_ids
# )
#
# # NEB: is this NEB parentless
# get_neb_parent_unique_id = GetNEBParentUniqueId()
# app.add_route(
#     "/get_neb_parent_unique_id/{unique_id}", get_neb_parent_unique_id
# )
