#
# Created on Aug, 2018
#
# file: schema.py
# author: Nagy, Lesleis
#

import os

from datetime import datetime
from enum import Enum

import uuid

from sqlalchemy import Column, Integer, Float, String, DateTime, Boolean, Numeric
from sqlalchemy import ForeignKey
from sqlalchemy import UniqueConstraint, Index
from sqlalchemy import event
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import column_property
from sqlalchemy.orm import relationship

from m4db.utilities.password import password_hash

from m4db import GLOBAL

now = datetime.now

Base = declarative_base()


def new_unique_id():
    r"""
    Generates a universal unique identifier.

    :return: a global unique id.
    """
    return str(uuid.uuid4())


def new_random_pass():
    r"""
    Generates some random password.

    :return: a random (difficult to guess) password.
    """
    return password_hash(new_unique_id())


class SizeConventionEnum(str, Enum):
    r"""
    A class to hold allowed size conventions.
    """
    esvd = "ESVD"
    ecvl = "ECVL"


class AnisotropyFormEnum(str, Enum):
    r"""
    A class to hold acceptable size conventions.
    """
    cubic = "cubic"  # cubic anisotropy.
    uniaxial = "uniaxial"  # uniaxial anisotropy.


class GeometryEnum(str, Enum):
    r"""
    Class to enumerate strings representing supported geometries.
    """
    ellipsoid = "ellipsoid"
    truncated_octahedron = "truncated_octahedron"


class RunningStatusEnum(str, Enum):
    r"""
    Class to hold default running statuses.
    """
    not_run = "not-run"
    re_run = "re-run"
    running = "running"
    finished = "finished"
    crashed = "crashed"
    scheduled = "scheduled"


class DBUser(Base):
    """
    Holds information about whom a model belongs to. Note: this is not ownership in the sense of permissions, but it
    gives us a useful dimension to differentiate different models.

    :param id: a unique internal id for the object.
    :param user_name: a unique name for the user.
    :param first_name: the user's first name.
    :param initials: the user's middle initial.
    :param surname: the user's surname.
    :param email: the user's email.
    :param telephone: the user's telephone number.
    :param last_modified: the date/time at which this object/record was modified.
    :param created: the creation date/time of this object/record.
    """

    __tablename__ = 'db_user'

    id = Column(Integer, primary_key=True, doc="a unique internal id for the object.")
    user_name = Column(String, nullable=False, doc="a unique name for the user.")
    first_name = Column(String, nullable=False, doc="the user's first name.")
    initials = Column(String, nullable=True, doc="the user's middle initial.")
    surname = Column(String, nullable=False, doc="the user's surname.")
    email = Column(String, nullable=False, doc="the user's email")
    telephone = Column(String, nullable=True, doc="the user's telephone number.")
    last_modified = Column(DateTime, default=now, onupdate=now, nullable=False, doc="the date/time at which this object/record was modified.")
    created = Column(DateTime, default=now, nullable=False, doc="the creation date/time of this object/record.")

    __table_args__ = (
        UniqueConstraint('first_name', 'surname', 'email', 'telephone', name='uniq_db_user_01'),
        UniqueConstraint('user_name', name='uniq_db_user_02'),
    )

    def as_dict(self):
        r"""
        Get a python dictionary representation of this object.

        :return: A dictionary representing this object.
        """

        return {
            "id": self.id,
            "user_name": self.user_name,
            "password": self.password,
            "first_name": self.first_name,
            "initials": self.initials,
            "surname": self.surname,
            "email": self.email,
            "telephone": self.telephone,
            "last_modified": self.last_modified.strftime(GLOBAL.DATE_TIME_FORMAT),
            "created": self.created.strftime(GLOBAL.DATE_TIME_FORMAT)
        }


class Software(Base):
    """
    This object holds information about the software used to run models.

    :param id: a unique internal id for a software object.
    :param name: the name of the software object.
    :param version: the version of the software object.
    :param executable: the path to the executable of the software object.
    :param description: the description of the software object.
    :param url: the url of the software object.
    :param citation: a citation for the software object.
    :param last_modified: the date/time at which this object/record was modified.
    :param created: the creation date/time of this object/record.
    """

    __tablename__ = 'software'

    id = Column(Integer, primary_key=True, doc="a unique internal id for a software object.")
    name = Column(String, nullable=False, doc="the name of the software object.")
    version = Column(String, nullable=False, doc="the version of the software object.")
    executable = Column(String, nullable=True, doc="the path to the executable of the software object.")
    description = Column(String, nullable=True, doc="the description of the software object.")
    url = Column(String, nullable=True, doc="the url of the software object.")
    citation = Column(String, nullable=True, doc="a citation for the software object.")
    last_modified = Column(DateTime, default=now, onupdate=now, nullable=False, doc="the date/time at which this object/record was modified.")
    created = Column(DateTime, default=now, nullable=False, doc="the creation date/time of this object/record.")

    __table_args__ = (
        UniqueConstraint('name', 'version', name='uniq_software_01'),
    )

    def as_dict(self):
        r"""
        Get a python dictionary representation of this object.

        :return: a dictionary representing this object.
        """

        return {
            "id": self.id,
            "name": self.name,
            "version": self.version,
            "executable": self.executable,
            "description": self.description,
            "url": self.url,
            "citation": self.citation,
            "last_modified": self.last_modified.strftime(GLOBAL.DATE_TIME_FORMAT),
            "created": self.created.strftime(GLOBAL.DATE_TIME_FORMAT)
        }


class SizeConvention(Base):
    """
    Holds a size convention. Size conventions are useful since we use them as a short-hand to refer to volumetric sizes.
    For example: what do we mean by "100nm grain"?, if we're using equivalent spherical volume diameter (ESVD)
    then the grain has a volume equivalent to a sphere of diameter 100nm.

    :param id: a unique internal id for the object.
    :param symbol: the symbol associated with the size convention.
    :param description: a description for the size convention.
    :param last_modified: the date/time at which this object/record was modified.
    :param created: the creation date/time of this object/record.
    """
    __tablename__ = 'size_convention'

    id = Column(Integer, primary_key=True, doc="a unique internal id for the object")
    symbol = Column(String, nullable=False, doc="the symbol associated with the size convention")
    description = Column(String, nullable=False, doc="a description for the size convention")
    last_modified = Column(DateTime, default=now, onupdate=now, nullable=False, doc="the date/time at which this object/record was modified")
    created = Column(DateTime, default=now, nullable=False, doc="the creation date/time of this object/record")

    __table_args = (
        UniqueConstraint('symbol', name='uniq_size_convention_01'),
    )

    def as_dict(self):
        r"""
        Get a python dictionary representation of this object.

        :returns: a dictionary representing this object.
        """
        return {
            "id": self.id,
            "symbol": self.symbol,
            "description": self.description,
            "last_modified": self.last_modified.strftime(GLOBAL.DATE_TIME_FORMAT),
            "created": self.created.strftime(GLOBAL.DATE_TIME_FORMAT)
        }


