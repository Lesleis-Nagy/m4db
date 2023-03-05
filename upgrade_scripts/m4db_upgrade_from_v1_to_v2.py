r"""
A selection of routines to quickly upgrade a database from v1 to v2.
"""
import random
import datetime

from argparse import ArgumentParser

from sqlalchemy.sql import text

from tqdm import tqdm

from m4db.m4db_utilities_utilities import password_hash
from m4db.m4db_utilities_utilities import random_password

from m4db.sessions import get_session_from_args

from m4db import GLOBAL


def drop_unique_constraints(new_session):
    r"""
    Disable/drop all unique constraints on the new database.
    :param new_session: a connection to the v2 (new) database.
    :return: None
    """
    # anisotropy_form
    print("Dropping unique constraints for table 'anisotropy_form'")
    new_session.execute("alter table anisotropy_form drop constraint if exists uniq_anisotropy_form_01")

    # db_user
    print("Dropping unique constraints for table 'db_user'")
    new_session.execute("alter table db_user drop constraint if exists uniq_db_user_01")
    new_session.execute("alter table db_user drop constraint if exists uniq_db_user_02")

    # geometry
    print("Dropping unique constraints for table 'geometry'")
    new_session.execute("alter table geometry drop constraint if exists uniq_geometry_01")
    new_session.execute("alter table geometry drop constraint if exists uniq_geometry_02")

    # material
    print("Dropping unique constraints for table 'material'")
    new_session.execute("alter table material drop constraint if exists uniq_material_01")

    # model
    print("Dropping unique constraints for table 'model'")
    new_session.execute("alter table model drop constraint if exists uniq_model_01")

    # neb
    print("Dropping unique constraints for table 'neb'")
    new_session.execute("alter table neb drop constraint if exists uniq_neb_01")

    # physical_constant
    print("Dropping unique constraints for table 'physical_constant'")
    new_session.execute("alter table physical_constant drop constraint if exists uniq_physical_constant_01")

    # running_status
    print("Dropping unique constraints for table 'running_status'")
    new_session.execute("alter table running_status drop constraint if exists uniq_running_status_01")

    # software
    print("Dropping unique constraints for table 'software'")
    new_session.execute("alter table software drop constraint if exists uniq_software_01")

    # unit
    print("Dropping unique constraints for table 'unit'")
    new_session.execute("alter table unit drop constraint if exists uniq_unit_01")

    new_session.commit()


def drop_foreign_key_constraints(new_session):
    r"""
    Disable/drop all foreign key constraints on the new database.
    :param new_session: a connection to the v2 (new) database.
    :return: None
    """
    # geometry
    print("Dropping foreign key constraints for table 'geometry'")
    new_session.execute("alter table geometry drop constraint if exists geometry_element_size_unit_id_fkey")
    new_session.execute("alter table geometry drop constraint if exists geometry_size_convention_id_fkey")
    new_session.execute("alter table geometry drop constraint if exists geometry_size_unit_id_fkey")
    new_session.execute("alter table geometry drop constraint if exists geometry_software_id_fkey")

    # material
    print("Dropping foreign key constraints for table 'material'")
    new_session.execute("alter table material drop constraint if exists material_anisotropy_form_id_fkey")

    # metadata
    print("Dropping foreign key constraints for table 'metadata'")
    new_session.execute("alter table metadata drop constraint if exists metadata_db_user_id_fkey")
    new_session.execute("alter table metadata drop constraint if exists metadata_project_id_fkey")
    new_session.execute("alter table metadata drop constraint if exists metadata_software_id_fkey")

    # model
    print("Dropping foreign key constraints for table 'model'")
    new_session.execute("alter table model drop constraint if exists model_external_field_id_fkey")
    new_session.execute("alter table model drop constraint if exists model_geometry_id_fkey")
    new_session.execute("alter table model drop constraint if exists model_legacy_model_info_id_fkey")
    new_session.execute("alter table model drop constraint if exists model_mdata_id_fkey")
    new_session.execute("alter table model drop constraint if exists model_model_materials_text_id_fkey")
    new_session.execute("alter table model drop constraint if exists model_model_report_data_id_fkey")
    new_session.execute("alter table model drop constraint if exists model_model_run_data_id_fkey")
    new_session.execute("alter table model drop constraint if exists model_running_status_id_fkey")
    new_session.execute("alter table model drop constraint if exists model_start_magnetization_id_fkey")

    # model_field
    print("Dropping foreign key constraints for table 'model_field'")
    new_session.execute("alter table model_field drop constraint if exists model_field_id_fkey")
    new_session.execute("alter table model_field drop constraint if exists model_field_model_id_fkey")

    # model_material_association
    print("Dropping foreign key constraints for table 'model_material_association'")
    new_session.execute("alter table model_material_association drop constraint if exists model_material_association_material_id_fkey")
    new_session.execute("alter table model_material_association drop constraint if exists model_material_association_model_id_fkey")

    # neb
    print("Dropping foreign key constraints for table 'neb'")
    new_session.execute("alter table neb drop constraint if exists neb_end_model_id_fkey")
    new_session.execute("alter table neb drop constraint if exists neb_external_field_id_fkey")
    new_session.execute("alter table neb drop constraint if exists neb_mdata_id_fkey")
    new_session.execute("alter table neb drop constraint if exists neb_neb_calculation_type_id_fkey")
    new_session.execute("alter table neb drop constraint if exists neb_neb_report_data_id_fkey")
    new_session.execute("alter table neb drop constraint if exists neb_neb_run_data_id_fkey")
    new_session.execute("alter table neb drop constraint if exists neb_parent_neb_id_fkey")
    new_session.execute("alter table neb drop constraint if exists neb_running_status_id_fkey")
    new_session.execute("alter table neb drop constraint if exists neb_start_model_id_fkey")

    # neb_model_split
    print("Dropping foreign key constraints for table 'neb_model_split'")
    new_session.execute("alter table neb_model_split drop constraint if exists neb_model_split_model_id_fkey")
    new_session.execute("alter table neb_model_split drop constraint if exists neb_model_split_neb_id_fkey")

    # random_field
    print("Dropping foreign key constraints for table 'random_field'")
    new_session.execute("alter table random_field drop constraint if exists random_field_id_fkey")

    # uniform_field
    print("Dropping foreign key constraints for table 'uniform_field'")
    new_session.execute("alter table uniform_field drop constraint if exists uniform_field_id_fkey")
    new_session.execute("alter table uniform_field drop constraint if exists uniform_field_unit_id_fkey")

    new_session.commit()


