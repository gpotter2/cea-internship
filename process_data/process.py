"""
The 'RequestInformation Script' parameter of a ProgrammableSource
"""

# https://docs.paraview.org/en/latest/ReferenceManual/pythonProgrammableFilter.html#programmable-filter

import os
import numpy as np
import cupy as cp
import cupyx as cpx

from tqdm import tqdm

def get_path(x, path=[]):
    return os.path.abspath(os.path.join(*([os.path.dirname(__file__)] + path + [x])))

# Read config
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config import dz, zlength

# Load files
print("Loading files...", end="", flush=True)
by = np.load(get_path('By.npy', ["..", "npy_files"]))
x = np.load(get_path('x.npy', ["..", "npy_files"]))
y = np.load(get_path('y.npy', ["..", "npy_files"]))
t = np.load(get_path('t.npy', ["..", "npy_files"]))
print("OK")

# Apply discrete fourier transform
print("Moving data to GPU. Allocating array %s..." % str(by.shape), end="", flush=True)
byfft = cp.asarray(by, dtype="complex64")
print("OK")

# FFT
print("Applying discrete fast fourier transform...", end="", flush=True)
cpx.scipy.fft.fftn(byfft,
                   axes=(0,1,2),
                   norm="forward",
                   overwrite_x=True)
print("OK")

print("Building freq grid...", end="", flush=True)
# Build frequences grid
freqy = np.fft.fftfreq(y.size, d=y[1] - y[0])
freqx = np.fft.fftfreq(x.size, d=x[1] - x[0])
freqt = np.fft.fftfreq(t.size, d=t[1] - t[0])
FY, FX, FT = np.meshgrid(freqy, freqx, freqt, indexing='ij')
print("OK")

data = []

# Propagate

print("Building propagation vector...", end="", flush=True)
# See PROPAGATION_DEMO.md for explanation of this formula
propag = np.zeros(by.shape, dtype="complex64")
FTi, FTni = (np.abs(FT) > 0.01), (np.abs(FT) <= 0.01)  # Do not try to divide by 0
propag[FTi] = np.exp(-np.pi * 1j * (FX[FTi]**2 + FY[FTi]**2) * dz / FT[FTi])
propag[FTni] = 0.
print("OK")
print("Copying propagation vector to GPU...", end="", flush=True)
propag = cp.asarray(propag,
                    dtype="complex64")
print("OK")

prog = tqdm(range(zlength))
prog.set_description("Propagating")
for i in prog:
    byfft *= propag
    v = cpx.scipy.fftpack.ifftn(byfft,
                                axes=(0,1,2))
    data.append(cp.real(v).get())
    del v

dirpath = get_path("", ["frames"])
if not os.path.exists(dirpath):
    os.mkdir(dirpath)

prog = tqdm(range(len(t)))
frame = np.empty(x.shape + y.shape + (zlength,))
for i in prog:
    prog.set_description("Building frames")
    for z in range(zlength):
        # We transpose the frame to put x and y axis back
        frame[:,:,z] = data[z][:,:,i].transpose()
    np.save(get_path("f%s.npy" % i, ["frames"]), frame)

print("done")