class AnisotropyForm(Base):
    """
    Holds different anisotropy forms for example 'cubic' and 'uniaxial'.

    :param id: a unique internal id for the object.
    :param name: anisotropy form's name.
    :param description: a description for the anisotropy form convention.
    :param last_modified: the date/time at which this object/record was modified.
    :param created: the creation date/time of this object/record.
    """

    __tablename__ = 'anisotropy_form'

    id = Column(Integer, primary_key=True, doc="a unique internal id for the object.")
    name = Column(String, nullable=False, doc="anisotropy form's name.")
    description = Column(String, nullable=False, doc="a description for the anisotropy form convention.")
    last_modified = Column(DateTime, default=now, onupdate=now, nullable=False, doc="the date/time at which this object/record was modified.")
    created = Column(DateTime, default=now, nullable=False, doc="the creation date/time of this object/record.")

    __table_args__ = (
        UniqueConstraint('name', name='uniq_anisotropy_form_01'),
    )

    def as_dict(self):
        r"""
        Get a python dictionary representation of this object.

        :returns: a dictionary representing this object.
        """

        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "last_modified": self.last_modified.strftime(GLOBAL.DATE_TIME_FORMAT),
            "created": self.created.strftime(GLOBAL.DATE_TIME_FORMAT)
        }


class Geometry(Base):
    """
    The parent class/entity of all geometries. This object should *NOT* be used on its own since it is abstract -
    please use one of the derived types: Ellipsoid, TruncatedOctahedron

    :param id: a unique internal id for the object.
    :param unique_id: unique identifier for the geometry that may be used outside the database.
    :param type: the type of geometry (see below).
    :param nelements: the number of elements that comprise the geometry.
    :param nvertices: the number of vertices that comprise the geometry.
    :param nsubmeshes: the number of submeshes that comprise the geometry.
    :param computed_volume: the total calculated volume of the geometry.
    :param computed_element_length_average: the calculated average element edge length of the geometry.
    :param computed_element_length_standard_deviation: the calculated standard deviation in element edge lengths.
    :param computed_element_length_minimum: the calculated minimum edge length.
    :param computed_element_length_maximum: the calculated maximum edge length.
    :param has_patran: flag indicates that a patran file is available for the geometry.
    :param has_exodus: flag indicates that an exodus file is available for the geometry.
    :param has_mesh_gen_script: flag indicates that a script to generate the mesh is available for the geometry.
    :param has_mesh_gen_output: flag indicates that output from meshing program, in addition to the mesh, is available.
    :param last_modified: the date/time at which this object/record was modified.
    :param created: the creation date/time of this object/record.
    :param software: the software object used to create this geometry.
    """

    # The software id used to generate the geometry
    __tablename__ = 'geometry'

    id = Column(Integer, primary_key=True, nullable=False, doc="a unique internal id for the object.")
    unique_id = Column(String, default=new_unique_id, nullable=False, doc="unique identifier for the geometry that may be used outside the database.")
    type = Column(String, nullable=False, doc="the type of geometry (see below).")
    nelements = Column(Integer, nullable=True, doc="the number of elements that comprise the geometry.")
    nvertices = Column(Integer, nullable=True, doc="the number of vertices that comprise the geometry.")
    nsubmeshes = Column(Integer, default=1, nullable=False, doc="the number of submeshes that comprise the geometry.")
    computed_volume = Column(Float, nullable=True, doc="the total calculated volume of the geometry.")
    computed_element_length_average = Column(Float, nullable=True, doc="the calculated average element edge length of the geometry.")
    computed_element_length_standard_deviation = Column(Float, nullable=True, doc="the calculated standard deviation in element edge lengths.")
    computed_element_length_minimum = Column(Float, nullable=True, doc="the calculated minimum edge length.")
    computed_element_length_maximum = Column(Float, nullable=True, doc="the calculated maximum edge length.")
    has_patran = Column(Boolean, default=False, nullable=False, doc="flag indicates that a patran file is available for the geometry.")
    has_exodus = Column(Boolean, default=False, nullable=False, doc="flag indicates that an exodus file is available for the geometry.")
    has_mesh_gen_script = Column(Boolean, default=False, nullable=False, doc="flag indicates that a script to generate the mesh is available for the geometry.")
    has_mesh_gen_output = Column(Boolean, default=False, nullable=False, doc="flag indicates that output from meshing program, in addition to the mesh, is available.")
    last_modified = Column(DateTime, default=now, onupdate=now, nullable=False, doc="the date/time at which this object/record was modified.")
    created = Column(DateTime, default=now, nullable=False, doc="the creation date/time of this object/record.")

    # The software id used to generate the geometry
    software_id = Column(Integer, ForeignKey('software.id'), nullable=True, doc="")
    software = relationship('Software')

    __mapper_args__ = {
        'polymorphic_identity': 'geometry',
        'polymorphic_on': type
    }

    __table_args__ = (
        UniqueConstraint('unique_id', name='uniq_geometry_01'),
    )

    def _as_dict(self):
        return {
            'id': self.id,
            'unique_id': self.unique_id,
            'type': self.type,
            'nelements': self.nelements,
            'nvertices': self.nvertices,
            'nsubmeshes': self.nsubmeshes,
            'volume_total': self.volume_total,
            'has_patran': self.has_patran,
            'has_exodus': self.has_exodus,
            'has_mesh_gen_script': self.has_mesh_gen_script,
            'has_mesh_gen_output': self.has_mesh_gen_output,
            'las_modified': self.last_modified,
            'created': self.created
        }


class Ellipsoid(Geometry):
    r"""
    An ellipsoid geometry that derives its structure from an existing Geometry object.

    :param id: a unique internal id for the object.
    :param size: the size of the geometry upon creation (in micron).
    :param element_size: element size at which this geometry was meshed (i.e. the element size specified to the mesher).
    :param prolateness: a measurement of the prolateness of the ellipsoid (x-length / y-length)
    :param oblateness: a measurement of the oblateness of the ellipsoid (y-length / z-length)
    :param size_convention: the size convention of this geometry's size.
    """
    __tablename__ = "ellipsoid"

    id = Column(Integer, ForeignKey('geometry.id'), primary_key=True, nullable=False, doc="a unique internal id for the object.")
    size = Column(Numeric(10, 5), nullable=True, doc="the size of the geometry upon creation (in micron).")
    element_size = Column(Numeric(10, 5), nullable=True, doc="element size at which this geometry was meshed (i.e. the element size specified to the mesher).")
    prolateness = Column(Numeric(10, 5), doc="a measurement of the prolateness of the ellipsoid (x-length / y-length)")
    oblateness = Column(Numeric(10, 5), doc="a measurement of the oblateness of the ellipsoid (y-length / z-length)")
    size_convention_id = Column(Integer, ForeignKey('size_convention.id'), nullable=True, doc="the convention in which the size is named.")
    size_convention = relationship('SizeConvention')

    __mapper_args__ = {
        'polymorphic_identity': 'ellipsoid',
    }

    __table_args__ = (UniqueConstraint('size',
                                       'element_size',
                                       'size_convention_id',
                                       'prolateness',
                                       'oblateness',
                                       name='uniq_ellipsoid_01'),)

    def as_dict(self):
        output = self._as_dict()
        output['size'] = self.size
        output['element_size'] = self.element_size
        output['size_convention'] = self.size_convention.symbol
        output["prolateness"] = self.prolateness
        output["oblateness"] = self.oblateness

        return output