def drop_primary_key_constraints(new_session):
    r"""
    Disable/drop all primary key constraints on the new database.
    :param new_session: a connection to the v2 (new) databse.
    :return: None
    """
    # anisotropy_form
    print("Dropping primary key from table 'anisotropy_form'")
    new_session.execute("alter table anisotropy_form drop constraint if exists anisotropy_form_pkey")

    # db_user
    print("Dropping primary key from table 'db_user'")
    new_session.execute("alter table db_user drop constraint if exists db_user_pkey")

    # field
    print("Dropping primary key from table 'field'")
    new_session.execute("alter table field drop constraint if exists field_pkey")

    # geometry
    print("Dropping primary key from table 'geometry'")
    new_session.execute("alter table geometry drop constraint if exists geometry_pkey")

    # legacy_model_info
    print("Dropping primary key from table 'legacy_model_info'")
    new_session.execute("alter table legacy_model_info drop constraint if exists legacy_model_info_pkey")

    # material
    print("Dropping primary key from table 'material'")
    new_session.execute("alter table material drop constraint if exists material_pkey")

    # metadata
    print("Dropping primary key from table 'metadata'")
    new_session.execute("alter table metadata drop constraint if exists metadata_pkey")

    # model
    print("Dropping primary key from table 'model'")
    new_session.execute("alter table model drop constraint if exists model_pkey")

    # model_field
    print("Dropping primary key from table 'model_field'")
    new_session.execute("alter table model_field drop constraint if exists model_field_pkey")

    # model_material_association
    print("Dropping primary key from table 'model_material_association'")
    new_session.execute("alter table model_material_association drop constraint if exists model_material_association_pkey")

    # model_materials_text
    print("Dropping primary key from table 'model_materials_text'")
    new_session.execute("alter table model_materials_text drop constraint if exists model_materials_text_pkey")

    # model_report_data
    print("Dropping primary key from table 'model_report_data'")
    new_session.execute("alter table model_report_data drop constraint if exists model_report_data_pkey")

    # model_run_data
    print("Dropping primary key from table 'model_run_data'")
    new_session.execute("alter table model_run_data drop constraint if exists model_run_data_pkey")

    # neb
    print("Dropping primary key from table 'neb'")
    new_session.execute("alter table neb drop constraint if exists neb_pkey")

    # neb_calculation_type
    print("Dropping primary key from table 'neb_calculation_type'")
    new_session.execute("alter table neb_calculation_type drop constraint if exists neb_calculation_type_pkey")

    # neb_model_split
    print("Dropping primary key from table 'neb_model_split'")
    new_session.execute("alter table neb_model_split drop constraint if exists neb_model_split_pkey")

    # neb_report_data
    print("Dropping primary key from table 'neb_report_data'")
    new_session.execute("alter table neb_report_data drop constraint if exists neb_report_data_pkey")

    # neb_run_data
    print("Dropping primary key from table 'neb_run_data'")
    new_session.execute("alter table neb_run_data drop constraint if exists neb_run_data_pkey")

    # physical_constant
    print("Dropping primary key from table 'physical_constant'")
    new_session.execute("alter table physical_constant drop constraint if exists physical_constant_pkey")

    # project
    print("Dropping primary key from table 'project'")
    new_session.execute("alter table project drop constraint if exists project_pkey")

    # random_field
    print("Dropping primary key from table 'random_field'")
    new_session.execute("alter table random_field drop constraint if exists random_field_pkey")

    # running_status
    print("Dropping primary key from table 'running_status'")
    new_session.execute("alter table running_status drop constraint if exists running_status_pkey")

    # size_convention
    print("Dropping primary key from table 'size_convention'")
    new_session.execute("alter table size_convention drop constraint if exists size_convention_pkey")

    # software
    print("Dropping primary key from table 'software'")
    new_session.execute("alter table software drop constraint if exists software_pkey")

    # uniform_field
    print("Dropping primary key from table 'uniform_field'")
    new_session.execute("alter table uniform_field drop constraint if exists uniform_field_pkey")

    # unit
    print("Dropping primary key from table 'unit'")
    new_session.execute("alter table unit drop constraint if exists unit_pkey")

    new_session.commit()


def drop_all_constraints(new_session):
    r"""
    Disable/drop all the constraints on the new database.
    :param new_session: a connection to the v2 (new) database.
    :return: None
    """
    # Drop the unique constraints.
    drop_unique_constraints(new_session)

    # Drop the foreign key constraints.
    drop_foreign_key_constraints(new_session)

    # Drop the primary key constraints.
    drop_primary_key_constraints(new_session)


def enable_unique_constraints(new_session):
    r"""
    Enable/recreate all unique constraints on the new database.
    :param new_session: a connection to the v2 (new) database.
    :return: None
    """
    # anisotropy_form
    print("Enabling unique constraints for table 'anisotropy_form'")
    new_session.execute("alter table anisotropy_form add constraint uniq_anisotropy_form_01 unique (name)")

    # db_user
    print("Enabling unique constraints for table 'db_user'")
    new_session.execute("alter table db_user add constraint uniq_db_user_01 unique (first_name, surname, email, telephone)")
    new_session.execute("alter table db_user add constraint uniq_db_user_02 unique (user_name)")

    # geometry
    print("Enabling unique constraints for table 'geometry'")
    new_session.execute("alter table geometry add constraint uniq_geometry_01 unique (name, size, size_unit_id)")
    new_session.execute("alter table geometry add constraint uniq_geometry_02 unique (unique_id)")

    # material
    print("Enabling unique constraints for table 'material'")
    new_session.execute("alter table material add constraint uniq_material_01 unique (name, temperature)")

    # model
    print("Enabling unique constraints for table 'model'")
    new_session.execute("alter table model add constraint uniq_model_01 unique (unique_id)")

    # neb
    print("Enabling unique constraints for table 'neb'")
    new_session.execute("alter table neb add constraint uniq_neb_01 unique (unique_id)")

    # physical_constant
    print("Enabling unique constraints for table 'physical_constant'")
    new_session.execute("alter table physical_constant add constraint uniq_physical_constant_01 unique (symbol)")

    # running_status
    print("Enabling unique constraints for table 'running_status'")
    new_session.execute("alter table running_status add constraint uniq_running_status_01 unique (name)")

    # software
    print("Enabling unique constraints for table 'software'")
    new_session.execute("alter table software add constraint uniq_software_01 unique (name, version)")

    # unit
    print("Enabling unique constraints for table 'unit'")
    new_session.execute("alter table unit add constraint uniq_unit_01 unique (symbol)")

    new_session.commit()


