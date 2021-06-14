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
print("Moving data to GPU. Allocating array %s..." % str(by.shape), end="", flush=True)
byfft = cp.asarray(by, dtype="complex64")
print("OK")
print("Applying fourier transform...", end="", flush=True)
byfft = cpx.scipy.fft.fftn(byfft,
                           axes=(0,1,2),
                           norm="forward",
                           overwrite_x=True)
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
print("Building propagation vector...", end="", flush=True)
# TODO: heavyside?
propag = cp.asarray(np.exp(-np.pi * 1j * FT * dz / c),
                    dtype="complex64")
print("OK")
# data = data * np.exp(-np.pi * 1j * (FX**2 + FY**2) * dz / FT)
prog = tqdm(range(zlength))
prog.set_description("Propagating")
for i in prog:
    byfft *= propag
    v = cpx.scipy.fftpack.ifftn(cp.asarray(byfft),
                                axes=(0,1,2))
    data.append(np.real(v.get()))
    del v

prog = tqdm(range(len(t)))
prog.set_description("Building frames")
frame = np.empty(x.shape + y.shape + (zlength,))
for i in prog:
    for z in range(zlength):
        frame[:,:,z] = data[z][:,:,i]

print("done")