class TruncatedOctahedron(Geometry):
    r"""
    A truncated octahedral geometry that derives its structure from an existing Geometry object.

    :param id: a unique internal id for the object.
    :param size: the size of the geometry upon creation (in micron).
    :param element_size: element size at which this geometry was meshed (i.e. the element size specified to the mesher).
    :param truncation_factor: the amount that the corners of the octahedron are sliced off (between 0.5 to 1.0)
    :param aspect_ratio: the aspect ratio of the truncated octahedron (x-axis to y/z-axis)
    :param size_convention: the size convention of this geometry's size.
    """
    __tablename__ = "truncated_octahedron"

    id = Column(Integer, ForeignKey('geometry.id'), primary_key=True, nullable=False, doc="a unique internal id for the object.")
    size = Column(Numeric(10, 5), nullable=True, doc="the size of the geometry upon creation (in micron).")
    element_size = Column(Numeric(10, 5), nullable=True, doc="element size at which this geometry was meshed (i.e. the element size specified to the mesher).")
    truncation_factor = Column(Numeric(10, 5), doc="the amount that the corners of the octahedron are sliced off (between 0.5 to 1.0)")
    aspect_ratio = Column( Numeric(10, 5), doc="the aspect ratio of the truncated octahedron (x-axis to y/z-axis)")
    size_convention_id = Column(Integer, ForeignKey('size_convention.id'), nullable=True, doc="the convention in which the size is named.")
    size_convention = relationship('SizeConvention')

    __mapper_args__ = {
        'polymorphic_identity': 'truncated_octahedron'
    }

    __table_args__ = (
        UniqueConstraint('size',
                         'element_size',
                         'size_convention_id',
                         'truncation_factor',
                         'aspect_ratio',
                         name='uniq_truncated_octahedron_01'),
    )

    def as_dict(self):
        output = self._as_dict()
        output['size'] = self.size
        output['element_size'] = self.element_size
        output['size_convention'] = self.size_convention.symbol
        output["truncation_factor"] = self.truncation_factor
        output["aspect_ratio"] = self.aspect_ratio

        return output


class Material(Base):
    """
    Holds material data that is important for micromagnetic calculations. The
    natural key for a material is name/temperature pair (hence the reason why
    temperature is an integer). Note: temperature is *ALWAYS* assumed to be in
    degrees Celsius.

    :param id: a unique internal id for the object
    :param submesh_id: the sub-mesh id number to which this material belongs.
    :param name: the name of the material (e.g. magnetite).
    :param temperature: the temperature at which material constants are calculated
    :param k1: the first magneto-crystalline anisotropy constant
    :param k2: the second magneto-crystalline anisotropy constant
    :param k3: the third magneto-crystalline anisotropy constant
    :param k4: the fourth magneto-crystalline anisotropy constant
    :param k5: the fifth magneto-crystalline anisotropy constant
    :param k6: the sixth magneto-crystalline anisotropy constant
    :param k7: the seventh magneto-crystalline anisotropy constant
    :param k8: the eighth magneto-crystalline anisotropy constant
    :param k9: the ninth magneto-crystalline anisotropy constant
    :param k10: the tenth magneto-crystalline anisotropy constant
    :param aex: the exchange constant
    :param ms: the saturation magnetization constant
    :param dir_x: the x direction of the orientation of the anisotropy axes.
    :param dir_y: the y direction of the orientation of the anisotropy axes.
    :param dir_z: the z direction of the orientation of the anisotropy axes.
    :param alpha: the alpha rotation angle for anisotropy axes.
    :param theta: the theta rotation angle for anisotropy axes.
    :param phi: the phi rotation angle of the anisotopy axes.
    :param last_modified: the data/time at which the object/record was modified
    :param created: the creation date/time of this object/record
    """
    __tablename__ = 'material'

    id = Column(Integer, primary_key=True, nullable=False)
    submesh_id = Column(Integer, default=1, nullable=False)
    name = Column(String, nullable=False)
    temperature = Column(Numeric(8,3), nullable=False)
    k1 = Column(Float, nullable=True)
    k2 = Column(Float, nullable=True)
    k3 = Column(Float, nullable=True)
    k4 = Column(Float, nullable=True)
    k5 = Column(Float, nullable=True)
    k6 = Column(Float, nullable=True)
    k7 = Column(Float, nullable=True)
    k8 = Column(Float, nullable=True)
    k9 = Column(Float, nullable=True)
    k10 = Column(Float, nullable=True)
    aex = Column(Float, nullable=True)
    ms = Column(Float, nullable=True)
    dir_x = Column(Float, nullable=True, default=1.0)
    dir_y = Column(Float, nullable=True, default=0.0)
    dir_z = Column(Float, nullable=True, default=0.0)
    alpha = Column(Float, nullable=True, default=0.0)
    theta = Column(Float, nullable=True, default=0.0)
    phi = Column(Float, nullable=True, default=0.0)
    last_modified = Column(DateTime, default=now, onupdate=now, nullable=False)
    created = Column(DateTime, default=now, nullable=False)

    anisotropy_form_id = Column(Integer, ForeignKey('anisotropy_form.id'), nullable=False)
    anisotropy_form = relationship('AnisotropyForm', uselist=False)

    model_id = Column(Integer, ForeignKey("model.id"))

    def as_dict(self):
        r"""
        Get a python dictionary representation of this object.

        :returns: a dictionary representing this object.
        """

        return {
            "id": self.id,
            "name": self.name,
            "temperature": str(self.temperature),
            "k1": self.k1,
            "aex": self.aex,
            "ms": self.ms,
            "kd": self.kd,
            "lambda_ex": self.lambda_ex,
            "q_hardness": self.q_hardness,
            "axis_theta": self.axis_theta,
            "axis_phi": self.axis_phi,
            "last_modified": self.last_modified.strftime(GLOBAL.DATE_TIME_FORMAT),
            "created": self.created.strftime(GLOBAL.DATE_TIME_FORMAT),
            "anisotropy_form": self.anisotropy_form.as_dict()
        }


