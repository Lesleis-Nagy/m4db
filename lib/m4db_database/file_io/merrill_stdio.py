r"""
A collection of routines to extract information form merrill stdout files.
"""

import re


def read_merrill_model_stdout(str_stdout):
    r"""
    This function will parse some merrill standard output and produce a python dictionary of values (see output).

    Arguments:
        str_stdout : the stdout string produced by merrill

    Output:
        a python dictionary with the following layout:
            {
                "anis_energy": <float>,
                "ext_energy": <float>,
                "demag_energy": <float>,
                "exch1_energy": <float>,
                "exch2_energy": <float>,
                "exch3_energy": <float>,
                "exch4_energy": <float>,
                "tot_energy": <float>,
                "mx": <float>,
                "my": <float>,
                "mz": <float>,
                "typical_energy_joule": <float>,
                "typical_energy_kvd": <float>,
                "failed": <boolean>,
                "restart": [
                    {
                        "delta_f": <float>,
                        "status": "SUCCESS" | "FAILED"
                    },
                    ...
                    {
                        "delta_f": <float>,
                        "status": "SUCCESS" | "FAILED"
                    }
                ]
            }.
        The "failed" flag is set to True, whenever any of the entries in the "restart" arrays is marked as "FAILED"
        i.e. *all* restarts must have succeeded in order for us to consider a model successful.
    """
    rstr_float = r'[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?'

    regex_joule_mode = re.compile(r'^Energies in units of J:$')
    regex_anis_energy = re.compile(r'^\s*E-Anis\s*({float:})\s*$'.format(
        float=rstr_float
    ))
    regex_ext_energy = re.compile(r'^\s*E-Ext\s*({float:})\s*$'.format(
        float=rstr_float
    ))
    regex_demag_energy = re.compile(r'^\s*E-Demag\s*({float:})\s*$'.format(
        float=rstr_float
    ))
    regex_exch1_energy = re.compile(r'^\s*E-Exch\s*({float:})\s*$'.format(
        float=rstr_float
    ))
    regex_exch2_energy = re.compile(r'^\s*E-Exch2\s*({float:})\s*$'.format(
        float=rstr_float
    ))
    regex_exch3_energy = re.compile(r'^\s*E-Exch3\s*({float:})\s*$'.format(
        float=rstr_float
    ))
    regex_exch4_energy = re.compile(r'^\s*E-Exch4\s*({float:})\s*$'.format(
        float=rstr_float
    ))
    regex_tot_energy = re.compile(r'^\s*E-Tot\s*({float:})\s*$'.format(
        float=rstr_float
    ))

    regex_avg_mag_mode = re.compile(r'^Average magnetization:$')
    regex_mx = re.compile(r'^\s*<Mx>\s*({float:})\s*$'.format(
        float=rstr_float
    ))
    regex_my = re.compile(r'^\s*<My>\s*({float:})\s*$'.format(
        float=rstr_float
    ))
    regex_mz = re.compile(r'^\s*<Mz>\s*({float:})\s*$'.format(
        float=rstr_float
    ))

    regex_typical_energy_mode = re.compile('^Typical energy scale.*$')
    regex_typical_energy_joule = re.compile(r'^\s*Typical Energy \(J\)\s*({float:})\s*$'.format(
        float=rstr_float
    ))
    regex_typical_energy_kvd = re.compile(r'^\s*Typical Energy \(Kd V\)\s*({float:})\s*$'.format(
        float=rstr_float
    ))

    regex_delta_f = re.compile(
        r'^\s*Delta F negligible:\s*({float:})\s*$'.format(
            float=rstr_float
        )
    )

    regex_failed_to_converge = re.compile(
        r'^.*FAILED TO CONVERGE.*$'
    )

    result = {
        'anis_energy': None,
        'ext_energy': None,
        'demag_energy': None,
        'exch1_energy': None,
        'exch2_energy': None,
        'exch3_energy': None,
        'exch4_energy': None,
        'tot_energy': None,
        'mx': None,
        'my': None,
        'mz': None,
        'typical_energy_joule': None,
        'typical_energy_kvd': None,
        'failed': None,
        'restart': None
    }

    joule_mode = False
    avg_mag_mode = False
    typical_energy_mode = False

    # Counts restart blocks.
    restart_counter = -1

    # Holds restart information.
    restart_info = []

    if isinstance(str_stdout, str):
        # If the user had provided a single string then split on the new line.
        stdout_lines = str_stdout.splitlines(False)
    else:
        # Assume that the user has provided a list of strings.
        stdout_lines = str_stdout

    # Process the stdout line by line.
    for line in stdout_lines:
        match_delta_f = regex_delta_f.match(line)
        if match_delta_f:
            restart_counter += 1

            restart_info.append({
                'delta_f': float(match_delta_f.group(1)),
                'status': 'SUCCESS'
            })
            continue

        match_failed_to_converge = regex_failed_to_converge.match(line)
        if match_failed_to_converge:
            restart_counter += 1

            restart_info.append({
                'delta_f': None,
                'status': 'FAILED'
            })
            continue

        match_joule_mode = regex_joule_mode.match(line)
        if match_joule_mode:
            joule_mode = True
            avg_mag_mode = False
            typical_energy_mode = False
            continue

        match_avg_mag_mode = regex_avg_mag_mode.match(line)
        if match_avg_mag_mode:
            joule_mode = False
            avg_mag_mode = True
            typical_energy_mode = False
            continue

        match_typical_energy = regex_typical_energy_mode.match(line)
        if match_typical_energy:
            joule_mode = False
            avg_mag_mode = False
            typical_energy_mode = True
            continue

        match_anis_energy = regex_anis_energy.match(line)
        if match_anis_energy and joule_mode:
            result['anis_energy'] = float(match_anis_energy.group(1))
            continue

        match_ext_energy = regex_ext_energy.match(line)
        if match_ext_energy and joule_mode:
            result['ext_energy'] = float(match_ext_energy.group(1))
            continue

        match_demag_energy = regex_demag_energy.match(line)
        if match_demag_energy and joule_mode:
            result['demag_energy'] = float(match_demag_energy.group(1))
            continue

        match_exch1_energy = regex_exch1_energy.match(line)
        if match_exch1_energy and joule_mode:
            result['exch1_energy'] = float(match_exch1_energy.group(1))
            continue

        match_exch2_energy = regex_exch2_energy.match(line)
        if match_exch2_energy and joule_mode:
            result['exch2_energy'] = float(match_exch2_energy.group(1))
            continue

        match_exch3_energy = regex_exch3_energy.match(line)
        if match_exch3_energy and joule_mode:
            result['exch3_energy'] = float(match_exch3_energy.group(1))
            continue

        match_exch4_energy = regex_exch4_energy.match(line)
        if match_exch4_energy and joule_mode:
            result['exch4_energy'] = float(match_exch4_energy.group(1))
            continue

        match_tot_energy = regex_tot_energy.match(line)
        if match_tot_energy and joule_mode:
            result['tot_energy'] = float(match_tot_energy.group(1))
            continue

        match_mx = regex_mx.match(line)
        if match_mx and avg_mag_mode:
            result['mx'] = float(match_mx.group(1))
            continue

        match_my = regex_my.match(line)
        if match_my and avg_mag_mode:
            result['my'] = float(match_my.group(1))
            continue

        match_mz = regex_mz.match(line)
        if match_mz and avg_mag_mode:
            result['mz'] = float(match_mz.group(1))
            continue

        match_typical_energy_joule = regex_typical_energy_joule.match(line)
        if match_typical_energy_joule and typical_energy_mode:
            result['typical_energy_joule'] = float(
                match_typical_energy_joule.group(1)
            )
            continue

        match_typical_energy_kvd = regex_typical_energy_kvd.match(line)
        if match_typical_energy_kvd and typical_energy_mode:
            result['typical_energy_kvd'] = float(
                match_typical_energy_kvd.group(1)
            )
            continue

    # Check if there is a failure in restart_info
    result['failed'] = False
    for r in restart_info:
        if r['status'] == 'FAILED':
            result['failed'] = True

    # Add restart_info to result
    result['restart'] = restart_info

    return result


