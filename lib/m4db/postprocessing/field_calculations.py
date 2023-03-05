import sys

import vtk

import numpy as np

from m4db.file_io.tecplot import read_tecplot


def formatFloat(flt):
    strFlt = "{:20.15E}".format(flt)
    if strFlt[0] != '-':
        return ' ' + strFlt
    return strFlt


def pathIdNameM(pathId):
    return 'm_{}'.format(pathId)


def pathIdNameH(pathId):
    return 'h_{}'.format(pathId)


def pathIdNameV(pathId):
    return 'v_{}'.format(pathId)


def pathIdNameADM(pathId):
    return 'adm_{}'.format(pathId)


def tec_to_unstructured_grid(absFileName, title=None, adm_fun='0.5*(1-(dot({M},iHat)^4 + dot({M},jHat)^4 + dot({M},kHat)^4))'):
    tec_raw = read_tecplot(absFileName)

    mag = None
    if title is None:
        mag = tec_raw["fields"][0]
    else:
        # Retrieve magnetization with title
        for index, field_title in enumerate(tec_raw["field_titles"]):
            if title == field_title:
                mag = tec_raw["fields"][index]
                break

    if mag is None:
        raise ValueError("Could not find magnetization associated with '{}'".format(title))

    vert = tec_raw['vertices']
    conn = tec_raw['elements']

    nvert = tec_raw['nvert']
    nconn = tec_raw['nelem']

    # print("len(mag): {}".format(len(mag)))

    # The unstructured grid
    ug = vtk.vtkUnstructuredGrid()

    # Vertices.
    # print("Adding vertices")
    points = vtk.vtkPoints()
    points.SetNumberOfPoints(nvert)
    for i in range(nvert):
        points.SetPoint(i, vert[i, 0], vert[i, 1], vert[i, 2])
    ug.SetPoints(points)

    # Connectivity
    for i in range(nconn):
        element = vtk.vtkIdList()

        element.InsertNextId(conn[i][0])
        element.InsertNextId(conn[i][1])
        element.InsertNextId(conn[i][2])
        element.InsertNextId(conn[i][3])

        ug.InsertNextCell(vtk.VTK_TETRA, element)

    # Magnetization
    mag_name = "M"
    vort_name = "V"
    hel_name = "H"
    rel_hel_name = "relH"
    adm_name = "ADM"

    field = vtk.vtkDoubleArray()
    field.SetName(mag_name)
    field.SetNumberOfComponents(3)
    field.SetNumberOfTuples(nvert)

    for i in range(nvert):
        field.SetTuple3(i, mag[i][0], mag[i][1], mag[i][2])

    ug.GetPointData().AddArray(field)

    vorticity = vtk.vtkGradientFilter()
    vorticity.ComputeVorticityOn()
    vorticity.SetInputArrayToProcess(0, 0, 0, 0, mag_name)
    vorticity.SetVorticityArrayName(vort_name)
    vorticity.SetInputData(ug)
    vorticity.Update()

    vfield = vtk.vtkDoubleArray()
    vfield.SetName(vort_name)
    vfield.SetNumberOfComponents(3)
    vfield.SetNumberOfTuples(nvert)

    vdata = vorticity.GetOutput().GetPointData().GetArray(vort_name)
    for i in range(nvert):
        vfield.SetTuple3(i, vdata.GetTuple(i)[0], vdata.GetTuple(i)[1], vdata.GetTuple(i)[2])
    ug.GetPointData().AddArray(vfield)

    # Helicity

    helicity = vtk.vtkArrayCalculator()
    # helicity.SetAttributeModeToUsePointData()
    helicity.AddVectorArrayName(mag_name)
    helicity.AddVectorArrayName(vort_name)
    helicity.SetResultArrayName(hel_name)
    helicity.SetFunction('dot({},{})'.format(mag_name, vort_name))
    helicity.SetInputData(vorticity.GetOutput())
    helicity.Update()

    hfield = vtk.vtkDoubleArray()
    hfield.SetName(hel_name)
    hfield.SetNumberOfComponents(1)
    hfield.SetNumberOfTuples(nvert)

    hdata = helicity.GetOutput().GetPointData().GetArray(hel_name)
    for i in range(nvert):
        hfield.SetValue(i, hdata.GetValue(i))
    ug.GetPointData().AddArray(hfield)

    # Relative helicity

    rel_helicity = vtk.vtkArrayCalculator()
    # rel_helicity.SetAttributeModeToUsePointData()
    rel_helicity.AddVectorArrayName(mag_name)
    rel_helicity.AddVectorArrayName(vort_name)
    rel_helicity.SetResultArrayName(rel_hel_name)
    rel_helicity.SetFunction("dot({V:},{M:})/(mag({V:})*mag({M:}))".format(V=vort_name, M=mag_name))
    rel_helicity.SetInputData(vorticity.GetOutput())
    rel_helicity.Update()

    rhfield = vtk.vtkDoubleArray()
    rhfield.SetName(rel_hel_name)
    rhfield.SetNumberOfComponents(1)
    rhfield.SetNumberOfTuples(nvert)

    rhdata = rel_helicity.GetOutput().GetPointData().GetArray(rel_hel_name)
    for i in range(nvert):
        rhfield.SetValue(i, rhdata.GetValue(i))
    ug.GetPointData().AddArray(rhfield)

    # ADM

    adm = vtk.vtkArrayCalculator()
    adm.AddVectorArrayName(mag_name)
    adm.SetResultArrayName(adm_name)
    adm.SetFunction(adm_fun.format(M=mag_name))
    adm.SetInputData(vorticity.GetOutput())
    adm.Update()

    adm_field = vtk.vtkDoubleArray()
    adm_field.SetName(adm_name)
    adm_field.SetNumberOfComponents(1)
    adm_field.SetNumberOfTuples(nvert)

    adm_data = adm.GetOutput().GetPointData().GetArray(adm_name)
    for i in range(nvert):
        adm_field.SetValue(i, adm_data.GetValue(i))
    ug.GetPointData().AddArray(adm_field)

    return ug, tec_raw


