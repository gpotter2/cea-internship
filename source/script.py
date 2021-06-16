"""
The 'Script' parameter of a ProgrammableSource
"""

# https://docs.paraview.org/en/latest/ReferenceManual/pythonProgrammableFilter.html#programmable-filter

import numpy as np

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
    (GetUpdateTimestep() or 0)) / abs(dz)
)

# Configure output
exts = [executive.UPDATE_EXTENT().Get(outInfo, i) for i in range(6)]
output.SetExtent(exts)

# Get data at specific timeframe
fnpz = np.load(get_path("f%s.npz" % req_time, "frames"))
data = fnpz['frame']
fnpz.close()

# DEBUG: fill space with first plane
# data = data[:,:,0]
# data = np.broadcast_to(data[..., np.newaxis],
#                        data.shape + (self.zlength,))

# Generate points grid (not required on images)
# from vtk.numpy_interface import dataset_adapter as dsa
# pts = vtk.vtkPoints()
# pts.SetData(dsa.numpyTovtkDataArray(self.points, "Points"))

output.PointData.append(data.ravel(order="F"), "By")
output.PointData.SetActiveScalars("By")

# Set current timestamp
output.GetInformation().Set(output.DATA_TIME_STEP(), req_time)