class UniformAppliedField(Base):
    r"""
    A class to hold applied field values (note that field magnitude is always in  micro Tesla).

    :param id: a unique internal id for the object.
    :param dir_x: the x-direction in which the field is applied.
    :param dir_y: the y-direction in which the field is applied.
    :param dir_z: the z-direction in which the field is applied.
    :param magnitude: the magnitude of the applied field in micro Tesla.
    """
    __tablename__ = 'uniform_applied_field'

    id = Column(Integer, primary_key=True, nullable=False)
    dir_x = Column(Float, nullable=False)
    dir_y = Column(Float, nullable=False)
    dir_z = Column(Float, nullable=False)
    magnitude = Column(Float, nullable=False)  # Magnitude is always in micro Tesla
    last_modified = Column(DateTime, default=now, onupdate=now, nullable=False)
    created = Column(DateTime, default=now, nullable=False)


class InitialMagnetization(Base):
    """
    The parent class/entity of all magnetizations. This field object/entity should
    *NOT* be used on its own since it is abstract - please use one of the
    derived types: 1) UniformInitialMagnetization - a uniform initial magnetization field;
    2) RandomInitialMagnetization - encapsulates a random field; 3) ModelInitalMagnetization.

    :param id: a unique internal id for the object
    :param type: a string that refers to the child db_type (see above)
    :param last_modified: the date/time at which this object/record was modified
    :param created: the creation date/time of this object/record
    """

    __tablename__ = 'initial_magnetization'

    id = Column(Integer, primary_key=True, nullable=False)
    type = Column(String, nullable=False)
    last_modified = Column(DateTime, default=now, onupdate=now, nullable=False)
    created = Column(DateTime, default=now, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'initial_magnetization',
        'polymorphic_on': type
    }


class ModelInitialMagnetization(InitialMagnetization):
    """
    A model magnetization is a field that that derives its structure from an existing model.

    :param last_modified: the date/time at which this object/record was modified.
    :param created: the creation date/time of this object/record.
    :param model: the model to which this field belongs.
    """

    __tablename__ = 'model_initial_magnetization'

    id = Column(Integer, ForeignKey('initial_magnetization.id'), primary_key=True, nullable=False)
    last_modified = column_property(Column(DateTime, default=now, onupdate=now, nullable=False),
                                    InitialMagnetization.last_modified)
    created = column_property(Column(DateTime, default=now, nullable=False), InitialMagnetization.created)

    model_id = Column(Integer, ForeignKey('model.id'), nullable=False)
    model = relationship('Model')

    __mapper_args__ = {
        'polymorphic_identity': 'model_initial_magnetization',
    }

    def as_dict(self):
        r"""
        Get a python dictionary representation of this object.

        :return: a dictionary representing this object.
        """

        return {
            "id": self.id,
            "db_type": self.type,
            "last_modified": self.last_modified.strftime(GLOBAL.DATE_TIME_FORMAT),
            "created": self.created.strftime(GLOBAL.DATE_TIME_FORMAT),
            "model_unique_id": self.model.unique_id
        }


class RandomInitialMagnetization(InitialMagnetization):
    """
    A random field is really just a placeholder record to denote a random initial magnetization.

    :param last_modified: the date/time at which this object/record was modified.
    :param created: the creation date/time of this object/record.
    """

    __tablename__ = 'random_initial_magnetization'

    id = Column(Integer, ForeignKey('initial_magnetization.id'), primary_key=True, nullable=False)
    last_modified = column_property(Column(DateTime, default=now, onupdate=now, nullable=False),
                                    InitialMagnetization.last_modified)
    created = column_property(Column(DateTime, default=now, nullable=False), InitialMagnetization.created)

    __mapper_args__ = {
        'polymorphic_identity': 'random_initial_magnetization',
    }

    def as_dict(self):
        r"""
        Get a python dictionary representation of this object.

        :returns: a dictionary representing this object.
        """
        return {
            "id": self.id,
            "db_type": self.type,
            "last_modified": self.last_modified.strftime(GLOBAL.DATE_TIME_FORMAT),
            "created": self.created.strftime(GLOBAL.DATE_TIME_FORMAT),
            "seed": self.seed
        }


class UniformInitialMagnetization(InitialMagnetization):
    """
    A uniform initial magnetization in a given direction with some defined magnitude (in micro Tesla).

    :param id: a unique internal id for the object.
    :param dir_x: the x component of the field direction.
    :param dir_y: the y component of the field direction.
    :param dir_z: the z component of the field direction.
    :param magnitude: the magnitude of the field (in micro Tesla).
    :param last_modified: the date/time at which this object/record was modified.
    :param created: the creation date/time of this object/record.
    """

    __tablename__ = 'uniform_initial_magnetization'

    id = Column(Integer, ForeignKey('initial_magnetization.id'), primary_key=True, nullable=False)
    dir_x = Column(Float, nullable=False)
    dir_y = Column(Float, nullable=False)
    dir_z = Column(Float, nullable=False)
    magnitude = Column(Float, nullable=False)  # Magnitude is always in micro Tesla
    last_modified = column_property(Column(DateTime, default=now, onupdate=now, nullable=False), InitialMagnetization.last_modified)
    created = column_property(Column(DateTime, default=now, nullable=False), InitialMagnetization.created)

    __mapper_args__ = {
        'polymorphic_identity': 'uniform_initial_magnetization',
    }

    def as_dict(self):
        r"""
        Get a python dictionary representation of this object.

        :returns: a dictionary representing this object.
        """

        return {
            "id": self.id,
            "db_type": self.type,
            "last_modified": self.last_modified.strftime(GLOBAL.DATE_TIME_FORMAT),
            "created": self.created.strftime(GLOBAL.DATE_TIME_FORMAT),
            "theta": self.theta,
            "phi": self.phi,
            "dir_x": self.dir_x,
            "dir_y": self.dir_y,
            "dir_z": self.dir_z,
            "magnitude": self.magnitude
        }


