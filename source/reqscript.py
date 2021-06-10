"""
The 'RequestInformation Script' parameter of a ProgrammableSource
"""

# https://docs.paraview.org/en/latest/ReferenceManual/pythonProgrammableFilter.html#programmable-filter

import os
import numpy as np

import paraview.util

# Some consts
c = 299792458

# Configure output
executive = self.GetExecutive()
outInfo = executive.GetOutputInformation(0)

# Load files
print("Loading files...")
self.by = np.load(get_path('By.npy'))
self.x = np.load(get_path('x.npy'))
self.y = np.load(get_path('y.npy'))
self.t = np.load(get_path('t.npy'))
print("Files loaded!")

self.x, self.y = self.y, self.x

# print("Debug")
# print(self.by.shape)
# print(self.x.shape)
# print(self.y.shape)
# print(self.t.shape)

# Define Z axis (arbitrary)
self.zlength = 30
self.z = np.arange(0, self.zlength, 1)

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
    0, self.z.shape[0] - 1
)
outInfo.Set(vtk.vtkDataObject.SPACING(),
    # (dx, dy, dz)
    self.x[1] - self.x[0],
    self.y[1] - self.y[0],
    self.z[1] - self.z[0],
)

# Set time steps
outInfo.Remove(executive.TIME_STEPS())
for timestep in self.t:
    outInfo.Append(executive.TIME_STEPS(), timestep)

outInfo.Remove(executive.TIME_RANGE())
outInfo.Append(executive.TIME_RANGE(), self.t[0])
outInfo.Append(executive.TIME_RANGE(), self.t[-1])
