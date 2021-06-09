"""
The 'Script' parameter of a ProgrammableSource
"""

# https://docs.paraview.org/en/latest/ReferenceManual/pythonProgrammableFilter.html#programmable-filter

import numpy as np

from vtk.numpy_interface import algorithms as algs
from vtk.numpy_interface import dataset_adapter as dsa

def GetUpdateTimestep(algorithm):
    """
    Returns the requested time value, or None if not present
    """
    executive = algorithm.GetExecutive()
    outInfo = executive.GetOutputInformation(0)
    return outInfo.Get(executive.UPDATE_TIME_STEP()) \
              if outInfo.Has(executive.UPDATE_TIME_STEP()) else None

req_time = int(GetUpdateTimestep(self) or 0)

data = self.by[:,:,req_time]

points = algs.make_vector(self.xgrid, self.ygrid, np.zeros(self.xgrid.shape))
pts = vtk.vtkPoints()
pts.SetData(dsa.numpyTovtkDataArray(points, "Points"))

output.SetPoints(pts)
output.PointData.append(data.ravel(), "By")
output.PointData.SetActiveScalars("By")

# next, we define the cells i.e. the connectivity for this mesh.
# here, we are creating merely a point could, so we'll add
# that as a single poly vextex cell.
numPts = pts.GetNumberOfPoints()
# ptIds is the list of point ids in this cell
# (which is all the points)
ptIds = vtk.vtkIdList()
ptIds.SetNumberOfIds(numPts)
for a in range(numPts):
    ptIds.SetId(a, a)

# Allocate space for 1 cell.
output.Allocate(1)
output.InsertNextCell(vtk.VTK_POLY_VERTEX, ptIds)

output.GetInformation().Set(output.DATA_TIME_STEP(), req_time)