def enable_foreign_key_constraints(new_session):
    r"""
    Enable/recreate all foreign key constraints on the new databse.
    :param new_session: a connection to the v2 (new) database.
    :return: None
    """
    # geometry
    print("Enabling foreign key constraints for table 'geometry'")
    new_session.execute("alter table geometry add constraint geometry_element_size_unit_id_fkey FOREIGN KEY (element_size_unit_id) REFERENCES unit(id)")
    new_session.execute("alter table geometry add constraint geometry_size_convention_id_fkey FOREIGN KEY (size_convention_id) REFERENCES size_convention(id)")
    new_session.execute("alter table geometry add constraint geometry_size_unit_id_fkey FOREIGN KEY (size_unit_id) REFERENCES unit(id)")
    new_session.execute("alter table geometry add constraint geometry_software_id_fkey FOREIGN KEY (software_id) REFERENCES software(id)")

    # material
    print("Enabling foreign key constraints for table 'material'")
    new_session.execute("alter table material add constraint material_anisotropy_form_id_fkey FOREIGN KEY (anisotropy_form_id) REFERENCES anisotropy_form(id)")

    # metadata
    print("Enabling foreign key constraints for table 'metadata'")
    new_session.execute("alter table metadata add constraint metadata_db_user_id_fkey FOREIGN KEY (db_user_id) REFERENCES db_user(id)")
    new_session.execute("alter table metadata add constraint metadata_project_id_fkey FOREIGN KEY (project_id) REFERENCES project(id)")
    new_session.execute("alter table metadata add constraint metadata_software_id_fkey FOREIGN KEY (software_id) REFERENCES software(id)")

    # model
    print("Enabling foreign key constraints for table 'model'")
    new_session.execute("alter table model add constraint model_external_field_id_fkey FOREIGN KEY (external_field_id) REFERENCES field(id)")
    new_session.execute("alter table model add constraint model_geometry_id_fkey FOREIGN KEY (geometry_id) REFERENCES geometry(id)")
    new_session.execute("alter table model add constraint model_legacy_model_info_id_fkey FOREIGN KEY (legacy_model_info_id) REFERENCES legacy_model_info(id)")
    new_session.execute("alter table model add constraint model_mdata_id_fkey FOREIGN KEY (mdata_id) REFERENCES metadata(id)")
    new_session.execute("alter table model add constraint model_model_materials_text_id_fkey FOREIGN KEY (model_materials_text_id) REFERENCES model_materials_text(id)")
    new_session.execute("alter table model add constraint model_model_report_data_id_fkey FOREIGN KEY (model_report_data_id) REFERENCES model_report_data(id)")
    new_session.execute("alter table model add constraint model_model_run_data_id_fkey FOREIGN KEY (model_run_data_id) REFERENCES model_run_data(id)")
    new_session.execute("alter table model add constraint model_running_status_id_fkey FOREIGN KEY (running_status_id) REFERENCES running_status(id)")
    new_session.execute("alter table model add constraint model_start_magnetization_id_fkey FOREIGN KEY (start_magnetization_id) REFERENCES field(id)")

    # model_field
    print("Enabling foreign key constraints for table 'model_field'")
    new_session.execute("alter table model_field add constraint model_field_id_fkey FOREIGN KEY (id) REFERENCES field(id)")
    new_session.execute("alter table model_field add constraint model_field_model_id_fkey FOREIGN KEY (model_id) REFERENCES model(id)")

    # model_material_association
    print("Enabling foreign key constraints for table 'model_material_association'")
    new_session.execute("alter table model_material_association add constraint model_material_association_material_id_fkey FOREIGN KEY (material_id) REFERENCES material(id)")
    new_session.execute("alter table model_material_association add constraint model_material_association_model_id_fkey FOREIGN KEY (model_id) REFERENCES model(id)")

    # neb
    print("Enabling foreign key constraints for table 'neb'")
    new_session.execute("alter table neb add constraint neb_end_model_id_fkey FOREIGN KEY (end_model_id) REFERENCES model(id)")
    new_session.execute("alter table neb add constraint neb_external_field_id_fkey FOREIGN KEY (external_field_id) REFERENCES field(id)")
    new_session.execute("alter table neb add constraint neb_mdata_id_fkey FOREIGN KEY (mdata_id) REFERENCES metadata(id)")
    new_session.execute("alter table neb add constraint neb_neb_calculation_type_id_fkey FOREIGN KEY (neb_calculation_type_id) REFERENCES neb_calculation_type(id)")
    new_session.execute("alter table neb add constraint neb_neb_report_data_id_fkey FOREIGN KEY (neb_report_data_id) REFERENCES neb_report_data(id)")
    new_session.execute("alter table neb add constraint neb_neb_run_data_id_fkey FOREIGN KEY (neb_run_data_id) REFERENCES neb_run_data(id)")
    new_session.execute("alter table neb add constraint neb_parent_neb_id_fkey FOREIGN KEY (parent_unique_id) REFERENCES neb(id)")
    new_session.execute("alter table neb add constraint neb_running_status_id_fkey FOREIGN KEY (running_status_id) REFERENCES running_status(id)")
    new_session.execute("alter table neb add constraint neb_start_model_id_fkey FOREIGN KEY (start_model_id) REFERENCES model(id)")

    # neb_model_split
    print("Enabling foreign key constraints for table 'neb_model_split'")
    new_session.execute("alter table neb_model_split add constraint neb_model_split_model_id_fkey FOREIGN KEY (model_id) REFERENCES model(id)")
    new_session.execute("alter table neb_model_split add constraint neb_model_split_neb_id_fkey FOREIGN KEY (neb_id) REFERENCES neb(id)")

    # random_field
    print("Enabling foreign key constraints for table 'random_field'")
    new_session.execute("alter table random_field add constraint random_field_id_fkey FOREIGN KEY (id) REFERENCES field(id)")

    # uniform_field
    print("Enabling foreign key constraints for table 'uniform_field'")
    new_session.execute("alter table uniform_field add constraint uniform_field_id_fkey FOREIGN KEY (id) REFERENCES field(id)")
    new_session.execute("alter table uniform_field add constraint uniform_field_unit_id_fkey FOREIGN KEY (unit_id) REFERENCES unit(id)")

    new_session.commit()


def enable_primary_key_constraints(new_session):
    r"""
    Enable/recreate all primary key constraints on the new databse.
    :param new_session: a connection to the v2 (new) database.
    :return: None
    """
    # anisotropy_form
    print("Enabling primary key from table 'anisotropy_form'")
    new_session.execute("alter table anisotropy_form add primary key (id)")

    # db_user
    print("Enabling primary key from table 'db_user'")
    new_session.execute("alter table db_user add primary key (id)")

    # field
    print("Enabling primary key from table 'field'")
    new_session.execute("alter table field add primary key (id)")

    # geometry
    print("Enabling primary key from table 'geometry'")
    new_session.execute("alter table geometry add primary key (id)")

    # legacy_model_info
    print("Enabling primary key from table 'legacy_model_info'")
    new_session.execute("alter table legacy_model_info add primary key (id)")

    # material
    print("Enabling primary key from table 'material'")
    new_session.execute("alter table material add primary key (id)")

    # metadata
    print("Enabling primary key from table 'metadata'")
    new_session.execute("alter table metadata add primary key (id)")

    # model
    print("Enabling primary key from table 'model'")
    new_session.execute("alter table model add primary key (id)")

    # model_field
    print("Enabling primary key from table 'model_field'")
    new_session.execute("alter table model_field add primary key (id)")

    # model_material_association
    print("Enabling primary key from table 'model_material_association'")
    new_session.execute("alter table model_material_association add primary key (model_id, material_id)")

    # model_materials_text
    print("Enabling primary key from table 'model_materials_text'")
    new_session.execute("alter table model_materials_text add primary key (id)")

    # model_report_data
    print("Enabling primary key from table 'model_report_data'")
    new_session.execute("alter table model_report_data add primary key (id)")

    # model_run_data
    print("Enabling primary key from table 'model_run_data'")
    new_session.execute("alter table model_run_data add primary key (id)")

    # neb
    print("Enabling primary key from table 'neb'")
    new_session.execute("alter table neb add primary key (id)")

    # neb_calculation_type
    print("Enabling primary key from table 'neb_calculation_type'")
    new_session.execute("alter table neb_calculation_type add primary key (id)")

    # neb_model_split
    print("Enabling primary key from table 'neb_model_split'")
    new_session.execute("alter table neb_model_split add primary key (id)")

    # neb_report_data
    print("Enabling primary key from table 'neb_report_data'")
    new_session.execute("alter table neb_report_data add primary key (id)")

    # neb_run_data
    print("Enabling primary key from table 'neb_run_data'")
    new_session.execute("alter table neb_run_data add primary key (id)")

    # physical_constant
    print("Enabling primary key from table 'physical_constant'")
    new_session.execute("alter table physical_constant add primary key (id)")

    # project
    print("Enabling primary key from table 'project'")
    new_session.execute("alter table project add primary key (id)")

    # random_field
    print("Enabling primary key from table 'random_field'")
    new_session.execute("alter table random_field add primary key (id)")

    # running_status
    print("Enabling primary key from table 'running_status'")
    new_session.execute("alter table running_status add primary key (id)")

    # size_convention
    print("Enabling primary key from table 'size_convention'")
    new_session.execute("alter table size_convention add primary key (id)")

    # software
    print("Enabling primary key from table 'software'")
    new_session.execute("alter table software add primary key (id)")

    # uniform_field
    print("Enabling primary key from table 'uniform_field'")
    new_session.execute("alter table uniform_field add primary key (id)")

    # unit
    print("Enabling primary key from table 'unit'")
    new_session.execute("alter table unit add primary key (id)")

    new_session.commit()


