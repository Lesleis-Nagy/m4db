r"""
A collection of routines for geometry type calculations.
"""

import numpy as np

from math import sqrt


def tetra_volume(v0, v1, v2, v3):
    r"""
    Compute the volume of a tetrahedron from four vertices.
    :param v0: the first vertex of the tetrahedron.
    :param v1: the second vertex of the tetrahedron.
    :param v2: the third vertex of the tetrahedron.
    :param v3: the fourth vertex of the tetrahedron.
    :return: the volume of a tetrahedron.
    """
    m = np.array([
        [v0[0] - v3[0], v0[1] - v3[1], v0[2] - v3[2]],
        [v1[0] - v3[0], v1[1] - v3[1], v1[2] - v3[2]],
        [v2[0] - v3[0], v2[1] - v3[1], v2[2] - v3[2]]
    ])

    return abs((1.0 / 6.0) * np.linalg.det(m))


def edge_length(v0, v1):
    r"""
    Return the distance between v0 and v1
    :param v0: the first vertex of an edge.
    :param v1: the second vertex of an edge.
    :return: the distance between v0 & v1
    """
    return sqrt((v0[0] - v1[0]) ** 2 + (v0[1] - v1[1]) ** 2 + (v0[2] - v1[2]) ** 2)


def order_pair(pair):
    r"""
    Given a pair, return a pair with the two entries in numerical order i.e.
    ordered_pair(1, 2) returns (1, 2) whereas ordered_pair(2, 1) returns (1, 2)
    :param pair: a pair of numbers
    :return: the input pair in order
    """
    if pair[1] < pair[0]:
        return pair[1], pair[0]
    else:
        return pair[0], pair[1]


def geometry_volume(vertices, elements):
    r"""
    Compute the volume of a geometry
    :param vertices: the vertices of the mesh.
    :param elements: the element indices of the mesh.
    :return: the total volume of a geometry.
    """

    # For each tetrahedron calculate a volume
    tetra_volumes = []
    for elem_idxs in elements:
        v0 = vertices[elem_idxs[0]]
        v1 = vertices[elem_idxs[1]]
        v2 = vertices[elem_idxs[2]]
        v3 = vertices[elem_idxs[3]]
        tetra_volumes.append(tetra_volume(v0, v1, v2, v3))

    # Return the sum total volume
    return sum(tetra_volumes)


def geometry_edge_stats(vertices, elements):
    r"""
    Compute statistics related to tetrahedral edge lengths of a geometry
    :param vertices: the vertices of the mesh.
    :param elements: the element indices of the mesh.
    :return: a tuple containing:
                average edge length,
                standard deviation of edge length,
                maximum edge length,
                minimum edge length
    """
    # For each unique edge, calculate a distance.
    edge_lengths = {}
    for elem_idxs in elements[:, 0:3]:
        for vidx_i in range(len(elem_idxs)):
            for vidx_j in range(vidx_i+1, len(elem_idxs)):
                edge_key = order_pair((elem_idxs[vidx_i], elem_idxs[vidx_j]))

                if (edge_key[0] == edge_key[1]):
                    print("WARNING: defective edge key for element {}".format(elem_idxs))

                if order_pair(edge_key) not in edge_lengths:
                    v_i = vertices[edge_key[0]]
                    v_j = vertices[edge_key[1]]
                    edge_lengths[edge_key] = edge_length(v_i, v_j)

                    if abs(edge_lengths[edge_key]) < 1E-15:
                        print("WARNING: there is a zero edge length!")
                        print("edge key: {}".format(edge_key))

    # Take the average
    lengths = list(edge_lengths.values())
    return np.average(lengths), np.std(lengths), max(lengths), min(lengths)
