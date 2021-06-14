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
    return os.path.abspath(*([os.path.join(os.path.dirname(__file__)] + path + [x])))

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
# See PROPAGATION_DEMO.md for explanation of this formula
propag = cp.asarray(np.exp(-np.pi * 1j * (FX**2 + FY**2) * dz / FT),
                    dtype="complex64")
print("OK")
prog = tqdm(range(zlength))
prog.set_description("Propagating")
for i in prog:
    byfft *= propag
    v = cpx.scipy.fftpack.ifftn(cp.asarray(byfft),
                                axes=(0,1,2))
    data.append(np.real(v.get()))
    del v

dirpath = get_path("", ["frames"])
if not os.path.exists(dirpath):
    os.mkdir(dirpath)

prog = tqdm(range(len(t)))
frame = np.empty(y.shape + x.shape + (zlength,))
for i in prog:
    prog.set_description("Building frame")
    for z in range(zlength):
        frame[:,:,z] = data[z][:,:,i]
    prog.set_description("Dumping")
    frame.dump(get_path("f%s.npy" % i, ["frames"]))

print("done")
