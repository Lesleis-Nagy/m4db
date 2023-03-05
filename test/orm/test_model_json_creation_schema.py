r"""
Test schema associated with the creation of new database objects.
"""


import unittest
import schematics
import schematics.exceptions
import xmlrunner

import json
from decimal import Decimal

from m4db.orm.model_creation_schema import EllipsoidSchema
from m4db.orm.model_creation_schema import TruncatedOctahedronSchema
from m4db.orm.model_creation_schema import MaterialSchema
from m4db.orm.model_creation_schema import AppliedFieldSchema
from m4db.orm.model_creation_schema import UniformInitialMagnetizationSchema
from m4db.orm.model_creation_schema import ModelInitialMagnetizationSchema
from m4db.orm.model_creation_schema import RandomInitialMagnetizationSchema
from m4db.orm.model_creation_schema import ModelSchema
from m4db.orm.model_creation_schema import ModelListSchema


class EllipsoidSchemaTestCase(unittest.TestCase):

    def test_all_full(self):

        geometry = EllipsoidSchema(json.loads(r"""
        {
            "type": "ellipsoid",
            "size": 0.100,
            "element-size": 0.001,
            "size-convention": "ESVD",
            "oblateness": 0.234,
            "prolateness": 0.567
        }
        """))
        geometry.validate()

        self.assertEqual(geometry.type, "ellipsoid")
        self.assertEqual(geometry.size, Decimal("0.100"))
        self.assertEqual(geometry.element_size, Decimal("0.001"))
        self.assertEqual(geometry.size_convention, "ESVD")
        self.assertEqual(geometry.oblateness, Decimal("0.234"))
        self.assertEqual(geometry.prolateness, Decimal("0.567"))


class TruncatedOctahedronSchemaTestCase(unittest.TestCase):

    def test_all_full(self):

        geometry = TruncatedOctahedronSchema(json.loads(r"""
        {
            "type": "truncated-octahedron",
            "size": 0.100,
            "element-size": 0.001,
            "size-convention": "ESVD",
            "aspect-ratio": 0.234,
            "truncation-factor": 0.700
        }
        """))
        geometry.validate()

        self.assertEqual(geometry.type, "truncated-octahedron")
        self.assertEqual(geometry.size, Decimal("0.100"))
        self.assertEqual(geometry.element_size, Decimal("0.001"))
        self.assertEqual(geometry.size_convention, "ESVD")
        self.assertEqual(geometry.aspect_ratio, Decimal("0.234"))
        self.assertEqual(geometry.truncation_factor, Decimal("0.700"))


class MaterialSchemaTestCase(unittest.TestCase):

    def test_all_full(self):

        material = MaterialSchema(json.loads(r"""
        {
            "name": "magnetite",
            "temperature": 123.11,
            "aex": 123.22,
            "k1": 123.33,
            "ms": 123.44,
            "dir-x": 123.55,
            "dir-y": 123.66,
            "dir-z": 123.77,
            "submesh-id": 123,
            "anisotropy-form": "cubic"
        }"""))

        self.assertEqual(material.name, "magnetite")
        self.assertEqual(material.temperature, Decimal("123.11"))
        self.assertEqual(material.aex, 123.22)
        self.assertEqual(material.k1, 123.33)
        self.assertEqual(material.ms, 123.44)
        self.assertEqual(material.dir_x, 123.55)
        self.assertEqual(material.dir_y, 123.66)
        self.assertEqual(material.dir_z, 123.77)
        self.assertEqual(material.submesh_id, 123)
        self.assertEqual(material.anisotropy_form, "cubic")

        material.validate()

    def test_required_only(self):

        material = MaterialSchema(json.loads(r"""
        {
            "name": "magnetite",
            "temperature": 123.11,
            "anisotropy-form": "cubic"
        }"""))

        self.assertEqual(material.name, "magnetite")
        self.assertEqual(material.temperature, Decimal("123.11"))
        self.assertIsNone(material.aex)
        self.assertIsNone(material.k1)
        self.assertIsNone(material.ms)
        self.assertIsNone(material.dir_x)
        self.assertIsNone(material.dir_y)
        self.assertIsNone(material.dir_z)

        material.validate()

    def test_required_missing(self):

        material = MaterialSchema(json.loads(r"""
        {
            "name": "magnetite"
        }"""))

        self.assertRaises(schematics.exceptions.DataError, material.validate)


class AppliedFieldSchemaTestCase(unittest.TestCase):

    def test_all_full(self):

        field = AppliedFieldSchema(json.loads(r"""
        {
            "magnitude": 123.11,
            "dir-x": 123.22,
            "dir-y": 123.33,
            "dir-z": 123.44
        }"""))

        self.assertEqual(field.magnitude, 123.11)
        self.assertEqual(field.dir_x, 123.22)
        self.assertEqual(field.dir_y, 123.33)
        self.assertEqual(field.dir_z, 123.44)

        field.validate()

    def test_required_missing(self):

        field = AppliedFieldSchema(json.loads(r"""
        {
            "magnitude": 123.11 
        }"""))

        self.assertRaises(schematics.exceptions.DataError, field.validate)


