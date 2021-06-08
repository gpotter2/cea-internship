"""
The 'RequestInformation Script' parameter of a ProgrammableSource
"""

# https://docs.paraview.org/en/latest/ReferenceManual/pythonProgrammableFilter.html#programmable-filter

import os
import numpy as np

import paraview.util

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

# Set boundaries
paraview.util.SetOutputWholeExtent(self, (
    # (xmin, xmax, ymin, ymax, zmin, zmax)
    0, self.x.shape[0],
    0, self.y.shape[0],
    0, 0
))

# Set time steps
outInfo.Remove(executive.TIME_STEPS())
for timestep in self.t:
    outInfo.Append(executive.TIME_STEPS(), timestep)

outInfo.Remove(executive.TIME_RANGE())
outInfo.Append(executive.TIME_RANGE(), self.t[0])
outInfo.Append(executive.TIME_RANGE(), self.t[-1])
