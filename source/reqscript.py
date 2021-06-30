"""
The 'RequestInformation Script' parameter of a ProgrammableSource
"""

# https://docs.paraview.org/en/latest/ReferenceManual/pythonProgrammableFilter.html#programmable-filter

import builtins
import glob

import numpy as np

# Configure output
executive = self.GetExecutive()
outInfo = executive.GetOutputInformation(0)

# Count frames
self.nbframes = builtins.sum(1 for _ in glob.iglob(get_path("*", "frames")))

# Read axis
self.x = np.load(get_path("x.npy", "npy_files"))[::x_drop]
self.y = np.load(get_path("y.npy", "npy_files"))[::y_drop]
self.t = np.load(get_path("t.npy", "npy_files"))

if self.CLIP_HALF:
    self.y = self.y[self.y.shape[0] // 2:]

if PROPAGATION_TYPE == "z":
    self.third_axis_length = self.t.shape[0]
else:
    self.third_axis_length = Z_LENGTH if Z_LENGTH is not None else self.shape[0]

## Define re-usable grid
#X, Y, Z = np.meshgrid(self.x, self.y, self.z)
#self.points = algs.make_vector(X.ravel(),
#                               Y.ravel(),
#                               Z.ravel())

if PROPAGATION_TYPE == "z":
    dz = self.t[1] - self.t[0]
    dt = abs(dz)
elif PROPAGATION_TYPE == "t":
    TOT_Z = TOT_Z or (self.t[0] - self.t[-1])
    dz = abs(TOT_Z) / self.third_axis_length

# Set boundaries
outInfo.Set(executive.WHOLE_EXTENT(),
    # (xmin, xmax, ymin, ymax, zmin, zmax)
    0, self.x.shape[0] - 1,
    0, self.y.shape[0] - 1,
    0, self.third_axis_length - 1
)
outInfo.Set(vtk.vtkDataObject.SPACING(),
    # (dx, dy, dz)
    self.x[1] - self.x[0],
    self.y[1] - self.y[0],
    dz
)
if PROPAGATION_TYPE == "t":
    outInfo.Set(vtk.vtkDataObject.ORIGIN(), 0, 0, -TOT_Z)

self.MAX_INSTANT = builtins.min(self.nbframes, self.MAX_INSTANT)

# Set time steps
outInfo.Remove(executive.TIME_STEPS())
for timestep in range(0, self.MAX_INSTANT):
    outInfo.Append(executive.TIME_STEPS(), timestep * dt)

outInfo.Remove(executive.TIME_RANGE())
outInfo.Append(executive.TIME_RANGE(), 0)
outInfo.Append(executive.TIME_RANGE(), self.MAX_INSTANT)
