"""
Process the data:
    - read npy files
    - propagate files
    - generate frames
"""

import os
import numpy as np
import cupy as cp
import cupyx as cpx

from tqdm import tqdm

# Read config
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config import (
    MAX_TIME,
    STORAGE_FOLDER,
    dz,
    x_drop,
    y_drop,
    time_drop,
    zlength,
)

def get_path(x, folder=""):
    return os.path.abspath(os.path.join(STORAGE_FOLDER, folder, x))

parser = argparse.ArgumentParser(description='Process numpy files to create frames')
parser.add_argument('--filter-lowpass', type=float, nargs=1,
                    help='Applies a low-pass filter to a frequence')
parser.add_argument('--filter-highpass', type=str, nargs=1,
                    help='Applies a low-pass filter to a frequence')
args = parser.parse_args()

# Load files
print("Loading files...", end="", flush=True)
by = np.load(get_path('By.npy', "npy_files"))
x = np.load(get_path('x.npy', "npy_files"))
y = np.load(get_path('y.npy', "npy_files"))
t = np.load(get_path('t.npy', "npy_files"))
print("OK")

zlength = t.shape[0] if zlength < 0 else zlength

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
aFT = np.abs(FT)
FTi, FTni = (aFT > 0.01), (aFT <= 0.01)  # Do not try to divide by 0
# Check for filter
if args.filter_lowpass:
    print("- Applying Lowpass W<%s" % args.filter_lowpass)
    FTi = FTi & (aFT <= args.filter_lowpass)
    FTni = FTni | (aFT > args.filter_lowpass)
if args.filter_highpass:
    print("- Applying Highpass W>%s" % args.filter_highpass)
    FTi = FTi & (aFT >= args.filter_highpass)
    FTni = FTni | (aFT < args.filter_highpass)
del aFT
# Do propag
propag[FTi] = np.exp(-np.pi * 1j * (FX[FTi]**2 + FY[FTi]**2) * dz / FT[FTi])
propag[FTni] = 0.
print("OK")
print("Copying propagation vector to GPU...", end="", flush=True)
propag = cp.asarray(propag,
                    dtype="complex64")
print("OK")

dirpath = get_path("", "frames")
if not os.path.exists(dirpath):
    os.mkdir(dirpath)

prog = tqdm(range(MAX_TIME))
prog.set_description("Propagating")
for i in prog:
    byfft *= propag
    v = cpx.scipy.fftpack.ifftn(byfft,
                                axes=(0,1,2))
    frame = cp.real(
        v[::y_drop, ::x_drop, :zlength:time_drop]
    ).transpose(1, 0, 2).get()
    np.savez(get_path("f%s.npz" % i, "frames"), frame=frame)
    del v

print("done")