def enable_all_constraints(new_session):
    r"""
    Enable/recreate all constraints on the new database.
    :param new_session: a connection to the v2 (new) database.
    :return: None
    """

    # Recreate the primary key constraints.
    enable_primary_key_constraints(new_session)

    # Recreate the foreign key constraints.
    enable_foreign_key_constraints(new_session)

    # Recreate the unique key constraints.
    enable_unique_constraints(new_session)


def copy_anisotropy_form(old_session, new_session):
    r"""
    Copy over anisotropy form information.
    :param old_session: a connection to the v1 (old) database.
    :param new_session: a connection to the v2 (new) database.
    :return: None
    """
    #print("Copying data for table 'anisotropy_form'")

    # Retrieve data from old database.
    records = old_session.execute("""
        select 
            id, name, description, last_modified, created
        from anisotropy_form
    """)

    # Construct new data and insert in to new database.
    insert_items = [
        {"id": record[0],
         "name": record[1],
         "description": record[2],
         "last_modified": record[3],
         "created": record[4]}
        for record in records]

    new_session.execute("delete from anisotropy_form")

    insert_statement = text("""
        insert into anisotropy_form 
            (id, name, description, last_modified, created)
        values (:id, :name, :description, :last_modified, :created)
    """)

    for insert_item in tqdm(insert_items, desc="Anisotropy forms"):
        new_session.execute(insert_statement, params=insert_item)

    new_session.commit()


def copy_db_user(old_session, new_session):
    r"""
    Copy over anisotropy form information.
    :param old_session: a connection to the v1 (old) database.
    :param new_session: a connection to the v2 (new) database.
    :return: None
    """
    #print("Copying data for table 'db_user'")

    # Retrieve data from old database.
    records = old_session.execute("""
        select 
            id, user_name, first_name, initials, surname, email, telephone, last_modified, created
        from db_user
    """)

    # Construct new data and insert in to new database.
    ticket_length = 3600  # default ticket length is 1hr in seconds.
    ticket_timeout = GLOBAL.UNIX_EPOCH  # automatically timed out.
    access_level = GLOBAL.ACCESS_ALL
    insert_items = [
        {"id": record[0],
         "user_name": record[1],
         "password": password_hash(random_password()),
         "first_name": record[2],
         "initials": record[3],
         "surname": record[4],
         "email": record[5],
         "telephone": record[6],
         "ticket_hash": None,
         "ticket_length": ticket_length,
         "ticket_timeout": ticket_timeout,
         "access_level": access_level,
         "last_modified": record[7],
         "created": record[8]} for record in records
    ]

    new_session.execute("delete from db_user")

    insert_statement = text("""
        insert into db_user
            (id, user_name, password, first_name, initials, surname, email, telephone, ticket_hash, ticket_length, ticket_timeout, access_level, last_modified, created)
        values 
            (:id, :user_name, :password, :first_name, :initials, :surname, :email, :telephone, :ticket_hash, :ticket_length, :ticket_timeout, :access_level, :last_modified, :created)
    """)

    for insert_item in tqdm(insert_items, desc="DB users"):
        new_session.execute(insert_statement, params=insert_item)

    new_session.commit()


def copy_field(old_session, new_session):
    r"""
    Copy over field table information.
    :param old_session: a connection to the v1 (old) database.
    :param new_session: a connection to the v2 (new) database.
    :return: None
    """
    #print("Copying data for table 'field'")

    # Retrieve data from old database.
    records = old_session.execute("""
        select 
            id, type, last_modified, created
        from field
    """)

    # Construct new data and insert it in to new database.
    insert_items = [
        {"id": record[0],
         "type": record[1],
         "last_modified": record[2],
         "created": record[3]} for record in records
    ]

    new_session.execute("delete from field")

    insert_statement = text("""
        insert into field
            (id, type, last_modified, created)
        values
            (:id, :type, :last_modified, :created)
    """)

    for insert_item in tqdm(insert_items, desc="Fields"):
        new_session.execute(insert_statement, params=insert_item)

    new_session.commit()


def copy_geometry(old_session, new_session):
    r"""
    Copy over anisotropy form information.
    :param old_session: a connection to the v1 (old) database.
    :param new_session: a connection to the v2 (new) database.
    :return: None
    """
    #print("Copying data for table 'geometry'")

    # Retrieve data from old database.
    records = old_session.execute("""
        select
            id, unique_id, name, size, element_size, description, nelements, nvertices, nsubmeshes, volume_total, 
            has_patran, has_exodus, has_mesh_gen_script, has_mesh_gen_output, last_modified, created, size_unit_id, 
            element_size_unit_id, size_convention_id, software_id
        from
            geometry
    """)

    # Construct new data and insert in to new database.
    insert_items = [
        {"id":record[0],
         "unique_id": record[1],
         "name": record[2],
         "size": record[3],
         "element_size": record[4],
         "description": record[5],
         "nelements": record[6],
         "nvertices": record[7],
         "nsubmeshes": record[8],
         "volume_total": record[9],
         "has_patran": record[10],
         "has_exodus": record[11],
         "has_mesh_gen_script": record[12],
         "has_mesh_gen_output": record[13],
         "last_modified": record[14],
         "created": record[15],
         "size_unit_id": record[16],
         "element_size_unit_id": record[17],
         "size_convention_id": record[18],
         "software_id": record[19]} for record in records
    ]

    new_session.execute("delete from geometry")

    insert_statement = text("""
        insert into geometry
            (id, unique_id, name, size, element_size, description, nelements, nvertices, nsubmeshes, volume_total, 
             has_patran, has_exodus, has_mesh_gen_script, has_mesh_gen_output, last_modified, created, size_unit_id, 
             element_size_unit_id, size_convention_id, software_id)
        values
            (:id, :unique_id, :name, :size, :element_size, :description, :nelements, :nvertices, :nsubmeshes, 
             :volume_total, :has_patran, :has_exodus, :has_mesh_gen_script, :has_mesh_gen_output, :last_modified, 
             :created, :size_unit_id, :element_size_unit_id, :size_convention_id, :software_id)
    """)

    for insert_item in tqdm(insert_items, desc="Geometries"):
        new_session.execute(insert_statement, params=insert_item)

    new_session.commit()


def copy_legacy_model_info(old_session, new_session):
    r"""
    Copy over legacy model information.
    :param old_session: a connection to the v1 (old) database.
    :param new_session: a connection to the v2 (new) database.
    :return: None
    """
    #print("Copying data for table 'legacy_model_info'")

    # Retrieve data from old database.
    records = old_session.execute("""
        select
            id, legacy_model_id, last_modified, created
        from
            legacy_model_info
    """)

    # Construct new data and insert it in to the new database.
    insert_items = [
        {"id": record[0],
         "legacy_model_id": record[1],
         "last_modified": record[2],
         "created": record[3]} for record in records
    ]

    new_session.execute("delete from legacy_model_info")

    insert_statement = text("""
        insert into legacy_model_info
            (id, legacy_model_id, last_modified, created)
        values
            (:id, :legacy_model_id, :last_modified, :created)
    """)

    for insert_item in tqdm(insert_items, desc="Legacy model info"):
        new_session.execute(insert_statement, params=insert_item)

    new_session.commit()


