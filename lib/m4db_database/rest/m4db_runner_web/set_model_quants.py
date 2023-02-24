r"""
A service to set a model's quants.
"""

from m4db_database.orm.schema import Model


class SetModelQuants:

    def on_post(self, req, resp):
        r"""
        Set a model's quants.
        :param req: request object.
        :param resp: response object.
        :return: none
        """

        parameters = req.media

        # Retrieve the model and set the quants.
        model = self.session.query(Model).\
            filter(Model.unique_id == parameters["unique_id"]).one()

        if "mx_tot" in parameters.keys():
            model.mx_tot = parameters["mx_tot"]
        if "my_tot" in parameters.keys():
            model.my_tot = parameters["my_tot"]
        if "mz_tot" in parameters.keys():
            model.mz_tot = parameters["mz_tot"]
        if "vx_tot" in parameters.keys():
            model.vx_tot = parameters["vx_tot"]
        if "vy_tot" in parameters.keys():
            model.vy_tot = parameters["vy_tot"]
        if "vz_tot" in parameters.keys():
            model.vz_tot = parameters["vz_tot"]
        if "h_tot" in parameters.keys():
            model.h_tot = parameters["h_tot"]
        if "rh_tot" in parameters.keys():
            model.rh_tot = parameters["rh_tot"]
        if "adm_tot" in parameters.keys():
            model.adm_tot = parameters["adm_tot"]
        if "e_typical" in parameters.keys():
            model.e_typical = parameters["e_typical"]
        if "e_anis" in parameters.keys():
            model.e_anis = parameters["e_anis"]
        if "e_ext" in parameters.keys():
            model.e_ext = parameters["e_ext"]
        if "e_demag" in parameters.keys():
            model.e_demag = parameters["e_demag"]
        if "e_exch1" in parameters.keys():
            model.e_exch1 = parameters["e_exch1"]
        if "e_exch2" in parameters.keys():
            model.e_exch2 = parameters["e_exch2"]
        if "e_exch3" in parameters.keys():
            model.e_exch3 = parameters["e_exch3"]
        if "e_exch4" in parameters.keys():
            model.e_exch4 = parameters["e_exch4"]
        if "e_tot" in parameters.keys():
            model.e_tot = parameters["e_tot"]
        if "volume" in parameters.keys():
            model.volume = parameters["volume"]

        self.session.commit()
