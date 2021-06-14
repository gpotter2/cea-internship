"""
The 'Script' parameter of a ProgrammableSource
"""

# https://docs.paraview.org/en/latest/ReferenceManual/pythonProgrammableFilter.html#programmable-filter

import numpy as np

from vtk.numpy_interface import algorithms as algs
from vtk.numpy_interface import dataset_adapter as dsa


executive = self.GetExecutive()
outInfo = executive.GetOutputInformation(0)

# A util to get the current timestamp
def GetUpdateTimestep():
    """
    Returns the requested time value, or None if not present
    """
    return outInfo.Get(executive.UPDATE_TIME_STEP()) \
              if outInfo.Has(executive.UPDATE_TIME_STEP()) else None

# Build time index
req_time = int((
    (GetUpdateTimestep() or self.t[0]) - self.t[0])/
    (self.t[-1] - self.t[0]) * (len(self.t) - 1)
)

# Configure output
exts = [executive.UPDATE_EXTENT().Get(outInfo, i) for i in range(6)]
output.SetExtent(exts)

# Get data at specific timeframe
data = np.load(get_path("f%s.npy" % req_time, True))

# DEBUG: fill space with first plane
# data = data[:,:,0]
# data = np.broadcast_to(data[..., np.newaxis],
#                        data.shape + (self.zlength,))

# Generate points grid (not required on images)
#pts = vtk.vtkPoints()
#pts.SetData(dsa.numpyTovtkDataArray(self.points, "Points"))

output.PointData.append(data.ravel(order="F"), "By")
output.PointData.SetActiveScalars("By")

# Set current timestamp
output.GetInformation().Set(output.DATA_TIME_STEP(), req_time)