class RunningStatus(Base):
    r"""
    The running status of a model. Models can be in one of the following states: 1) not-run, 2) re-run, 3) running
    and 4) finished.

    :param id: the primary key id of a RunningStatus object.
    :param name: the name of the running status.
    :param description: a description of the running status.
    :param last_modified: the last modified time of the RunningStatus object.
    :param created: the creation time of the RunningStatus object.
    """
    __tablename__ = 'running_status'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    last_modified = Column(DateTime, default=now, onupdate=now, nullable=False)
    created = Column(DateTime, default=now, nullable=False)

    __table_args__ = (
        UniqueConstraint('name', name='uniq_running_status_01'),
    )

    def as_dict(self):
        r"""
        Get a python dictionary representation of this object.

        :returns: a dictionary representing this object.

        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "last_modified": self.last_modified.strftime(GLOBAL.DATE_TIME_FORMAT),
            "created": self.created.strftime(GLOBAL.DATE_TIME_FORMAT)
        }


class ModelRunData(Base):
    r"""
    Important metadata regarding a model.

    :param id: a unique internal id for the object.
    :param has_script: a flag to indicate whether the model has a script (which generated the model) associated with it.
    :param has_stdout: a flag to indicate whether the model has a standard output file associated with it.
    :param has_stderr: a flag to indicate whether the model has a standard error file associated with it.
    :param has_energy_log: a flag to indicate whether the model has an energy log associated with it.
    :param has_tecplot: a flag to indicate whether the model has a tecplot representation associated with it.
    :param has_json: a flag to indicate whether the model has a json representation associated with it.
    :param has_dat: a flag to indicate whether the model has a dat representation associated with it.
    :param has_helicity_dat: a flag to indicate whether the model has a dat representation of its helicity scalar field associated with it.
    :param has_vorticity_dat: a flag to indicate whether the model has a dat representation of its vorticity vector field associated with it.
    :param has_adm_dat: a flag to indicate whether the model has a dat representation of its adm scalar field associated with it.
    :param last_modified: the date/time at which this object/record was modified.
    :param created: the creation date/time of this object/record.
    """

    __tablename__ = 'model_run_data'

    id = Column(Integer, primary_key=True, nullable=False)
    has_script = Column(Boolean, default=False, nullable=False)
    has_stdout = Column(Boolean, default=False, nullable=False)
    has_stderr = Column(Boolean, default=False, nullable=False)
    has_energy_log = Column(Boolean, default=False, nullable=False)
    has_tecplot = Column(Boolean, default=False, nullable=False)
    has_json = Column(Boolean, default=False, nullable=False)
    has_dat = Column(Boolean, default=False, nullable=False)
    has_helicity_dat = Column(Boolean, default=False, nullable=False)
    has_vorticity_dat = Column(Boolean, default=False, nullable=False)
    has_adm_dat = Column(Boolean, default=False, nullable=False)
    last_modified = Column(DateTime, default=now, onupdate=now, nullable=False)
    created = Column(DateTime, default=now, nullable=False)

    def as_dict(self):
        r"""
        Get a python dictionary representation of this object.

        :return: a dictionary representing this object.
        """

        return {
            "id": self.id,
            "has_script": self.has_script,
            "has_stdout": self.has_stdout,
            "has_stderr": self.has_stderr,
            "has_energy_log": self.has_energy_log,
            "has_tecplot": self.has_tecplot,
            "has_json": self.has_json,
            "has_dat": self.has_dat,
            "has_helicity_dat": self.has_helicity_dat,
            "has_vorticity_dat": self.has_vorticity_dat,
            "has_adm_dat": self.has_adm_dat,
            "last_modified": self.last_modified.strftime(GLOBAL.DATE_TIME_FORMAT),
            "created": self.created.strftime(GLOBAL.DATE_TIME_FORMAT)
        }


class ModelReportData(Base):
    r"""
    Some metadata to track whether some data items used for generating a Model
    report have been created.

    :param id: the primary key.
    :param has_xy_thumb_png: a boolean set to true if there is a thumbnail image of the model with the x-y axis corresponding to the user's screen/monitor.
    :param has_yz_thumb_png: a boolean set to true if there is a thumbnail image of the model with the y-z axis corresponding to the user's screen/monitor.
    :param has_xz_thumb_png: a boolean set to true if there is a thumbnail image of the model with the x-z axis corresponding to the user's screen/monitor.
    :param has_xy_png: a boolean set to true if there is an image of the model with the x-y axis corresponding to the user's screen/monitor.
    :param has_yz_png: a boolean set to true if there is an image of the model with the y-z axis corresponding to the user's screen/monitor.
    :param has_xz_png: a boolean set to true if there is an image of the model with the x-z axis corresponding to the user's screen/monitor.
    :param last_modified: the date/time at which this object/record was modified.
    :param created: the creation date/time of this object/record.
    """

    __tablename__ = 'model_report_data'

    id = Column(Integer, primary_key=True, nullable=False)
    has_xy_thumb_png = Column(Boolean, default=False, nullable=False)
    has_yz_thumb_png = Column(Boolean, default=False, nullable=False)
    has_xz_thumb_png = Column(Boolean, default=False, nullable=False)
    has_xy_png = Column(Boolean, default=False, nullable=False)
    has_yz_png = Column(Boolean, default=False, nullable=False)
    has_xz_png = Column(Boolean, default=False, nullable=False)

    def as_dict(self):
        r"""
        Get a python dictionary representation of this object.

        :return: dictionary representing this object.
        """

        return {
            "id": self.id,
            "has_xy_thumb_png": self.has_xy_thumb_png,
            "has_yz_thumb_png": self.has_yz_thumb_png,
            "has_xz_thumb_png": self.has_xz_thumb_png,
            "has_xy_png": self.has_xy_png,
            "has_yz_png": self.has_yz_png,
            "has_xz_png": self.has_xz_png
        }


class Project(Base):
    r"""
    Some metadata regarding a project.

    :param id: the primary key.
    :param name: the name of the project.
    :param description: a description of the project.
    :param last_modified: the date/time at which this object/record was modified.
    :param created: the creation date/time of this object/record.
    """

    __tablename__ = 'project'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    last_modified = Column(DateTime, default=now, onupdate=now, nullable=False)
    created = Column(DateTime, default=now, nullable=False)

    UniqueConstraint('project_name', name='uniq_project_01')

    def as_dict(self):
        r"""
        Get a python dictionary representation of this object.

        :returns: a dictionary representing this object.
        """

        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "last_modified": self.last_modified.strftime(GLOBAL.DATE_TIME_FORMAT),
            "created": self.created.strftime(GLOBAL.DATE_TIME_FORMAT)
        }


class Metadata(Base):
    r"""
    Metadata associated with a model. Each model has a user that created it,
    a project to which it belongs and a piece of software that generated it.

    :param id: the primary key.
    :param project: the Project object associated with this piece of metadata.
    :param db_user: the DBUser object associated with this piece of metadata.
    :param software: the Software object associated with this piece of metadata.
    :param created: the time when the object was created.
    :param last_modified: the time when the object was last modified.
    """

    __tablename__ = 'metadata'

    id = Column(Integer, primary_key=True, nullable=False)
    last_modified = Column(DateTime, default=now, onupdate=now, nullable=False)
    created = Column(DateTime, default=now, nullable=False)

    project_id = Column(Integer, ForeignKey('project.id'), nullable=False)
    project = relationship('Project')

    db_user_id = Column(Integer, ForeignKey('db_user.id'), nullable=False)
    db_user = relationship('DBUser')

    software_id = Column(Integer, ForeignKey('software.id'), nullable=True)
    software = relationship('Software')

    def as_dict(self):
        r"""
        Get a python dictionary representation of this object.

        :returns: a dictionary representing this object.
        """

        return {
            "id": self.id,
            "last_modified": self.last_modified.strftime(GLOBAL.DATE_TIME_FORMAT),
            "created": self.created.strftime(GLOBAL.DATE_TIME_FORMAT),
            "project_name": self.project.name,
            "db_user_user_name": self.db_user.user_name,
            "software_name": self.software.name if self.software is not None else None,
            "software_version": self.software.version if self.software is not None else None
        }


class LegacyModelInfo(Base):
    r"""
    Some models have some legacy information associated with them, these are
    stored in this object.

    :param id: the primary key.
    :param index: the index referring to the the model index from the legacy data structure.
    :param created: the time when the object was created.
    :param last_modified: the time when the object was last modified.
    """

    __tablename__ = 'legacy_model_info'

    id = Column(Integer, primary_key=True, nullable=False)
    legacy_model_id = Column(Integer, nullable=False)
    last_modified = Column(DateTime, default=now, onupdate=now, nullable=False)
    created = Column(DateTime, default=now, nullable=False)

    def as_dict(self):
        r"""
        Get a python dictionary representation of this object.

        :return: a dictionary representing this object.
        """

        return {
            "id": self.id,
            "legacy_model_id": self.legacy_model_id,
            "last_modified": self.last_modified.strftime(GLOBAL.DATE_TIME_FORMAT),
            "created": self.created.strftime(GLOBAL.DATE_TIME_FORMAT)
        }


class Model(Base):
    r"""
    Class to hold model LEM data.

    :param id: a unique internal id.
    :param unique_id: a unique id that is used to identify a model.
    :param mx_tot: the x direction of the total magnetization field (this is populated on a successful run).
    :param my_tot: the y direction of the total magnetization field (this is populated on a successful run).
    :param mz_tot: the y direction of the total magnetization field (this is populated on a successful run).
    :param vx_tot: the x direction of the total vorticity field (this field is populated on a successful run).
    :param vy_tot: the y direction of the total vorticity field (this field is populated on a successful run).
    :param vz_tot: the z direction of the total vorticity field (this field is populated on a successful run).
    :param h_tot: the total helicity (this field is populated on a successful run).
    :param rh_tot: the total relative helicity (this field is populated on a successful run).
    :param adm_tot: the total anisotropy direction of moments metric (this field is populated on a successful run).
    :param e_typical: the typical system energy (this field is populated on a successful run).
    :param e_anis: the anisotropy energy (this field is populated on a successful run).
    :param e_ext: the external field energy (this field is populated on a successful run).
    :param e_demag: the demagnetizing energy (this field is populated on a successful run).
    :param e_exch1: the exchange energy, calculated using method 1 (this field is populated on a successful run).
    :param e_exch2: the exchange energy, calculated using method 2 (this field is populated on a successful run).
    :param e_exch3: the exchange energy, calculated using method 3 (this field is populated on a successful run).
    :param e_exch4: the exchange energy, calculated using method 4 (this field is populated on a successful run).
    :param e_tot: the total energy (this field is populated on a successful run).
    :param max_energy_evaluations: the maximum number of energy evaluation steps.
    :param created: the time when the object was created.
    :param last_modified: the time when the object was last modified.
    :param geometry: the object reference to the geometry that belongs to this model.
    :param materials: the material objects references that belong to this model.
    :param initial_magnetization: the object reference to the magnetization that belongs to this model.
    :param applied_field: the object reference to the applied field of this model.
    :param running_status:  the object reference to the running status of this model.
    :param model_run_data: the object reference to the run data of this model.
    :param model_report_data: the object reference to the report data of this model.
    :param mdata: the object reference to the metadata of this model.
    :param legacy_model_info: the object reference to the legacy model info of this model.
    :param nebs: a list of neb objects that this model is a part of.
    """

    __tablename__ = 'model'

    id = Column(Integer, primary_key=True, nullable=False)
    unique_id = Column(String, default=new_unique_id, nullable=False)
    mx_tot = Column(Float, nullable=True)
    my_tot = Column(Float, nullable=True)
    mz_tot = Column(Float, nullable=True)
    vx_tot = Column(Float, nullable=True)
    vy_tot = Column(Float, nullable=True)
    vz_tot = Column(Float, nullable=True)
    h_tot = Column(Float, nullable=True)
    rh_tot = Column(Float, nullable=True)
    adm_tot = Column(Float, nullable=True)
    e_typical = Column(Float, nullable=True)
    e_anis = Column(Float, nullable=True)
    e_ext = Column(Float, nullable=True)
    e_demag = Column(Float, nullable=True)
    e_exch1 = Column(Float, nullable=True)
    e_exch2 = Column(Float, nullable=True)
    e_exch3 = Column(Float, nullable=True)
    e_exch4 = Column(Float, nullable=True)
    e_tot = Column(Float, nullable=True)
    max_energy_evaluations = Column(Integer, default=10000, nullable=False)
    last_modified = Column(DateTime, default=now, onupdate=now, nullable=False)
    created = Column(DateTime, default=now, nullable=False)

    geometry_id = Column(Integer, ForeignKey('geometry.id'), nullable=False)
    geometry = relationship('Geometry', uselist=False)

    materials = relationship("Material")

    initial_magnetization_id = Column(Integer, ForeignKey('initial_magnetization.id'), nullable=False)
    initial_magnetization = relationship('InitialMagnetization', uselist=False, foreign_keys=[initial_magnetization_id])

    applied_field_id = Column(Integer, ForeignKey('uniform_applied_field.id'), nullable=True)
    applied_field = relationship('UniformAppliedField', uselist=False, foreign_keys=[applied_field_id])

    running_status_id = Column(Integer, ForeignKey('running_status.id'), nullable=False)
    running_status = relationship('RunningStatus', uselist=False)

    model_run_data_id = Column(Integer, ForeignKey('model_run_data.id'), nullable=False)
    model_run_data = relationship('ModelRunData', uselist=False)

    model_report_data_id = Column(Integer, ForeignKey('model_report_data.id'), nullable=False)
    model_report_data = relationship('ModelReportData', uselist=False)

    mdata_id = Column(Integer, ForeignKey('metadata.id'), nullable=False)
    mdata = relationship('Metadata', uselist=False)

    legacy_model_info_id = Column(Integer, ForeignKey('legacy_model_info.id'), nullable=True)
    legacy_model_info = relationship('LegacyModelInfo', uselist=False)

    nebs = relationship('NEBModelSplit', back_populates='model')

    __table_args__ = (
        UniqueConstraint('unique_id', name='uniq_model_01'),
    )

    def as_dict(self):
        r"""
        Get a python dictionary representation of this object.

        :returns: a dictionary representing this object.
        """

        return {
            "id": self.id,
            "unique_id": self.unique_id,
            "mx_tot": self.mx_tot,
            "my_tot": self.my_tot,
            "mz_tot": self.mz_tot,
            "vx_tot": self.vx_tot,
            "vy_tot": self.vy_tot,
            "vz_tot": self.vz_tot,
            "h_tot": self.h_tot,
            "hr_tot": self.rh_tot,
            "adm_tot": self.adm_tot,
            "e_typical": self.e_typical,
            "e_anis": self.e_anis,
            "e_ext": self.e_ext,
            "e_demag": self.e_demag,
            "e_exch1": self.e_exch1,
            "e_exch2": self.e_exch2,
            "e_exch3": self.e_exch3,
            "e_exch4": self.e_exch4,
            "e_tot": self.e_tot,
            "volume": self.volume,
            "max_energy_evaluations": self.max_energy_evaluations,
            "last_modified": self.last_modified.strftime(GLOBAL.DATE_TIME_FORMAT),
            "created": self.created.strftime(GLOBAL.DATE_TIME_FORMAT),
            "geometry": self.geometry.as_dict(),
            "materials": [mma.as_dict() for mma in self.materials],
            "start_magnetization": self.start_magnetization.as_dict(),
            "running_status": self.running_status.as_dict(),
            "model_run_data": self.model_run_data.as_dict(),
            "model_report_data": self.model_report_data.as_dict(),
            "mdata": self.mdata.as_dict(),
            "legacy_model_info": self.legacy_model_info.as_dict()if self.legacy_model_info is not None else None,
        }


class NEBCalculationType(Base):
    r"""
    The db_type of neb calculation used to calculate the data associated with an NEB. For example: neb - NEB calculation
    based on the Nudged Elastic Band (NEB); or fs_heuristic - NEB calculation based on Fabian & Shcherbakov
    (arXiv:1702.00070v1).

    :param id: the primary key.
    :param name: the name of the NEB calculation db_type, 1) 'neb', 2) 'fs_heuristic'.
    :param description: a description of the NEB calculation db_type.
    :param created: the time when the object was created.
    :param last_modified: the time when the object was last modified.
    """

    __tablename__ = 'neb_calculation_type'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    last_modified = Column(DateTime, default=now, onupdate=now, nullable=False)
    created = Column(DateTime, default=now, nullable=False)

    def as_dict(self):
        r"""
        Get a python dictionary representation of this object.

        :return: a dictionary representing this object.

        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "last_modified": self.last_modified.strftime(GLOBAL.DATE_TIME_FORMAT),
            "created": self.created.strftime(GLOBAL.DATE_TIME_FORMAT)
        }


