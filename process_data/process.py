"""
The 'RequestInformation Script' parameter of a ProgrammableSource
"""

# https://docs.paraview.org/en/latest/ReferenceManual/pythonProgrammableFilter.html#programmable-filter

import os
import numpy as np
import cupy as cp
import cupyx as cpx

# Some consts
c = 299792458

# Load files
print("Loading files...")
self.by = np.load(get_path('By.npy'))
self.x = np.load(get_path('x.npy'))
self.y = np.load(get_path('y.npy'))
self.t = np.load(get_path('t.npy'))
print("Files loaded!")

self.x, self.y = self.y, self.x

# Apply discrete fourier transform
print("Moving data to GPU. Allocation array: %s" % str(self.by.shape))
self.byfft = cp.asarray(self.by, dtype="complex64")
print("Applying fourier transform...")
self.byfft = cpx.scipy.fft.fftn(self.byfft,
                                axes=(0,1,2),
                                norm="forward",
                                overwrite_x=True)

print("OK!")

# Define Z axis (arbitrary)
self.zlength = 30
self.dz = 1 / self.zlength

# Build frequences grid
freqx = np.fft.fftfreq(self.x.size, d=self.x[1] - self.x[0])
freqy = np.fft.fftfreq(self.y.size, d=self.y[1] - self.y[0])
freqt = np.fft.fftfreq(self.t.size, d=self.t[1] - self.t[0])
self.FY, self.FX, self.FT = np.meshgrid(freqy, freqx, freqt, indexing='ij')

self.data = []

# Propagate
print("Propagating...")
# data = data * np.exp(-np.pi * 1j * (self.FX**2 + self.FY**2) * self.dz / self.FT)
for i in range(self.zlength):
    self.byfft *= np.exp(-np.pi * 1j * self.FT * self.dz / c)
    v = cupyx.scipy.fftpack.ifftn(self.byfft, axes=(0,1,2), norm="backward")
    self.data.append(np.asarray(v))
    del v

print("done")
