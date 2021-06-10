"""
The 'Script' parameter of a ProgrammableSource
"""

# https://docs.paraview.org/en/latest/ReferenceManual/pythonProgrammableFilter.html#programmable-filter

import numpy as np

from vtk.numpy_interface import algorithms as algs
from vtk.numpy_interface import dataset_adapter as dsa

# A util to get the current timestamp
def GetUpdateTimestep(algorithm):
    """
    Returns the requested time value, or None if not present
    """
    executive = algorithm.GetExecutive()
    outInfo = executive.GetOutputInformation(0)
    return outInfo.Get(executive.UPDATE_TIME_STEP()) \
              if outInfo.Has(executive.UPDATE_TIME_STEP()) else None

req_time = int((
    (GetUpdateTimestep(self) or self.t[0]) - self.t[0])/
    (self.t[-1] - self.t[0]) * (len(self.t) - 1)
)

# Configure output
executive = self.GetExecutive()
outInfo = executive.GetOutputInformation(0)
exts = [executive.UPDATE_EXTENT().Get(outInfo, i) for i in range(6)]
output.SetExtent(exts)

# Get data at specific timeframe
data = self.by[:,:,req_time]

# DEBUG: fill space with plane
data = np.broadcast_to(data[..., np.newaxis], data.shape + (self.zlength,))

# Generate points grid (not required on images)
#pts = vtk.vtkPoints()
#pts.SetData(dsa.numpyTovtkDataArray(self.points, "Points"))

output.PointData.append(data.ravel(order="F"), "By")
output.PointData.SetActiveScalars("By")

# Set current timestamp
output.GetInformation().Set(output.DATA_TIME_STEP(), req_time)
