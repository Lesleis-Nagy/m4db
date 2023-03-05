import schematics

######################################################################################################################
# Model quants schema                                                                                                #
######################################################################################################################

class ModelsQuantsSchema(schematics.models.Model):

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