class NEBRunData(Base):
    r"""
    Stores run data, i.e. flags regarding what is produced when NEBs are run.

    :param id: the primary key.
    :param has_script: boolean flag indicating whether an NEB script is present.
    :param has_stdout: boolean flag indicating whether a standard output file is present.
    :param has_stderr: boolean flag indicating whether a standard error output file is present.
    :param has_energy_log: boolean flag indicating whether an energy log is present.
    :param has_tecplot: boolean flag indicating whether a tecplot file is present.
    :param has_neb_energies: boolean flag indicating whether neb energies file (path energies) is present.
    :param created: the time when the object was created.
    :param last_modified: the time when the object was last modified.
    """

    __tablename__ = 'neb_run_data'

    id = Column(Integer, primary_key=True, nullable=False)
    has_script = Column(Boolean, default=False, nullable=False)
    has_stdout = Column(Boolean, default=False, nullable=False)
    has_stderr = Column(Boolean, default=False, nullable=False)
    has_energy_log = Column(Boolean, default=False, nullable=False)
    has_tecplot = Column(Boolean, default=False, nullable=False)
    has_neb_energies = Column(Boolean, default=False, nullable=False)
    last_modified = Column(DateTime, default=now, onupdate=now, nullable=False)
    created = Column(DateTime, default=now, nullable=False)

    def as_dict(self):
        r"""
        Get a python dictionary representation of this object.

        :return: a dictionary representing this object.
        """

        return {
            "id": self.id,
            "has_script": self.has_script,
            "has_stdout": self.has_stdout,
            "has_stderr": self.has_stderr,
            "has_energy_log": self.has_energy_log,
            "has_tecplot": self.has_tecplot,
            "has_neb_energies": self.has_neb_energies,
            "last_modified": self.last_modified.strftime(GLOBAL.DATE_TIME_FORMAT),
            "created": self.created.strftime(GLOBAL.DATE_TIME_FORMAT)
        }


