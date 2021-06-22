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

if PROPAGATION_TYPE == "z":
    self.third_axis_length = self.t.shape[0]
else:
    self.third_axis_length = z_length

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
    0, self.third_axis_length - 1
)
dt = self.t[1] - self.t[0]
outInfo.Set(vtk.vtkDataObject.SPACING(),
    # (dx, dy, dz)
    self.x[1] - self.x[0],
    self.y[1] - self.y[0],
    dt if PROPAGATION_TYPE == "z" else (self.t.shape[0] / z_length)
)

MAX_INSTANT = builtins.min(self.nbframes, MAX_INSTANT)

# Set time steps
outInfo.Remove(executive.TIME_STEPS())
for timestep in range(0, MAX_INSTANT):
    outInfo.Append(executive.TIME_STEPS(), timestep * (
        abs(dz) if PROPAGATION_TYPE == "z" else dt
    ))

outInfo.Remove(executive.TIME_RANGE())
outInfo.Append(executive.TIME_RANGE(), 0)
outInfo.Append(executive.TIME_RANGE(), MAX_INSTANT)
