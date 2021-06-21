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
    cnob,
    cnoe,
    dz,
    c,
    x_drop,
    x_subsampling,
    y_drop,
    y_subsampling,
    z_length,
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

# Apply discrete fourier transform
print("Moving data to GPU. Allocating array %sx%sx%s..." % by.shape, end="", flush=True)
byfft = cp.asarray(by, dtype="complex64") * cnob / cnoe
print("OK")

# FW
print("Applying discrete fast fourier transform...", end="", flush=True)
cpx.scipy.fft.fftn(byfft,
                   axes=(0,1,2),
                   norm="forward",
                   overwrite_x=True)
print("OK")

def build_freq_grid(x, y, t):
    print("Building freq grid...", end="", flush=True)
    # Build frequences grid
    freqx = np.fft.fftfreq(x.size, d=x[1] - x[0])
    freqy = np.fft.fftfreq(y.size, d=y[1] - y[0])
    freqt = np.fft.fftfreq(t.size, d=t[1] - t[0])
    print("OK")
    return np.meshgrid(freqy, freqx, freqt, indexing='ij')

KY, KX, W = build_freq_grid(x, y, t)

data = []

# Propagate

print("Building propagation vector (slow).", end="", flush=True)
# See PROPAGATION_DEMO.md for explanation of this formula
propag = np.zeros(by.shape, dtype="complex64")
aW = np.abs(W)
Wi, Wni = (aW > 0.01), (aW <= 0.01)  # Do not try to divide by 0
# Check for filter
if args.filter_lowpass:
    fl = args.filter_lowpass[0]
    Wi = Wi & (aW <= fl)
    Wni = Wni | (aW > fl)
if args.filter_highpass:
    fl = args.filter_highpass[0]
    Wi = Wi & (aW >= fl)
    Wni = Wni | (aW < fl)
del aW
# Create propag vector
if PROPAGATION_TYPE == "z":
    propag[Wi] = np.exp(-np.pi * 1j * (KX[Wi]**2 + KY[Wi]**2) * dz / W[Wi])
    propag[Wni] = 0.
elif PROPAGATION_TYPE == "t":
    KZ2 = abs(W**2 - KX**2 - KY**2)
    KZ2[KZ2 < 0] = 0.
    ns = np.zeros(byfft.shape)
    for i in range(0, t.shape[0]):
        ns[:,:,i] = np.ones(byfft.shape[:2]) * i
    print(ns)
    print(".", end="", flush=True)
    propag = np.exp(-np.pi * 2j * np.sqrt(KZ2) * ns / t.shape[0] * dz)
print(".", end="", flush=True)
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
            v[::y_drop, ::x_drop, :t.shape[0]]
        ).transpose(1, 0, 2).get()
        np.savez(get_path("f%s.npz" % i, "frames"), frame=frame)
        del v
elif PROPAGATION_TYPE == "t":
    # First propagate on z
    prog = tqdm(range(z_length))
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
    # Then build the frames
    frame = np.empty(data[0].shape[:2] + (z_length,))
    prog = tqdm(range(data[0].shape[2]))
    prog.set_description("2/2 Building frames")
    for i in prog:
        for z in range(z_length):
            frame[:,:,z] = data[z_length - 1 - z][:,:,i]
        np.savez(get_path("f%s.npz" % i, "frames"), frame=frame)

print("done")