class NEBReportData(Base):
    r"""
    Stores NEB report data.

    :param id: the primary key.
    :param has_x_thumb_png: a boolean set to true if there is a thumbnail image of the model with the x-y axis corresponding to the user's screen/monitor.
    :param has_y_thumb_png: a boolean set to true if there is a thumbnail image of the model with the y-z axis corresponding to the user's screen/monitor.
    :param has_z_thumb_png: a boolean set to true if there is a thumbnail image of the model with the x-z axis corresponding to the user's screen/monitor.
    :param has_x_png: a boolean set to true if there is an image of the model with the x-y axis corresponding to the user's screen/monitor.
    :param has_y_png: a boolean set to true if there is an image of the model with the y-z axis corresponding to the user's screen/monitor.
    :param has_z_png: a boolean set to true if there is an image of the model with the x-z axis corresponding to the user's screen/monitor.
    :param last_modified: the date/time at which this object/record was modified.
    :param created: the creation date/time of this object/record.
    """

    __tablename__ = 'neb_report_data'

    id = Column(Integer, primary_key=True, nullable=False)
    has_x_thumb_png = Column(Boolean, default=False, nullable=False)
    has_y_thumb_png = Column(Boolean, default=False, nullable=False)
    has_z_thumb_png = Column(Boolean, default=False, nullable=False)
    has_x_png = Column(Boolean, default=False, nullable=False)
    has_y_png = Column(Boolean, default=False, nullable=False)
    has_z_png = Column(Boolean, default=False, nullable=False)
    last_modified = Column(DateTime, default=now, onupdate=now, nullable=False)
    created = Column(DateTime, default=now, nullable=False)

    def as_dict(self):
        r"""
        Get a python dictionary representation of this object.

        :return: a dictionary representing this object.
        """

        return {
            "id": self.id,
            "has_x_thumb_png": self.has_x_thumb_png,
            "has_y_thumb_png": self.has_y_thumb_png,
            "has_z_thumb_png": self.has_z_thumb_png,
            "has_x_png": self.has_x_png,
            "has_y_png": self.has_y_png,
            "has_z_png": self.has_z_png,
            "last_modified": self.last_modified.strftime(GLOBAL.DATE_TIME_FORMAT),
            "created": self.created.strftime(GLOBAL.DATE_TIME_FORMAT)
        }