def extract_path_data(file_name):
    r"""
    Extracts the path information from 'file_name'.

    :param file_name: the name of the file containing NEB path energy data.

    :return: a table of 2-tuples, the first entry corresponds to the path
             index, the second entry corresponds to the energy (in Joule).
    """
    regex_path_structure_energies_line = re.compile(
        r"^\s+Parsing\s+:\s+PathStructureEnergies$"
    )
    regex_path_line = re.compile(
        r"\s+([0-9]+)\s+([-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?)$"
    )

    MODE_NONE = 0
    MODE_PSTE = 1

    parse_data = []
    parse_mode = MODE_NONE
    with open(file_name, "r", errors="ignore") as fin:
        for line in fin:

            match_path_structure_energies_line = \
                regex_path_structure_energies_line.match(line)

            if match_path_structure_energies_line:
                parse_mode = MODE_PSTE
                continue

            match_path_line = regex_path_line.match(line)
            if match_path_line and parse_mode == MODE_PSTE:
                p_index = int(match_path_line.group(1))
                p_energy = float(match_path_line.group(2))
                parse_data.append((p_index, p_energy))

    return parse_data


def extract_path_type(file_name):
    r"""
    Extracts the path type information from 'file_name'.
    :param file_name: NEB path file.
    :return: a string: INITIAL_PATH, NEB_PATH, UNKNOWN_PATH
    """
    regex_initial_path = re.compile(r"MakeInitialPath")
    regex_neb_path = re.compile(r"PathMinimize")

    with open(file_name, "r", errors="ignore") as fin:
        for line in fin:
            match_initial_path = regex_initial_path.search(line, re.IGNORECASE)
            if match_initial_path:
                return "INITIAL_PATH"
            match_neb_path = regex_neb_path.search(line, re.IGNORECASE)
            if match_neb_path:
                return "NEB_PATH"

    return "UNKNOWN_PATH"