class TestUniformInitialMagnetizationSchema(unittest.TestCase):

    def test_all_full(self):

        field = UniformInitialMagnetizationSchema(json.loads(r"""
        {
            "type": "uniform",
            "magnitude": 123.11,
            "dir-x": 123.22,
            "dir-y": 123.33,
            "dir-z": 123.44
        }"""))

        self.assertEqual(field.type, "uniform")
        self.assertEqual(field.magnitude, 123.11)
        self.assertEqual(field.dir_x, 123.22)
        self.assertEqual(field.dir_y, 123.33)
        self.assertEqual(field.dir_z, 123.44)

        field.validate()

    def test_type_is_wrong(self):

        field = UniformInitialMagnetizationSchema(json.loads(r"""
        {
            "type": "uniforms",
            "magnitude": 123.11,
            "dir-x": 123.22,
            "dir-y": 123.33,
            "dir-z": 123.44
        }"""))

        self.assertRaises(schematics.exceptions.DataError, field.validate)

    def test_required_missing(self):

        field = UniformInitialMagnetizationSchema(json.loads(r"""
        {
            "magnitude": 123.11 
        }"""))

        self.assertRaises(schematics.exceptions.DataError, field.validate)


class TestModelInitialMagnetizationSchema(unittest.TestCase):

    def test_all_full(self):
        field = ModelInitialMagnetizationSchema(json.loads(r"""
        {
            "type": "model",
            "unique-id": "f5fa3b24-81de-4cfd-b27c-04a91a7b706a"
        }"""))

        self.assertEqual(field.type, "model")
        self.assertEqual(field.unique_id, "f5fa3b24-81de-4cfd-b27c-04a91a7b706a")

        field.validate()

    def test_type_is_wrong(self):
        field = ModelInitialMagnetizationSchema(json.loads(r"""
        {
            "type": "models",
            "unique-id": "f5fa3b24-81de-4cfd-b27c-04a91a7b706a"
        }"""))

        self.assertRaises(schematics.exceptions.DataError, field.validate)

    def test_unique_id_is_wrong(self):
        field = ModelInitialMagnetizationSchema(json.loads(r"""
        {
            "type": "model",
            "unique-id": "f5fa3b24-81de-4cfd-b27c-04a91a7b706g"
        }"""))

        self.assertRaises(schematics.exceptions.DataError, field.validate)

    def test_required_missing(self):
        field = ModelInitialMagnetizationSchema(json.loads(r"""
        {
            "type": "model" 
        }"""))

        self.assertRaises(schematics.exceptions.DataError, field.validate)


class TestRandomInitialMagnetizationSchema(unittest.TestCase):

    def test_all_full(self):
        field = RandomInitialMagnetizationSchema(json.loads(r"""
        {
            "type": "random"
        }"""))

        self.assertEqual(field.type, "random")

        field.validate()

    def test_type_is_wrong(self):
        field = RandomInitialMagnetizationSchema(json.loads(r"""
        {
            "type": "randoms"
        }"""))

        self.assertRaises(schematics.exceptions.DataError, field.validate)

    def test_required_is_missing(self):
        field = RandomInitialMagnetizationSchema(json.loads(r"""
        {}"""))

        self.assertRaises(schematics.exceptions.DataError, field.validate)


class TestModelSchema(unittest.TestCase):

    def test_model_with_random_initial_field_and_no_applied_field(self):

        try:
            model = ModelListSchema(json.loads(r"""
            {
                "models": [
                    {
                        "max-energy-evaluations": 123,
                        "geometry": {
                            "type": "truncated-octahedron",
                            "size": 0.100,
                            "element-size": 0.001,
                            "size-convention": "ESVD",
                            "aspect-ratio": 0.234,
                            "truncation-factor": 0.700
                        },
                        "materials": [
                            {"name": "magnetite", "temperature": 20.0, "submesh-id": 1, "anisotropy-form": "cubic"},
                            {"name": "maghemite", "temperature": 20.0, "submesh-id": 2, "anisotropy-form": "cubic"}
                        ],
                        "initial-magnetization": {
                            "type": "random"
                        },
                        "reps": 1
                    },
                    {
                        "max-energy-evaluations": 123,
                        "geometry": {
                            "type": "truncated-octahedron",
                            "size": 0.100,
                            "element-size": 0.001,
                            "size-convention": "ESVD",
                            "aspect-ratio": 0.234,
                            "truncation-factor": 0.700
                        },
                        "materials": [
                            {"name": "magnetite", "temperature": 20.0, "submesh-id": 1, "anisotropy-form": "cubic"},
                            {"name": "maghemite", "temperature": 20.0, "submesh-id": 2, "anisotropy-form": "cubic"}
                        ],
                        "initial-magnetization": {
                            "type": "random"
                        },
                        "reps": 1
                    }
                ]
            }
            """))
            model.validate()
        except schematics.exceptions.DataError as e:
            data = e.to_primitive()
            print(data)
            print("Model file validation has failed")
            for field, messages in data.items():
                print(f"\tField '{field}':")
                for field_id, submessages in messages.items():
                    for submessage in submessages:
                        print(f"\t\t* index: {field_id} field: {submessage}")


if __name__ == "__main__":
    with open("test-model-json-creation-schema.xml", "wb") as fout:
        unittest.main(
            testRunner=xmlrunner.XMLTestRunner(output=fout),
            failfast=False, buffer=False, catchbreak=False
        )
