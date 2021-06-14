"""
The 'RequestInformation Script' parameter of a ProgrammableSource
"""

# https://docs.paraview.org/en/latest/ReferenceManual/pythonProgrammableFilter.html#programmable-filter

import builtins
import glob

import numpy as np
import cupy as cp
import cupyx as cpx

self.dz = dz
self.zlength = zlength

# Configure output
executive = self.GetExecutive()
outInfo = executive.GetOutputInformation(0)

# Count frames
self.nbframes = builtins.sum(1 for _ in glob.iglob(get_path("*", True)))

# Read axis
self.x = np.load(get_path("x.npy"))
self.y = np.load(get_path("y.npy"))
# We crop because maybe processing was cancelled (frame files missing)
self.t = np.load(get_path("t.npy"))[:self.nbframes]

## Define re-usable grid
#X, Y, Z = np.meshgrid(self.x, self.y, self.z)
#self.points = algs.make_vector(X.ravel(),
#                               Y.ravel(),
#                               Z.ravel())

# Set boundaries
outInfo.Set(executive.WHOLE_EXTENT(),
    # (xmin, xmax, ymin, ymax, zmin, zmax)
    0, self.x.shape[0] - 1,
    0, self.y.shape[0] - 1,
    0, self.zlength - 1
)
outInfo.Set(vtk.vtkDataObject.SPACING(),
    # (dx, dy, dz)
    self.x[1] - self.x[0],
    self.y[1] - self.y[0],
    self.dz
)

# Set time steps
outInfo.Remove(executive.TIME_STEPS())
for timestep in self.t:
    outInfo.Append(executive.TIME_STEPS(), timestep)

outInfo.Remove(executive.TIME_RANGE())
outInfo.Append(executive.TIME_RANGE(), self.t[0])
outInfo.Append(executive.TIME_RANGE(), self.t[-1])