def copy_material(old_session, new_session):
    r"""
    Copy over material table information.
    :param old_session: a connection to the v1 (old) database.
    :param new_session: a connection to the v2 (new) database.
    :return: None
    """
    #print("Copying data for table 'material'")

    # Retrieve data from old database.
    records = old_session.execute("""
        select 
            id, name, temperature, k1, aex, ms, kd, lambda_ex, q_hardness, axis_theta, axis_phi, last_modified,
            created, anisotropy_form_id
        from
            material 
    """)

    # Construct new data and insert in to new database.
    insert_items = [
        {"id": record[0],
         "name": record[1],
         "temperature": record[2],
         "k1": record[3],
         "aex": record[4],
         "ms": record[5],
         "kd": record[6],
         "lambda_ex": record[7],
         "q_hardness": record[8],
         "axis_theta": record[9],
         "axis_phi": record[10],
         "last_modified": record[11],
         "created": record[12],
         "anisotropy_form_id": record[13]} for record in records
    ]

    new_session.execute("delete from material")

    insert_statement = text("""
        insert into material 
            (id, name, temperature, k1, aex, ms, kd, lambda_ex, q_hardness, axis_theta, axis_phi, last_modified,
             created, anisotropy_form_id)
        values
            (:id, :name, :temperature, :k1, :aex, :ms, :kd, :lambda_ex, :q_hardness, :axis_theta, :axis_phi, 
             :last_modified, :created, :anisotropy_form_id)
    """)

    for insert_item in tqdm(insert_items, desc="Materials"):
        new_session.execute(insert_statement, params=insert_item)

    new_session.commit()


def copy_metadata(old_session, new_session):
    r"""
    Copy over metadata table information.
    :param old_session: a connection to the v1 (old) database.
    :param new_session: a connection to the v2 (new) database.
    :return: None
    """
    #print("Copying data for table 'metadata'")

    # Retrieve data from old database.
    records = old_session.execute("""
        select 
            id, last_modified, created, project_id, db_user_id, software_id
        from
            metadata
    """)

    # Construct new data and insert it into new database.
    insert_items = [
        {"id": record[0],
         "last_modified": record[1],
         "created": record[2],
         "project_id": record[3],
         "db_user_id": record[4],
         "software_id": record[5]} for record in records
    ]

    new_session.execute("delete from metadata")

    insert_statement = text("""
        insert into metadata
            (id, last_modified, created, project_id, db_user_id, software_id)
        values
            (:id, :last_modified, :created, :project_id, :db_user_id, :software_id)
    """)

    for insert_item in tqdm(insert_items, desc="Metadata"):
        new_session.execute(insert_statement, params=insert_item)

    new_session.commit()


def copy_model(old_session, new_session):
    r"""
    Copy over model information.
    :param old_session: a connection to the v1 (old) database.
    :param new_session: a connection to the v2 (new) database.
    :return: None
    """
    #print("Copying data for table 'geometry'")

    # Retrieve data from old database.
    records = old_session.execute("""
        select 
            id, unique_id, mx_tot, my_tot, mz_tot, vx_tot, vy_tot, vz_tot, h_tot, adm_tot, e_typical, e_anis, e_ext, 
            e_demag, e_exch1, e_exch2, e_exch3, e_exch4, e_tot, max_energy_evaluations, last_modified, created, 
            geometry_id, start_magnetization_id, external_field_id, running_status_id, model_run_data_id,
            model_report_data_id, mdata_id, legacy_model_info_id
        from
            model
    """)

    # Construct new data and insert into new database.
    model_items = [
        {"id": record[0],
         "unique_id": record[1],
         "mx_tot": record[2],
         "my_tot": record[3],
         "mz_tot": record[4],
         "vx_tot": record[5],
         "vy_tot": record[6],
         "vz_tot": record[7],
         "h_tot": record[8],
         "rh_tot": None,
         "adm_tot": record[9],
         "e_typical": record[10],
         "e_anis": record[11],
         "e_ext": record[12],
         "e_demag": record[13],
         "e_exch1": record[14],
         "e_exch2": record[15],
         "e_exch3": record[16],
         "e_exch4": record[17],
         "e_tot": record[18],
         "volume": None,
         "max_energy_evaluations": record[19],
         "last_modified": record[20],
         "created": record[21],
         "geometry_id": record[22],
         "model_materials_text_id": None,
         "start_magnetization_id": record[23],
         "external_field_id": record[24],
         "running_status_id": record[25],
         "model_run_data_id": record[26],
         "model_report_data_id": record[27],
         "mdata_id": record[28],
         "legacy_model_info_id": record[29]} for record in records
    ]

    new_session.execute("delete from model")
    new_session.execute("delete from model_materials_text")

    insert_statement = text("""
        insert into model
            (id, unique_id, mx_tot, my_tot, mz_tot, vx_tot, vy_tot, vz_tot, h_tot, adm_tot, e_typical, e_anis, e_ext, 
             e_demag, e_exch1, e_exch2, e_exch3, e_exch4, e_tot, max_energy_evaluations, last_modified, created, 
             geometry_id, model_materials_text_id, start_magnetization_id, external_field_id, running_status_id, model_run_data_id,
             model_report_data_id, mdata_id, legacy_model_info_id)
        values
            (:id, :unique_id, :mx_tot, :my_tot, :mz_tot, :vx_tot, :vy_tot, :vz_tot, :h_tot, :adm_tot, :e_typical, 
             :e_anis, :e_ext, :e_demag, :e_exch1, :e_exch2, :e_exch3, :e_exch4, :e_tot, :max_energy_evaluations, 
             :last_modified, :created, :geometry_id, :model_materials_text_id, :start_magnetization_id, 
             :external_field_id, :running_status_id, :model_run_data_id, :model_report_data_id, :mdata_id, 
             :legacy_model_info_id)
    """)

    # For each 'model', we need to create a new 'model_materials_text'.

    model_materials_text_id = 0
    for model_item in tqdm(model_items, desc="Models"):
        # For each copied model, we need to create an associated model_materials_text entry
        materials = old_session.execute("""
            select 
                material.id, material.name, material.temperature, model_material_association.submesh_id
            from model_material_association 
                inner join material on model_material_association.material_id = material.id
            where model_material_association.model_id = {model_id:}
        """.format(model_id=model_item["id"]))

        materials_text_list = []
        materials_submesh_idx_text_list = []
        materials_submesh_idx_text_temperature_list = []

        for material in materials:
            materials_text_list.append(material[1])
            materials_submesh_idx_text_list.append("{}:{}".format(material[3], material[1]))
            materials_submesh_idx_text_temperature_list.append("{}:{}:{}".format(material[3], material[1], material[2]))

        insert_model_materials_text = text("""
            insert into model_materials_text
                (id, materials, submeshidxs_materials, submeshidxs_materials_temperatures, last_modified, created)
            values 
                (:id, :materials, :submeshidxs_materials, :submeshidxs_materials_temperatures, :last_modified, :created)
        """)

        current_time = datetime.datetime.now()
        model_materials_text_item = {"id": model_materials_text_id,
                                     "materials": ",".join(sorted(materials_text_list)),
                                     "submeshidxs_materials": ",".join(materials_submesh_idx_text_list),
                                     "submeshidxs_materials_temperatures": ",".join(materials_submesh_idx_text_temperature_list),
                                     "last_modified": current_time,
                                     "created": current_time}

        new_session.execute(insert_model_materials_text, params=model_materials_text_item)
        model_item["model_materials_text_id"] = model_materials_text_id
        new_session.execute(insert_statement, params=model_item)

        model_materials_text_id += 1

    new_session.commit()