def count_path_fails_and_minimized(file_name):
    r"""
    Counts the failures / successful minimizations from 'file_name'
    :param file_name:
    :return:
    """
    regex_failed_to_converge = re.compile(r'FAILED TO CONVERGE')
    regex_minimization_finished = re.compile(r"MINIMIZATION FINISHED")

    n_failures = 0
    n_minimizations = 0
    with open(file_name, "r", errors="ignore") as fin:
        for line in fin:
            match_failed_to_converge = regex_failed_to_converge.search(line)
            if match_failed_to_converge:
                n_failures += 1
                continue
            match_minimization_finished = regex_minimization_finished.search(line)
            if match_minimization_finished:
                n_minimizations += 1
                continue

    return n_failures, n_minimizations


def is_merrill_model_finished(file_name):
    r"""
    Assesses whether a merrill model standard output corresponds with a finished model.
    :param file_name: the merrill model standard output file name.
    :return: True if the model corresponds with a 'finished' state, otherwise False.
    """
    regex_max_energy_evaluations_reached = re.compile(r'MAX Energy Evaluations reached')
    regex_gradient_negligible = re.compile(r'GRADIENT Negligible')
    regex_delta_f_negligible = re.compile(r'Delta F negligible')

    contains_gradient_negligible = False
    contains_delta_f_negligible = False

    with open(file_name, "r", errors="ignore") as fin:
        for line in fin:
            match_max_energy_evaluations_reached = regex_max_energy_evaluations_reached.search(line)
            if match_max_energy_evaluations_reached:
                # We reached the maximum no. of energy evaluations and so did *not* converge.
                return False

            match_gradient_negligible = regex_gradient_negligible.search(line)
            if match_gradient_negligible:
                # Set flag to indicate that gradient was negligible.
                contains_gradient_negligible = True
                continue

            match_delta_f_negligible = regex_delta_f_negligible.search(line)
            if match_delta_f_negligible:
                # Set flag to indicate that delta f was negligible.
                contains_delta_f_negligible = True
                continue

    # If flow reaches here, then we didn't reach maximum no. of energy evaluations

    if contains_gradient_negligible or contains_delta_f_negligible:
        # If we *did* find message telling us that the gradient or delta f were negligible
        return True
    else:
        # We found no message telling us that gradient or delta f was negligible
        return False
