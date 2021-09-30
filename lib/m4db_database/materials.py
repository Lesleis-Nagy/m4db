#!/usr/bin/env python

from math import *


def saturation_magnetization(t, material='iron'):
    if material == 'iron':
        t = 273.0 + t
        return 1.75221e6 - 1.21716e3 * t + 33.3368 * (t ** 2) - 0.363228 * (t ** 3) + 1.96713e-3 * (t ** 4) \
               - 5.98015e-6 * (t ** 5) + 1.06587e-8 * (t ** 6) - 1.1048e-11 * (t ** 7) + 6.16143e-15 * (t ** 8) \
               - 1.42904e-18 * (t ** 9)
    elif material == 'magnetite':
        t_c = 580.0
        return 737.384 * 51.876 * (t_c - t) ** 0.4
    else:
        raise ValueError("Saturation magnetization calculation with unknown material '{}'".format(material))


def exchange_constant(t, material='iron'):
    if material == 'iron':
        t = 273.0 + t
        return -1.8952e-12 + 3.0657e-13 * t - 1.599e-15 * (t ** 2) + 4.0151e-18 * (t ** 3) - 5.3728e-21 * (t ** 4) \
               + 3.6501e-24 * (t ** 5) - 9.9515e-28 * (t ** 6)
    elif material == 'magnetite':
        t_c = 580.0
        return (sqrt(21622.526 + 816.476 * (t_c - t)) - 147.046) / 408.238e11
    else:
        raise ValueError("Exchange calculation with unknown material '{}'".format(material))


def anisotropy_constant(t, material='iron'):
    if material == 'iron':
        t = (273.0 + t)
        k1 = 54967.1 + 44.2946 * t - 0.426485 * (t ** 2) + 0.000811152 * (t ** 3) - 1.07579e-6 * (t ** 4) + \
             8.83207e-10 * (t ** 5) - 2.90947e-13 * (t ** 6)
        k1 = k1 * (480.0 / 456.0)
        return k1
    elif material == 'magnetite':
        t_c = 580.0
        return -2.13074e-5 * (t_c - t) ** 3.2
    else:
        raise ValueError("Magnetocrystalline anisotropy calculation with unknown material '{}'".format(material))


def saturation_energy(t, material='iron'):
    mu = 1e-7
    ms = saturation_magnetization(t, material=material)

    return 4 * 3.1415926535897932 * mu * ms * ms * 0.5


def lambda_ex(t, material='iron'):
    a = exchange_constant(t, material=material)
    kd = saturation_energy(t, material=material)

    try:
        r_val = sqrt(a / kd)
        return r_val
    except ValueError:
        return None
    except ZeroDivisionError:
        return None


def q_hardness(t, material='iron'):
    k1 = anisotropy_constant(t, material=material)
    kd = saturation_energy(t, material=material)

    try:
        r_val = k1 / kd
        return r_val
    except ValueError:
        return None
    except ZeroDivisionError:
        return None


def material_parameters(t, material='iron'):
    if material == 'iron':
        anisform = 'cubic'
    elif material == 'magnetite':
        anisform = 'cubic'
    else:
        raise ValueError("Attempting to calculate material parameters for unknown material '{}'".format(material))

    ms = saturation_magnetization(t, material=material)
    a = exchange_constant(t, material=material)
    k1 = anisotropy_constant(t, material=material)
    kd = saturation_energy(t, material=material)
    lex = lambda_ex(t, material=material)
    qhd = q_hardness(t, material=material)

    return {'anisform': anisform,
            'material': material,
            'Aex': a,
            'Ms': ms,
            'K1': k1,
            'Kd': kd,
            'lambda_ex': lex,
            'q_hardness': qhd}


def iron_parameters(t):
    return material_parameters(t, 'iron')


def magnetite_parameters(t):
    return material_parameters(t, 'magnetite')