def copy_model_field(old_session, new_session):
    r"""
    Copy over model field information.
    :param old_session: a connection to the v1 (old) database.
    :param new_session: a connection to the v2 (old) database.
    :return: None
    """
    #print("Copying data for table 'model_field'")

    # Retrieve data from old database.
    records = old_session.execute("""
        select 
            id, last_modified, created, model_id
        from 
            model_field
    """)

    # Construct new data and insert in to new database.
    insert_items = [
        {"id": record[0],
         "last_modified": record[1],
         "created": record[2],
         "model_id": record[3]} for record in records
    ]

    new_session.execute("delete from model_field")

    insert_statement = text("""
        insert into model_field
            (id, last_modified, created, model_id)
        values
            (:id, :last_modified, :created, :model_id)
    """)

    for insert_item in tqdm(insert_items, desc="Model fields"):
        new_session.execute(insert_statement, params=insert_item)

    new_session.commit()


def copy_model_material_association(old_session, new_session):
    r"""
    Copy over model material association information.
    :param old_session: a connection to the v1 (old) database.
    :param new_session: a connection to the v2 (new) database.
    :return: None
    """
    #print("Copying data for table 'model_material_association'")

    # Retrieve data from old database.
    records = old_session.execute("""
        select 
            model_id, material_id, submesh_id
        from
            model_material_association
    """)

    # Construct new data and insert in to new database.
    insert_items = [
        {"model_id": record[0],
         "material_id": record[1],
         "submesh_id": record[2]} for record in records
    ]

    new_session.execute("delete from model_material_association")

    insert_statement = text("""
        insert into model_material_association
            (model_id, material_id, submesh_id)
        values
            (:model_id, :material_id, :submesh_id)
    """)

    for insert_item in tqdm(insert_items, desc="Model material associations"):
        new_session.execute(insert_statement, params=insert_item)

    new_session.commit()


def copy_model_report_data(old_session, new_session):
    r"""
    Copy over model report data information.
    :param old_session: a connection to the v1 (old) database.
    :param new_session: a connection to the v2 (new) database.
    :return: None
    """
    #print("Copying data for table 'model_report_data'")

    # Retrieve data from old database.
    records = old_session.execute("""
        select 
            id, has_xy_thumb_png, has_yz_thumb_png, has_xz_thumb_png, has_xy_png, has_yz_png, has_xz_png
        from
            model_report_data
    """)

    # Construct new data and insert into new database.
    insert_items = [
        {"id": record[0],
         "has_xy_thumb_png": record[1],
         "has_yz_thumb_png": record[2],
         "has_xz_thumb_png": record[3],
         "has_xy_png": record[4],
         "has_yz_png": record[5],
         "has_xz_png": record[6]} for record in records
    ]

    insert_statement = text("""
        insert into model_report_data
            (id, has_xy_thumb_png, has_yz_thumb_png, has_xz_thumb_png, has_xy_png, has_yz_png, has_xz_png)
        values
            (:id, :has_xy_thumb_png, :has_yz_thumb_png, :has_xz_thumb_png, :has_xy_png, :has_yz_png, :has_xz_png)
    """)

    for insert_item in tqdm(insert_items, desc="Model reports"):
        new_session.execute(insert_statement, params=insert_item)

    new_session.commit()


def copy_model_run_data(old_session, new_session):
    r"""
    Copy over model run data information.
    :param old_session: a connection to the v1 (old) database.
    :param new_session: a connection to the v2 (new) database.
    :return: None
    """
    #print("Copying data for table 'model_run_data'")

    # Retrieve data from old database.
    records = old_session.execute("""
        select 
            id,  has_script, has_stdout, has_stderr, has_energy_log, has_tecplot, has_json, has_dat, has_helicity_dat,
            has_vorticity_dat, has_adm_dat, last_modified, created
        from
            model_run_data
    """)

    # Construct new data and insert into new database.
    insert_items = [
        {"id": record[0],
         "has_script": record[1],
         "has_stdout": record[2],
         "has_stderr": record[3],
         "has_energy_log": record[4],
         "has_tecplot": record[5],
         "has_json": record[6],
         "has_dat": record[7],
         "has_helicity_dat": record[8],
         "has_vorticity_dat": record[9],
         "has_adm_dat": record[10],
         "last_modified": record[11],
         "created": record[12]} for record in records
    ]

    insert_statement = text("""
        insert into model_run_data
            (id, has_script, has_stdout, has_stderr, has_energy_log, has_tecplot, has_json, has_dat, has_helicity_dat,
             has_vorticity_dat, has_adm_dat, last_modified, created)
        values
            (:id, :has_script, :has_stdout, :has_stderr, :has_energy_log, :has_tecplot, :has_json, :has_dat, 
             :has_helicity_dat, :has_vorticity_dat, :has_adm_dat, :last_modified, :created)
    """)

    for insert_item in tqdm(insert_items, desc="Model run"):
        new_session.execute(insert_statement, params=insert_item)

    new_session.commit()


def copy_neb(old_session, new_session):
    r"""
    Copy over neb data information.
    :param old_session: a connection to the v1 (old) database.
    :param new_session: a connection to the v2 (new) database.
    :return: None
    """
    #print("Copying over data for table 'neb'")

    # Retrieve data from old database.
    records = old_session.execute("""
        select id, 
               unique_id, 
               spring_constant, 
               curvature_weight, 
               no_of_points,
               max_energy_evaluations,
               max_path_evaluations, 
               last_modified, 
               created, 
               start_model_id, 
               end_model_id, 
               parent_unique_id, 
               neb_calculation_type_id, 
               neb_run_data_id, 
               neb_report_data_id, 
               running_status_id, 
               mdata_id, 
               external_field_id 
        from neb
    """)

    # Construct new data and insert into new databse.
    insert_items = [
        {"id": record[0],
         "unique_id": record[1],
         "spring_constant": record[2],
         "curvature_weight": record[3],
         "no_of_points": record[4],
         "max_energy_evaluations": record[5],
         "max_path_evaluations": record[6],
         "energy_barrier": 0.0,
         "last_modified": record[7],
         "created": record[8],
         "external_field_id": record[17],
         "start_model_id": record[9],
         "end_model_id": record[10],
         "parent_unique_id": record[11],
         "neb_calculation_type_id": record[12],
         "neb_run_data_id": record[13],
         "neb_report_data_id": record[14],
         "running_status_id": record[15],
         "mdata_id":record[16]} for record in records
    ]

    new_session.execute("delete from neb")

    insert_statement = text("""
        insert into neb
             (id, unique_id, spring_constant, curvature_weight, no_of_points, max_energy_evaluations, 
              max_path_evaluations, energy_barrier, last_modified, created, external_field_id, start_model_id,
              end_model_id, parent_unique_id, neb_calculation_type_id, neb_run_data_id, neb_report_data_id,
              running_status_id, mdata_id)
        values 
            (:id, :unique_id, :spring_constant, :curvature_weight, :no_of_points, :max_energy_evaluations, 
             :max_path_evaluations, :energy_barrier, :last_modified, :created, :external_field_id, :start_model_id,
             :end_model_id, :parent_unique_id, :neb_calculation_type_id, :neb_run_data_id, :neb_report_data_id,
             :running_status_id, :mdata_id)
    """)

    for insert_item in tqdm(insert_items, desc="NEBs"):
        new_session.execute(insert_statement, params=insert_item)

    new_session.commit()


def copy_neb_calculation_type(old_session, new_session):
    r"""
    Copy over neb calculation db_type information.
    :param old_session: a connection to the v1 (old) database.
    :param new_session: a connection to the v2 (new) database.
    :return: None
    """
    #print("Copying data for table 'neb_calculation_type'")

    # Retrieve data from old database.
    records = old_session.execute("""
        select
            id, name, description, last_modified, created
        from
            neb_calculation_type
    """)

    # Construct new data and insert into new database.
    insert_items = [
        {"id": record[0],
         "name": record[1],
         "description": record[2],
         "last_modified": record[3],
         "created": record[4]} for record in records
    ]

    new_session.execute("delete from neb_calculation_type")

    insert_statement = text("""
        insert into neb_calculation_type
            (id, name, description, last_modified, created)
        values
            (:id, :name, :description, :last_modified, :created)
    """)

    for insert_item in tqdm(insert_items, desc="NEB calculation types"):
        new_session.execute(insert_statement, params=insert_item)

    new_session.commit()