def write_vorticity_helicity_adm_to_vtk(ug, file_name):
    writer = vtk.vtkXMLUnstructuredGridWriter()
    writer.SetFileName(file_name)
    writer.SetInputData(ug)
    writer.Write()


def net_quantities(ug):
    r"""
    Integrate each component
    """
    vertices = ug.GetPoints().GetData()
    cells = ug.GetCells()
    cellData = cells.GetData()

    tmx = 0.0
    tmy = 0.0
    tmz = 0.0

    tvx = 0.0
    tvy = 0.0
    tvz = 0.0

    th = 0.0
    trh = 0.0

    tadm = 0.0

    vol = 0.0

    mag_name = "M"
    vort_name = "V"
    hel_name = "H"
    rel_hel_name = "relH"
    adm_name = "ADM"

    magnetization = ug.GetPointData().GetArray(mag_name)
    vorticity = ug.GetPointData().GetArray(vort_name)
    helicity = ug.GetPointData().GetArray(hel_name)
    rel_helicity = ug.GetPointData().GetArray(rel_hel_name)
    adm = ug.GetPointData().GetArray(adm_name)

    for cid in range(int(cellData.GetNumberOfTuples() / 5)):
        cvid1 = cellData.GetValue(5 * cid + 1)  # WARNING!! These offsets are correct
        cvid2 = cellData.GetValue(5 * cid + 2)  # since the 0th offset refers to
        cvid3 = cellData.GetValue(5 * cid + 3)  # the number of indices
        cvid4 = cellData.GetValue(5 * cid + 4)  # please see ref 1 below!

        # First vertex
        x1 = vertices.GetTuple(cvid1)[0]
        y1 = vertices.GetTuple(cvid1)[1]
        z1 = vertices.GetTuple(cvid1)[2]
        mx1 = magnetization.GetTuple(cvid1)[0]
        my1 = magnetization.GetTuple(cvid1)[1]
        mz1 = magnetization.GetTuple(cvid1)[2]
        vx1 = vorticity.GetTuple(cvid1)[0]
        vy1 = vorticity.GetTuple(cvid1)[1]
        vz1 = vorticity.GetTuple(cvid1)[2]
        h1 = helicity.GetValue(cvid1)
        rh1 = rel_helicity.GetValue(cvid1)
        adm1 = adm.GetValue(cvid1)

        # Second vertex
        x2 = vertices.GetTuple(cvid2)[0]
        y2 = vertices.GetTuple(cvid2)[1]
        z2 = vertices.GetTuple(cvid2)[2]
        mx2 = magnetization.GetTuple(cvid2)[0]
        my2 = magnetization.GetTuple(cvid2)[1]
        mz2 = magnetization.GetTuple(cvid2)[2]
        vx2 = vorticity.GetTuple(cvid2)[0]
        vy2 = vorticity.GetTuple(cvid2)[1]
        vz2 = vorticity.GetTuple(cvid2)[2]
        h2 = helicity.GetValue(cvid2)
        rh2 = rel_helicity.GetValue(cvid2)
        adm2 = adm.GetValue(cvid2)

        # Third vertex
        x3 = vertices.GetTuple(cvid3)[0]
        y3 = vertices.GetTuple(cvid3)[1]
        z3 = vertices.GetTuple(cvid3)[2]
        mx3 = magnetization.GetTuple(cvid3)[0]
        my3 = magnetization.GetTuple(cvid3)[1]
        mz3 = magnetization.GetTuple(cvid3)[2]
        vx3 = vorticity.GetTuple(cvid3)[0]
        vy3 = vorticity.GetTuple(cvid3)[1]
        vz3 = vorticity.GetTuple(cvid3)[2]
        h3 = helicity.GetValue(cvid3)
        rh3 = rel_helicity.GetValue(cvid3)
        adm3 = adm.GetValue(cvid3)

        # Fourth vertex
        x4 = vertices.GetTuple(cvid4)[0]
        y4 = vertices.GetTuple(cvid4)[1]
        z4 = vertices.GetTuple(cvid4)[2]
        mx4 = magnetization.GetTuple(cvid4)[0]
        my4 = magnetization.GetTuple(cvid4)[1]
        mz4 = magnetization.GetTuple(cvid4)[2]
        vx4 = vorticity.GetTuple(cvid4)[0]
        vy4 = vorticity.GetTuple(cvid4)[1]
        vz4 = vorticity.GetTuple(cvid4)[2]
        h4 = helicity.GetValue(cvid4)
        rh4 = rel_helicity.GetValue(cvid4)
        adm4 = adm.GetValue(cvid4)

        dxdydz = abs(np.linalg.det(
            np.array([
                [x1, y1, z1, 1.0],
                [x2, y2, z2, 1.0],
                [x3, y3, z3, 1.0],
                [x4, y4, z4, 1.0]
            ])
        ) / 6.0)

        tmx += ((mx1 + mx2 + mx3 + mx4) / 4.0) * dxdydz
        tmy += ((my1 + my2 + my3 + my4) / 4.0) * dxdydz
        tmz += ((mz1 + mz2 + mz3 + mz4) / 4.0) * dxdydz

        tvx += ((vx1 + vx2 + vx3 + vx4) / 4.0) * dxdydz
        tvy += ((vy1 + vy2 + vy3 + vy4) / 4.0) * dxdydz
        tvz += ((vz1 + vz2 + vz3 + vz4) / 4.0) * dxdydz

        th += ((h1 + h2 + h3 + h4) / 4.0) * dxdydz
        trh += ((rh1 + rh2 + rh3 + rh4) / 4.0) * dxdydz

        tadm += ((adm1 + adm2 + adm3 + adm4) / 4.0) * dxdydz

        vol += dxdydz

    return {
        'total_mx': tmx,
        'total_my': tmy,
        'total_mz': tmz,
        'total_vx': tvx,
        'total_vy': tvy,
        'total_vz': tvz,
        'total_h': th,
        'total_rh': trh,
        'total_adm': tadm,
        'total_vol': vol
    }

#
# References
#
# (1) http://vtk.1045678.n5.nabble.com/vtkCellArray-in-python-td3348424.html
#
