r"""
Routines to read patran files.
"""

import linecache
import re

import numpy as np

regex_header_data = re.compile("^26\s+([0-9]+)\s+([0-9]+)\s+([0-9]+)\s+([0-9]+)\s+([0-9]+)\s+([0-9]+)\s+([0-9]+)\s+([0-9]+)$")
regex_vertex_data = re.compile(r"^01\s+([0-9]+)\s+([0-9]+)\s+([0-9]+)\s+([0-9]+)\s+([0-9]+)\s+([0-9]+)\s+([0-9]+)\s+([0-9]+)$")
regex_element_data = re.compile(r"^02\s+([0-9]+)\s+([0-9]+)\s+([0-9]+)\s+([0-9]+)\s+([0-9]+)\s+([0-9]+)\s+([0-9]+)\s+([0-9]+)$")


def read_patran(patran_file):
    r"""
    Read a patran file header information.
    :param patran_file: the patran file name
    :return: patran file header information.
    """
    current_line_no = 1
    vertex_dict = {}
    element_dict = {}
    submesh_ids = {}
    nverts = 0
    nelems = 0
    while linecache.getline(patran_file, current_line_no) != '':

        line = linecache.getline(patran_file, current_line_no).strip()

        match_header_data = regex_header_data.match(line)
        if match_header_data:
            nverts = int(match_header_data.group(4))
            nelems = int(match_header_data.group(5))

            # Advance the current line
            current_line_no += 1
            continue

        match_vertex_data = regex_vertex_data.match(line)
        if match_vertex_data:
            index = int(match_vertex_data.group(1)) - 1

            # Advance a line & extract the vertex components
            current_line_no += 1
            line = linecache.getline(patran_file, current_line_no).strip()
            components = [float(f.strip()) for f in re.split(r"\s+", line)]
            vertex_dict[index] = (components[0], components[1], components[2])

            continue

        match_element_data = regex_element_data.match(line)
        if match_element_data:
            index = int(match_element_data.group(1)) - 1

            # Advance a line & extract the submesh index
            current_line_no += 1
            line = linecache.getline(patran_file, current_line_no).strip()
            components = re.split(r"\s+", line)
            submesh_id = int(components[2])
            submesh_ids[submesh_id] = True

            # Advance a line & extract the element indices
            current_line_no += 1
            line = linecache.getline(patran_file, current_line_no).strip()
            components = [int(idx.strip()) - 1 for idx in re.split(r"\s+", line)]
            element_dict[index] = (components[0], components[1], components[2], components[3], submesh_id)

            continue

        current_line_no += 1

    # Contiguity check for vertex indices
    vertex_indices = sorted(vertex_dict.keys())
    vertex_range_list = list(range(min(vertex_indices), max(vertex_indices)+1))
    if vertex_indices != vertex_range_list:
        raise ValueError("Vertex indices are not contiguous.")

    # Set the vertices
    vertices = np.zeros((len(vertex_dict), 3))
    for i in range(len(vertices)):
        vertices[i][0] = vertex_dict[i][0]
        vertices[i][1] = vertex_dict[i][1]
        vertices[i][2] = vertex_dict[i][2]

    # Contiguity check for element indices
    element_indices = sorted(element_dict.keys())
    element_range_list = list(range(min(element_indices), max(element_indices)+1))
    if element_indices != element_range_list:
        raise ValueError("Element indices are not contiguous.")

    # Set the elements
    elements = np.zeros((len(element_dict), 5), dtype=int)
    for i in range(len(elements)):
        elements[i][0] = element_dict[i][0]
        elements[i][1] = element_dict[i][1]
        elements[i][2] = element_dict[i][2]
        elements[i][3] = element_dict[i][3]
        elements[i][4] = element_dict[i][4]

    # Check that the number of vertices match
    if len(vertices) != nverts:
        raise ValueError("Error reading Patran file, no. of vertices found {} (expected {})".format(
            len(vertices), nverts
        ))

    # Check that the number of elements match
    if len(elements) != nelems:
        raise ValueError("Error reading Patran file, no. of elements found {} (expected {})".format(
            len(elements), nelems
        ))

    return {
        "vertices": vertices,
        "elements": elements,
        "submesh_indices": sorted(submesh_ids.keys())
    }