def copy_neb_model_split(old_session, new_session):
    r"""
    Copy over neb model split information.
    :param old_session: a connection to the v1 (old) database.
    :param new_session: a connection to the v2 (new) database.
    :return: None
    """
    #print("Copying data for table 'neb_model_split'")

    # Retrieve data from old database.
    records = old_session.execute("""
        select
            image_number, last_modified, created, neb_id, model_id
        from
            neb_model_split
    """)

    # Construct new data and insert into new database.
    id = 0
    insert_items = []
    for record in records:
        insert_items.append({"id": id,
                             "image_number": record[0],
                             "last_modified": record[1],
                             "created": record[2],
                             "neb_id": record[3],
                             "model_id": record[4]})
        id = id + 1

    new_session.execute("delete from neb_model_split")

    insert_statement = text("""
        insert into new_model_split
            (id, image_number, last_modified, created, neb_id, model_id)
        values
            (:id, :image_number, :last_modified, :created, :neb_id, :model_id)
    """)

    for insert_item in tqdm(insert_items, desc="NEB model split"):
        new_session.execute(insert_statement, params=insert_item)

    new_session.commit()


def copy_neb_report_data(old_session, new_session):
    r"""
    Copy over NEB report data information.
    :param old_session: a connection to the v1 (old) database.
    :param new_session: a connection to the v2 (new) database.
    :return: None
    """
    #print("Copying data for table 'neb_report_data'")

    # Retrieve data from old database.
    records = old_session.execute("""
        select
            id, has_x_thumb_png, has_y_thumb_png, has_z_thumb_png, has_x_png, has_y_png, has_z_png, last_modified,
            created
        from
            neb_report_data
    """)

    # Construct new data and insert into new database.
    insert_items = [
        {"id": record[0],
         "has_x_thumb_png": record[1],
         "has_y_thumb_png": record[2],
         "has_z_thumb_png": record[3],
         "has_x_png": record[4],
         "has_y_png": record[5],
         "has_z_png": record[6],
         "last_modified": record[7],
         "created": record[8]} for record in records
    ]

    new_session.execute("delete from neb_report_data")

    insert_statement = text("""
        insert into neb_report_data
            (id, has_x_thumb_png, has_y_thumb_png, has_z_thumb_png, has_x_png, has_y_png, has_z_png, last_modified,
             created)
        values
            (:id, :has_x_thumb_png, :has_y_thumb_png, :has_z_thumb_png, :has_x_png, :has_y_png, :has_z_png, 
             :last_modified, :created)
    """)

    for insert_item in tqdm(insert_items, desc="NEB report data items"):
        new_session.execute(insert_statement, params=insert_item)

    new_session.commit()


def copy_neb_run_data(old_session, new_session):
    r"""
    Copy over NEB run data information.
    :param old_session: a connection to the v1 (old) database.
    :param new_session: a connection to the v2 (new) database.
    :return: None
    """
    #print("Copying data for table 'neb_run_data'")

    # Retrieve data from old database.
    records = old_session.execute("""
        select
             id, has_script, has_stdout, has_stderr, has_energy_log, has_tecplot, has_neb_energies, last_modified,
             created
        from
            neb_run_data
    """)

    # Construct new data and insert into new database.
    insert_items = [
        {"id": record[0],
         "has_script": record[1],
         "has_stdout": record[2],
         "has_stderr": record[3],
         "has_energy_log": record[4],
         "has_tecplot": record[5],
         "has_neb_energies": record[6],
         "last_modified": record[7],
         "created": record[8]} for record in records
    ]

    new_session.execute("delete from neb_run_data")

    insert_statement = text("""
        insert into neb_run_data
            (id, has_script, has_stdout, has_stderr, has_energy_log, has_tecplot, has_neb_energies, last_modified,
             created)
        values
            (:id, :has_script, :has_stdout, :has_stderr, :has_energy_log, :has_tecplot, :has_neb_energies, 
             :last_modified, :created)
    """)

    for insert_item in tqdm(insert_items, desc="NEB run data"):
        new_session.execute(insert_statement, params=insert_item)

    new_session.commit()


def copy_physical_constant(old_session, new_session):
    r"""
    Copy over physical constant information.
    :param old_session: a connection to the v1 (old) database.
    :param new_session: a connection to the v2 (new) database.
    :return: None
    """
    #print("Copying data for table 'physical_constant'")

    # Retrieve data from old database.
    records = old_session.execute("""
        select
            id, symbol, name, value, unit, last_modified, created
        from
            physical_constant
    """)

    # Construct new data and insert into new database.
    insert_items = [
        {"id": record[0],
         "symbol": record[1],
         "name": record[2],
         "value": record[3],
         "unit": record[4],
         "last_modified":record[5],
         "created": record[6]} for record in records
    ]

    new_session.execute("delete from physical_constant")

    insert_statement = text("""
        insert into physical_constant
            (id, symbol, name, value, unit, last_modified, created)
        values
            (:id, :symbol, :name, :value, :unit, :last_modified, :created)
    """)

    for insert_item in tqdm(insert_items, desc="Physical constants"):
        new_session.execute(insert_statement, params=insert_item)

    new_session.commit()


def copy_project(old_session, new_session):
    r"""
    Copy over project information.
    :param old_session: a connection to the v1 (old) database.
    :param new_session: a connection to the v2 (new) database.
    :return: None
    """
    #print("Copying data for table 'project'")

    # Retrieve data from old database.
    records = old_session.execute("""
        select
            id, name, description
        from
            project
    """)

    # Construct new data and insert into new database.
    now = datetime.datetime.now(datetime.timezone.utc)
    insert_items = [
        {"id": record[0],
         "name": record[1],
         "description": record[2],
         "last_modified": now,
         "created": now} for record in records
    ]

    new_session.execute("delete from project")

    insert_statement = text("""
        insert into project
            (id, name, description, last_modified, created)
        values
            (:id, :name, :description, :last_modified, :created)
    """)

    for insert_item in tqdm(insert_items, desc="Project items"):
        new_session.execute(insert_statement, params=insert_item)

    new_session.commit()


def copy_random_field(old_session, new_session):
    r"""
    Copy over random field information.
    :param old_session: a connection to the v1 (old) database.
    :param new_session: a connection to the v2 (new) database.
    :return: None
    """
    #print("Copying data for table 'random_field'")

    # Retrieve data from old database.
    records = old_session.execute("""
        select
            id, seed, last_modified, created
        from
            random_field
    """)

    # Construct new data and insert into new database.
    insert_items = [
        {"id": record[0],
         "seed": record[1],
         "last_modified": record[2],
         "created": record[3]} for record in records
    ]

    new_session.execute("delete from random_field")

    insert_statement = text("""
        insert into random_field
            (id, seed, last_modified, created)
        values
            (:id, :seed, :last_modified, :created)
    """)

    for insert_item in tqdm(insert_items, desc="Random fields"):
        new_session.execute(insert_statement, params=insert_item)

    new_session.commit()


