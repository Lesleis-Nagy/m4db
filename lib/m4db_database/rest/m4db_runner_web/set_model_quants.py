r"""
A service to set a model's quants.
"""
import falcon
import json

from m4db_database import GLOBAL
from m4db_database.orm.schema import Model

import schematics


class SetModelQuantsJSONSchema(schematics.models.Model):

    unique_id = schematics.types.StringType(regex=GLOBAL.UID_REGEX,
                                            required=True,
                                            deserialize_from="unique-id")
    mx_tot = schematics.types.FloatType(deserialize_from="mx-tot")
    my_tot = schematics.types.FloatType(deserialize_from="my-tot")
    mz_tot = schematics.types.FloatType(deserialize_from="mz-tot")
    vx_tot = schematics.types.FloatType(deserialize_from="vx-tot")
    vy_tot = schematics.types.FloatType(deserialize_from="vy-tot")
    vz_tot = schematics.types.FloatType(deserialize_from="vz-tot")
    h_tot = schematics.types.FloatType(deserialize_from="h-tot")
    rh_tot = schematics.types.FloatType(deserialize_from="rh-tot")
    adm_tot = schematics.types.FloatType(deserialize_from="adm-tot")
    e_typical = schematics.types.FloatType(deserialize_from="e-typical")
    e_anis = schematics.types.FloatType(deserialize_from="e-anis")
    e_ext = schematics.types.FloatType(deserialize_from="e-ext")
    e_demag = schematics.types.FloatType(deserialize_from="e-demag")
    e_exch1 = schematics.types.FloatType(deserialize_from="e-exch1")
    e_exch2 = schematics.types.FloatType(deserialize_from="e-exch2")
    e_exch3 = schematics.types.FloatType(deserialize_from="e-exch3")
    e_exch4 = schematics.types.FloatType(deserialize_from="e-exch4")
    e_tot = schematics.types.FloatType(deserialize_from="e-tot")


class SetModelQuants:

    def on_post(self, req, resp):
        r"""
        Set a model's quants.
        :param req: request object.
        :param resp: response object.
        :return: none
        """

        parameters = req.media
        self.logger.debug(parameters)

        try:
            quants = SetModelQuantsJSONSchema(json.loads(parameters))
            quants.validate()
            self.logger.debug(f"model-quants-data: {quants.to_primitive()}")
        except schematics.exceptions.ValidationError as e:
            self.logger.error(e)
            resp.status = falcon.HTTP_500
            return
        except schematics.exceptions.DataError as e:
            self.logger.error(e)
            resp.status = falcon.HTTP_500
            return

        # Retrieve the model and set the running status id.
        model = self.session.query(Model).\
            filter(Model.unique_id == quants.unique_id).one_or_none()
        if model is None:
            resp.status = falcon.HTTP_404
            resp.text = json.dumps({
                "error": f"Missing model with unique id: '{quants.unique_id}'."
            })
            return
        self.logger.debug(f"Model {model.unique_id}, has been retrieved.")

        if quants.mx_tot is not None:
            model.mx_tot = quants.mx_tot
            self.logger.debug(f"Model {model.unique_id}, mx-tot changed to {quants.mx_tot}.")
        if quants.my_tot is not None:
            model.my_tot = quants.my_tot
            self.logger.debug(f"Model {model.unique_id}, my-tot changed to {quants.my_tot}.")
        if quants.mz_tot is not None:
            model.mz_tot = quants.mz_tot
            self.logger.debug(f"Model {model.unique_id}, mz-tot changed to {quants.mz_tot}.")
        if quants.vx_tot is not None:
            model.vx_tot = quants.vx_tot
            self.logger.debug(f"Model {model.unique_id}, vx-tot changed to {quants.vx_tot}.")
        if quants.vy_tot is not None:
            model.vy_tot = quants.vy_tot
            self.logger.debug(f"Model {model.unique_id}, vy-tot changed to {quants.vy_tot}.")
        if quants.vz_tot is not None:
            model.vz_tot = quants.vz_tot
            self.logger.debug(f"Model {model.unique_id}, vz-tot changed to {quants.vz_tot}.")
        if quants.h_tot is not None:
            model.h_tot = quants.h_tot
            self.logger.debug(f"Model {model.unique_id}, h-tot changed to {quants.h_tot}.")
        if quants.rh_tot is not None:
            model.rh_tot = quants.rh_tot
            self.logger.debug(f"Model {model.unique_id}, rh-tot changed to {quants.rh_tot}.")
        if quants.adm_tot is not None:
            model.adm_tot = quants.adm_tot
            self.logger.debug(f"Model {model.unique_id}, adm-tot changed to {quants.adm_tot}.")
        if quants.e_typical is not None:
            model.e_typical = quants.e_typical
            self.logger.debug(f"Model {model.unique_id}, e-typical changed to {quants.e_typical}.")
        if quants.e_anis is not None:
            model.e_anis = quants.e_anis
            self.logger.debug(f"Model {model.unique_id}, e-anis changed to {quants.e_anis}.")
        if quants.e_ext is not None:
            model.e_ext = quants.e_ext
            self.logger.debug(f"Model {model.unique_id}, e-ext changed to {quants.e_ext}.")
        if quants.e_demag is not None:
            model.e_demag = quants.e_demag
            self.logger.debug(f"Model {model.unique_id}, e-demag changed to {quants.e_demag}.")
        if quants.e_exch1 is not None:
            model.e_exch1 = quants.e_exch1
            self.logger.debug(f"Model {model.unique_id}, e-exch1 changed to {quants.e_exch1}.")
        if quants.e_exch2 is not None:
            model.e_exch2 = quants.e_exch2
            self.logger.debug(f"Model {model.unique_id}, e-exch2 changed to {quants.e_exch2}.")
        if quants.e_exch3 is not None:
            model.e_exch3 = quants.e_exch3
            self.logger.debug(f"Model {model.unique_id}, e-exch3 changed to {quants.e_exch3}.")
        if quants.e_exch4 is not None:
            model.e_exch4 = quants.e_exch4
            self.logger.debug(f"Model {model.unique_id}, e-exch4 changed to {quants.e_exch4}.")
        if quants.e_tot is not None:
            model.e_tot = quants.e_tot
            self.logger.debug(f"Model {model.unique_id}, e-tot changed to {quants.e_tot}.")

        self.session.commit()
