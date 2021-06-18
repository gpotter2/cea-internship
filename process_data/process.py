"""
Process the data:
    - read npy files
    - propagate files
    - generate frames
"""

import argparse
import os
import numpy as np
import cupy as cp
import cupyx as cpx

from tqdm import tqdm

# Read config
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config import (
    MAX_INSTANT,
    PROPAGATION_TYPE,
    STORAGE_FOLDER,
    dz,
    z_length,
    time_drop,
    x_drop,
    y_drop,
)

def get_path(x, folder=""):
    return os.path.abspath(os.path.join(STORAGE_FOLDER, folder, x))

parser = argparse.ArgumentParser(description='Process numpy files to create frames')
parser.add_argument('--filter-lowpass', type=float, nargs=1,
                    help='Applies a low-pass filter to a frequence')
parser.add_argument('--filter-highpass', type=float, nargs=1,
                    help='Applies a low-pass filter to a frequence')
args = parser.parse_args()

print("PROPAGATION TYPE: %s" % PROPAGATION_TYPE)
if args.filter_lowpass or args.filter_highpass:
    print("FILTER: %s, fc=%s" % (args.filter_lowpass and "lowpass" or "highpass",
                                (args.filter_lowpass or args.filter_highpass)[0]))

# Load files
print("Loading files...", end="", flush=True)
by = np.load(get_path('By.npy', "npy_files"))
x = np.load(get_path('x.npy', "npy_files"))
y = np.load(get_path('y.npy', "npy_files"))
t = np.load(get_path('t.npy', "npy_files"))
print("OK")

if PROPAGATION_TYPE == "z":
    third_axis_length = t.shape[0]
else:
    third_axis_length = z_length

# Apply discrete fourier transform
print("Moving data to GPU. Allocating array %sx%sx%s..." % by.shape, end="", flush=True)
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

print("Building propagation vector (slow).", end="", flush=True)
# See PROPAGATION_DEMO.md for explanation of this formula
propag = np.zeros(by.shape, dtype="complex64")
aFT = np.abs(FT)
FTi, FTni = (aFT > 0.01), (aFT <= 0.01)  # Do not try to divide by 0
# Check for filter
if args.filter_lowpass:
    fl = args.filter_lowpass[0]
    FTi = FTi & (aFT <= fl)
    FTni = FTni | (aFT > fl)
if args.filter_highpass:
    fl = args.filter_highpass[0]
    FTi = FTi & (aFT >= fl)
    FTni = FTni | (aFT < fl)
del aFT
# Do propag
if PROPAGATION_TYPE == "z":
    propag[FTi] = np.exp(-np.pi * 1j * (FX[FTi]**2 + FY[FTi]**2) * dz / FT[FTi])
elif PROPAGATION_TYPE == "t":
    propag[FTi] = np.exp(np.pi * 2j * FT[FTi] * (1 - 0.5 * (FX[FTi]**2 + FY[FTi]**2) / FT[FTi]**2) * dz)
print(".", end="", flush=True)
propag[FTni] = 0.
print("OK")
print("Copying propagation vector to GPU...", end="", flush=True)
propag = cp.asarray(propag,
                    dtype="complex64")
print("OK")

dirpath = get_path("", "frames")
if not os.path.exists(dirpath):
    os.mkdir(dirpath)

if PROPAGATION_TYPE == "z":
    prog = tqdm(range(MAX_INSTANT))
    prog.set_description("1/1 Propagating on z")
    for i in prog:
        byfft *= propag
        v = cpx.scipy.fftpack.ifftn(byfft,
                                    axes=(0,1,2))
        frame = cp.real(
            v[::y_drop, ::x_drop, :third_axis_length]
        ).transpose(1, 0, 2).get()
        np.savez(get_path("f%s.npz" % i, "frames"), frame=frame)
        del v
elif PROPAGATION_TYPE == "t":
    # First propagate on z
    prog = tqdm(range(third_axis_length))
    prog.set_description("1/2 Propagating on z")
    data = []
    for i in prog:
        byfft *= propag
        v = cpx.scipy.fftpack.ifftn(byfft,
                                    axes=(0,1,2))
        data.append(cp.real(
            v[::y_drop, ::x_drop, :]
        ).transpose(1, 0, 2).get())
        del v
    # Then build the frames on t
    prog = tqdm(range(data[0].shape[2]))
    frame = np.empty(data[0].shape[:2] + (third_axis_length,))
    for i in prog:
        prog.set_description("2/2 Building frames")
        for z in range(third_axis_length):
            # We transpose the frame to put x and y axis back
            frame[:,:,z] = data[z][:,:,i]
        np.savez(get_path("f%s.npz" % i, "frames"), frame=frame)

print("done")
