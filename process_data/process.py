"""
The 'RequestInformation Script' parameter of a ProgrammableSource
"""

# https://docs.paraview.org/en/latest/ReferenceManual/pythonProgrammableFilter.html#programmable-filter

import os
import numpy as np
import cupy as cp
import cupyx as cpx

from tqdm import tqdm

def get_path(x):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "npy_files", x))

# Some consts
c = 299792458

# Load files
print("Loading files...", end="", flush=True)
by = np.load(get_path('By.npy'))
x = np.load(get_path('x.npy'))
y = np.load(get_path('y.npy'))
t = np.load(get_path('t.npy'))
print("OK")

# Apply discrete fourier transform
print("Moving data to GPU. Allocation array: %s..." % str(by.shape), end="", flush=True)
byfft = cp.asarray(by, dtype="complex64")
print("OK")
print("Applying fourier transform...", end="", flush=True)
byfft = np.fft.fftn(by,
                    axes=(0,1,2),
                    norm="forward")

print("OK")

# Define Z axis (arbitrary)
zlength = 30
dz = 1 / zlength

print("Building freq grid...", end="", flush=True)
# Build frequences grid
freqx = np.fft.fftfreq(x.size, d=x[1] - x[0])
freqy = np.fft.fftfreq(y.size, d=y[1] - y[0])
freqt = np.fft.fftfreq(t.size, d=t[1] - t[0])
FY, FX, FT = np.meshgrid(freqy, freqx, freqt, indexing='ij')
print("OK")

data = []

# Propagate
print("Propagating...")
# data = data * np.exp(-np.pi * 1j * (FX**2 + FY**2) * dz / FT)
for i in tqdm(range(zlength)):
    print(byfft.shape)
    print(FT.shape)
    byfft *= np.asarray(np.exp(-np.pi * 1j * FT * dz / c))
    v = cupyx.scipy.fftpack.ifftn(cp.asarray(byfft), axes=(0,1,2), norm="backward")
    data.append(np.asarray(v))
    del v

print("done")
