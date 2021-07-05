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
    (GetUpdateTimestep() or 0)) / (
        abs(dz) if PROPAGATION_TYPE == "z" else dt
    )
)

# Configure output
exts = [executive.UPDATE_EXTENT().Get(outInfo, i) for i in range(6)]
output.SetExtent(exts)

# Get data at specific timeframe
fnpz = np.load(get_path("f%s%s.npz" % (req_time, self.SUFFIX), "frames"))
data = fnpz['frame']
fnpz.close()

# Scale data
data = data * cnob / cnoe

if self.LOG_SCALE:
    low = data < -self.LOG_THRESHOLD
    high = data > self.LOG_THRESHOLD
    mid = (data >= -self.LOG_THRESHOLD) & (data <= self.LOG_THRESHOLD)
    data[low] = -np.log10(-data[low])
    data[high] = np.log10(data[high])
    data[mid] = 0.

# DEBUG: fill space with first plane
# data = data[:,:,0]
# data = np.broadcast_to(data[..., np.newaxis],
#                        data.shape + (self.zlength,))

# Generate points grid (not required on images)
# from vtk.numpy_interface import dataset_adapter as dsa
# pts = vtk.vtkPoints()
# pts.SetData(dsa.numpyTovtkDataArray(self.points, "Points"))

if self.CLIP_HALF:
    data = data[:,:self.y.shape[0],:]

if self.CLIP_INV_QUARTER:
    data[self.x.shape[0]//2:,self.y.shape[0]//2:,:] = 0.

if self.CLIP_QUARTER:
    data[:self.x.shape[0]//2,:,:] = 0.
    data[:,:self.y.shape[0]//2,:] = 0.

output.PointData.append(data.ravel(order="F"), "By")
output.PointData.SetActiveScalars("By")

# Set current timestamp
output.GetInformation().Set(output.DATA_TIME_STEP(), req_time)