class NEB(Base):
    r"""
    Information about Nudged Elastic Band (NEB) paths.

    :param id: the primary key.
    :param unique_id: the unique id of the model.
    :param spring_constant: the NEB calculation spring constant.
    :param curvature_weight: the NEB calculation curvature weight.
    :param no_of_points: the number of points that comprise the NEB path.
    :param max_energy_evaluations: the number of energy evaluations for each path point.
    :param max_path_evaluations: the number of evaluations for the complete path.
    :param energy_barrier: the energy barrier in Joules.
    :param last_modified: the date/time at which this object/record was modified.
    :param created: the creation date/time of this object/record.
    :param start_model: the start model, i.e. the first model on the NEB path.
    :param end_model: the end model, i.e. the last model on the NEB path.
    :param parent_neb: the NEB path that this path is a refinement of (or no path).
    :param neb_calculation_type: the db_type of calculation used for the computation of the path.
    :param neb_run_data: the data produced as part of the computation.
    :param neb_report_data: information indicating the artifacts that can be used to generate a report (also useful for the web).
    :param running_status: the running status of the NEB path.
    :param mdata: the metadata associated with the NEB path.
    """

    __tablename__ = 'neb'

    id = Column(Integer, primary_key=True, nullable=False)
    unique_id = Column(String, default=new_unique_id, nullable=False)
    spring_constant = Column(Float, nullable=True)
    curvature_weight = Column(Float, nullable=True)
    no_of_points = Column(Integer, nullable=True)
    max_energy_evaluations = Column(Integer, nullable=False, default=10000)
    max_path_evaluations = Column(Integer, nullable=False, default=5000)
    energy_barrier = Column(Float, nullable=True)
    last_modified = Column(DateTime, default=now, onupdate=now, nullable=False)
    created = Column(DateTime, default=now, nullable=False)

    applied_field_id = Column(Integer, ForeignKey('uniform_applied_field.id'), nullable=True)
    applied_field = relationship('UniformAppliedField', uselist=False, foreign_keys=[applied_field_id])

    start_model_id = Column(Integer, ForeignKey('model.id'), nullable=False)
    start_model = relationship('Model', uselist=False, foreign_keys=[start_model_id])

    end_model_id = Column(Integer, ForeignKey('model.id'), nullable=False)
    end_model = relationship('Model', uselist=False, foreign_keys=[end_model_id])

    parent_neb_id = Column(Integer, ForeignKey('neb.id'), default=None, nullable=True)
    parent_neb = relationship('NEB', uselist=False, foreign_keys=[parent_neb_id], remote_side=[id])

    neb_calculation_type_id = Column(Integer, ForeignKey('neb_calculation_type.id'), nullable=False)
    neb_calculation_type = relationship('NEBCalculationType')

    neb_run_data_id = Column(Integer, ForeignKey('neb_run_data.id'), nullable=False)
    neb_run_data = relationship('NEBRunData')

    neb_report_data_id = Column(Integer, ForeignKey('neb_report_data.id'), nullable=False)
    neb_report_data = relationship('NEBReportData', uselist=False)

    running_status_id = Column(Integer, ForeignKey('running_status.id'), nullable=False)
    running_status = relationship('RunningStatus', uselist=False)

    mdata_id = Column(Integer, ForeignKey('metadata.id'), nullable=False)
    mdata = relationship('Metadata', uselist=False)

    models = relationship('NEBModelSplit', back_populates='neb')

    __table_args__ = (
        UniqueConstraint('unique_id', name='uniq_neb_01'),
    )

    def as_dict(self):
        r"""
        Get a python dictionary representation of this object.

        Returns:
            A dictionary representing this object.

        """
        return {
            "id": self.id,
            "unique_id": self.unique_id,
            "spring_constant": self.spring_constant,
            "curvature_weight": self.curvature_weight,
            "no_of_points": self.no_of_points,
            "max_energy_evaluations": self.max_energy_evaluations,
            "max_path_evaluations": self.max_path_evaluations,
            "last_modified": self.last_modified.strftime(GLOBAL.DATE_TIME_FORMAT),
            "created": self.created.strftime(GLOBAL.DATE_TIME_FORMAT),
            "start_model_unique_id": self.start_model.unique_id,
            "end_model_unique_id": self.end_model.unique_id,
            "parent_neb_unique_id": self.parent_neb.unique_id if self.parent_neb is not None else None,
            "neb_calculation_type": self.neb_calculation_type.as_dict(),
            "neb_run_data": self.neb_run_data.as_dict(),
            "neb_report_data": self.neb_report_data.as_dict(),
            "running_status": self.running_status.as_dict(),
            "mdata": self.mdata.as_dict(),
        }


# noinspection PyUnusedLocal
def validate_neb(mapper, connection, value):
    r"""
    Routine to validate the addition of a new NEB path computation.
    """
    if not value.parent_neb:
        # Start and end must have same geometries
        if value.start_model.geometry.id != value.end_model.geometry.id:
            raise ValueError('NEB does not have start/end models with same geometry')

        # Start and end must have same no. of materials
        if len(value.start_model.materials) != len(value.end_model.materials):
            raise ValueError(
                'NEB does not have start/end models with same material. '
                'No of start model materials: {}, no. of end model materials: {}'.format(
                    ' '.join(map(lambda x : '{} {}'.format(x.name, x.temperature), value.start_model.materials)),
                    ' '.join(map(lambda x : '{} {}'.format(x.name, x.temperature), value.end_model.materials))
                )
            )

        # Start and end must have same materials
        start_material_ids = set()
        end_material_ids = set()

        for start_material in value.start_model.materials:
            start_material_ids.add(start_material.material.id)

        for end_material in value.end_model.materials:
            end_material_ids.add(end_material.material.id)

        if start_material_ids != end_material_ids:
            raise ValueError('NEB does not have start/end models with same material.')


event.listen(NEB, 'before_insert', validate_neb)


class NEBModelSplit(Base):
    r"""
    Table to track NEB path that has been split into individual path models.

    :param id: the primary key.
    :param image_number: the image index of the model along the NEB path.
    :param last_modified: the date/time at which this object/record was modified.
    :param created: the creation date/time of this object/record.
    :param neb: the NEB path to which the model split belongs.
    :param model: the model that is part of the NEB split.
    """
    __tablename__ = 'neb_model_split'

    id = Column(Integer, primary_key=True, nullable=False)

    image_number = Column(Integer, nullable=False)
    last_modified = Column(DateTime, default=now, onupdate=now, nullable=False)
    created = Column(DateTime, default=now, nullable=False)

    neb_id = Column(Integer, ForeignKey('neb.id'), primary_key=True, nullable=False)
    neb = relationship('NEB', back_populates='models')

    model_id = Column(Integer, ForeignKey('model.id'), primary_key=True, nullable=False)
    model = relationship('Model', back_populates='nebs')