def copy_running_status(old_session, new_session):
    r"""
    Copy over running status information.
    :param old_session: a connection to the v1 (old) database.
    :param new_session: a connection to the v2 (new) database.
    :return: None
    """
    #print("Copying data for table 'running_status'")

    # Retrieve data from old database.
    records = old_session.execute("""
        select
            id, name, description, last_modified, created
        from
            running_status
    """)

    # Construct new data and insert into new database.
    insert_items = [
        {"id": record[0],
         "name": record[1],
         "description": record[2],
         "last_modified": record[3],
         "created": record[4]} for record in records
    ]

    new_session.execute("delete from running_status")

    insert_statement = text("""
        insert into running_status
            (id, name, description, last_modified, created)
        values
            (:id, :name, :description, :last_modified, :created)
    """)

    for insert_item in tqdm(insert_items, desc="Running statuses"):
        new_session.execute(insert_statement, params=insert_item)

    new_session.commit()


def copy_size_convention(old_session, new_session):
    r"""
    Copy over size convention information.
    :param old_session: a connection to the v1 (old) database.
    :param new_session: a connection to the v2 (new) database.
    :return: None
    """
    #print("Copying data for table 'size_convention'")

    # Retrieve data from old database.
    records = old_session.execute("""
        select
            id, symbol, description, last_modified, created
        from
            size_convention
    """)

    # Construct new data and insert into new database.
    insert_items = [
        {"id": record[0],
         "symbol": record[1],
         "description": record[2],
         "last_modified": record[3],
         "created": record[4]} for record in records
    ]

    new_session.execute("delete from size_convention")

    insert_statement = text("""
        insert into size_convention
            (id, symbol, description, last_modified, created)
        values
            (:id, :symbol, :description, :last_modified, :created)
    """)

    for insert_item in tqdm(insert_items, desc="Size conventions"):
        new_session.execute(insert_statement, params=insert_item)

    new_session.commit()


def copy_software(old_session, new_session):
    r"""
    Copy over software information.
    :param old_session: a connection to the v1 (old) database.
    :param new_session: a connection to the v2 (new) database.
    :return: None
    """
    #print("Copying data for table 'software'")

    # Retrieve data from old database.
    records = old_session.execute("""
        select
            id, name, version, description, url, citation, last_modified, created
        from
            software
    """)

    # Construct new data and insert into new database.
    insert_items = [
        {"id": record[0],
         "name": record[1],
         "version": record[2],
         "description": record[3],
         "url": record[4],
         "citation": record[5],
         "last_modified": record[6],
         "created": record[7]} for record in records
    ]

    new_session.execute("delete from software")

    insert_statement = text("""
        insert into software
            (id, name, version, description, url, citation, last_modified, created)
        values
            (:id, :name, :version, :description, :url, :citation, :last_modified, :created)
    """)

    for insert_item in tqdm(insert_items, desc="Softwares"):
        new_session.execute(insert_statement, params=insert_item)

    new_session.commit()


def copy_uniform_field(old_session, new_session):
    r"""
    Copy over uniform field information.
    :param old_session: a connection to the v1 (old) database.
    :param new_session: a connection to the v2 (new) database.
    :return: None
    """
    #print("Copying data for table 'uniform_field'")

    # Retrieve data from old database.
    records = old_session.execute("""
        select
            id, theta, phi, dir_x, dir_y, dir_z, magnitude, last_modified, created, unit_id
        from
            uniform_field
    """)

    # Construct new data and insert into new database.
    insert_items = [
        {"id": record[0],
         "theta": record[1],
         "phi": record[2],
         "dir_x": record[3],
         "dir_y": record[4],
         "dir_z": record[5],
         "magnitude": record[6],
         "last_modified": record[7],
         "created": record[8],
         "unit_id": record[9]} for record in records
    ]

    new_session.execute("delete from uniform_field")

    insert_statement = text("""
        insert into uniform_field
            (id, theta, phi, dir_x, dir_y, dir_z, magnitude, last_modified, created, unit_id)
        values
            (:id, :theta, :phi, :dir_x, :dir_y, :dir_z, :magnitude, :last_modified, :created, :unit_id)
    """)

    for insert_item in tqdm(insert_items, desc="Uniform fields"):
        new_session.execute(insert_statement, params=insert_item)

    new_session.commit()


def copy_unit(old_session, new_session):
    r"""
    Copy over unit information.
    :param old_session: a connection to the v1 (old) database.
    :param new_session: a connection to the v2 (new) database.
    :return: None
    """
    #print("Copying data for table 'unit'")

    # Retrieve data from old database.
    records = old_session.execute("""
        select
            id, symbol, name, power, last_modified, created
        from
            unit
    """)

    # Construct new data and insert into new database.
    insert_items = [
        {"id": record[0],
         "symbol": record[1],
         "name": record[2],
         "power": record[3],
         "last_modified": record[4],
         "created": record[5]} for record in records
    ]

    new_session.execute("delete from unit")

    insert_statement = text("""
        insert into unit
            (id, symbol, name, power, last_modified, created)
        values
            (:id, :symbol, :name, :power, :last_modified, :created)
    """)

    for insert_item in tqdm(insert_items, desc="Units"):
        new_session.execute(insert_statement, params=insert_item)

    new_session.commit()


def copy_all_tables(old_session, new_session):
    r"""
    Copy over all information from the v1 (old) database to the v2 (new) database.
    :param old_session: a connection to the v1 (old) database.
    :param new_session: a connection to the v2 (new) database.
    :return: None
    """
    copy_anisotropy_form(old_session, new_session)
    copy_db_user(old_session, new_session)
    copy_field(old_session, new_session)
    copy_geometry(old_session, new_session)
    copy_legacy_model_info(old_session, new_session)
    copy_material(old_session, new_session)
    copy_metadata(old_session, new_session)
    copy_model(old_session, new_session)
    copy_model_field(old_session, new_session)
    copy_model_material_association(old_session, new_session)
    copy_model_report_data(old_session, new_session)
    copy_model_run_data(old_session, new_session)
    copy_neb(old_session, new_session)
    copy_neb_calculation_type(old_session, new_session)
    copy_neb_model_split(old_session, new_session)
    copy_neb_report_data(old_session, new_session)
    copy_neb_run_data(old_session, new_session)
    copy_physical_constant(old_session, new_session)
    copy_project(old_session, new_session)
    copy_random_field(old_session, new_session)
    copy_running_status(old_session, new_session)
    copy_size_convention(old_session, new_session)
    copy_software(old_session, new_session)
    copy_uniform_field(old_session, new_session)
    copy_unit(old_session, new_session)


def command_line_parser():
    parser = ArgumentParser()

    parser.add_argument("old_db", help="old database name/file")
    parser.add_argument("old_db_type", choices=["postgres", "sqlite"], help="the old database db_type")
    parser.add_argument("--old-db-user", default=None, help="old database user")
    parser.add_argument("--old-db-host", default=None, help="old database host")
    parser.add_argument("new_db", help="new database name/file")
    parser.add_argument("new_db_type", choices=["postgres", "sqlite"], help="the new database db_type")
    parser.add_argument("--new-db-user", default=None, help="new database user")
    parser.add_argument("--new-db_host", default=None, help="new database host")

    return parser


def main():
    parser = command_line_parser()
    args = parser.parse_args()

    old_conn = get_session_from_args(args.old_db_type, db_version="v1",
        db_name=args.old_db, user=args.old_db_user, host=args.old_db_host,
        nullpool=True, autoflush=True, autocommit=False
    )

    new_conn = get_session_from_args(args.new_db_type, db_version="v2",
        db_name=args.new_db, user=args.new_db_user, host=args.new_db_host,
        nullpool=True, autoflush=True, autocommit=False
    )

    drop_all_constraints(new_conn)
    copy_all_tables(old_conn, new_conn)
    enable_all_constraints(new_conn)


if __name__ == "__main__":
    main()
