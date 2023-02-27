import shutil

from subprocess import Popen

from urllib.parse import urlparse

from m4db_database.configuration import read_config_from_environ


def setup_dataset_1():
    config = read_config_from_environ()

    result = urlparse(config.database.uri)
    db_name = result.path.replace("/", "")
    file_root = config.database.file_root

    # We use subprocess to destroy and recreate the database to get around issues with psycopg2's proclivity to
    # create transaction blocks (which prevent us from dropping databases).

    # Delete database directories.
    shutil.rmtree(file_root, ignore_errors=True)

    # Drop database.
    proc1 = Popen(
        f"echo 'drop database {db_name}' | psql -U postgres -h localhost",
        shell=True, universal_newlines=True
    )
    stdout, stderr = proc1.communicate()

    # Create database.
    proc2 = Popen(
        f"echo 'create database {db_name}' | psql -U postgres -h localhost",
        shell=True, universal_newlines=True)
    stdout, stderr = proc2.communicate()

    # Regenerate database.
    proc3 = Popen(
        f"m4db-setup-database {db_name} {file_root} --yes-to-all",
        shell=True, universal_newlines=True)
    stdout, stderr = proc3.communicate()

    # Populate with required test data.

    proc4 = Popen(
        "m4db-user add testuser Test User test.user@testurl.com",
        shell=True, universal_newlines=True)
    stdout, stderr = proc4.communicate()

    proc5 = Popen(
        "m4db-project add testproject 'A test project'",
        shell=True, universal_newlines=True)
    stdout, stderr = proc5.communicate()

    proc6 = Popen(
        "m4db-software add merrill 1.8.1 --executable='/home/m4dbdev/Install/merrill/1.8.1/bin/merrill'",
        shell=True, universal_newlines=True)
    stdout, stderr = proc6.communicate()

    proc7 = Popen(
        "m4db-geometry add-ellipsoid "
        "/data/meshes/all-ellipsoids/ellipsoid_40nm_3nm_pro_1p400_obl_1p700.pat "
        "0.040 0.003 ESVD 1.4 1.7 "
        "--exodus-file /data/meshes/all-ellipsoids/ellipsoid_40nm_3nm_pro_1p400_obl_1p700.e "
        "--mesh-gen-script /data/meshes/all-ellipsoids/ellipsoid_40nm_3nm_pro_1p400_obl_1p700.cubit "
        "--mesh-gen-stdout /data/meshes/all-ellipsoids/ellipsoid_40nm_3nm_pro_1p400_obl_1p700.stdout "
        "--unique-id 04c5e362-3c21-485b-8983-bbde335d60fc",
        shell=True, universal_newlines=True)
    stdout, stderr = proc7.communicate()

    proc8 = Popen(
        "m4db-geometry add-ellipsoid /data/meshes/all-ellipsoids/ellipsoid_40nm_3nm_pro_1p400_obl_1p000.pat "
        "0.040 0.003 ESVD 1.4 1.0 "
        "--exodus-file /data/meshes/all-ellipsoids/ellipsoid_40nm_3nm_pro_1p400_obl_1p000.e "
        "--mesh-gen-script /data/meshes/all-ellipsoids/ellipsoid_40nm_3nm_pro_1p400_obl_1p000.cubit "
        "--mesh-gen-stdout /data/meshes/all-ellipsoids/ellipsoid_40nm_3nm_pro_1p400_obl_1p000.stdout "
        "--unique-id 77fa4246-2378-4fc1-99de-92bd4479202f",
        shell=True, universal_newlines=True)
    stdout, stderr = proc8.communicate()

    proc9 = Popen(
        "m4db-model add /data/datasets/new_models_test_specimen_01.json "
        "testuser testproject merrill 1.8.1 --no-dry-run",
        shell=True, universal_newlines=True)
    stdout, stderr = proc9.communicate()
