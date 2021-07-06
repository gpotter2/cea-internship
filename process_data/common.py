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
    SUBSAMPLE_IN_PROPAGATE,
    TOT_Z,
    T_STEPS,
    X_STEPS,
    Y_STEPS,
    Z_LENGTH,
    Z_OFFSET,
    Z_STEPS,
    c,
    dt,
    dz,
    x_drop,
    x_subsampling,
    y_drop,
    y_subsampling,
    z_drop,
)

def get_path(x, folder=""):
    return os.path.abspath(os.path.join(STORAGE_FOLDER, folder, x))

def build_fft(by):
    # Apply discrete fourier transform
    print("Moving data to GPU. Allocating array %sx%sx%s..." % by.shape, end="", flush=True)
    byfft = cp.asarray(by, dtype="complex64")
    print("OK")
    # FW
    print("Applying discrete fast fourier transform...", end="", flush=True)
    cpx.scipy.fft.fftn(byfft,
                       axes=(0,1,2),
                       norm="forward",
                       overwrite_x=True)
    print("OK")
    return byfft

def build_grid(x, y, t):
    print("Building freq grid...", end="", flush=True)
    # Build frequences grid
    freqx = np.fft.fftfreq(x.size, d=x[1] - x[0])
    freqy = np.fft.fftfreq(y.size, d=y[1] - y[0])
    freqt = np.fft.fftfreq(t.size, d=t[1] - t[0])

    KY, KX, W = np.meshgrid(freqy, freqx, freqt, indexing='ij')
    print("OK")
    return KY, KX, W

def infos(by):
    if X_STEPS.shape[0] != by.shape[0]:
        print("ERROR: X_STEPS dimension != By X dimension")
        sys.exit(1)
    if Y_STEPS.shape[0] != by.shape[1]:
        print("ERROR: Y_STEPS dimension != By Y dimension")
        sys.exit(1)
    if PROPAGATION_TYPE == "z" and T_STEPS.shape[0] != by.shape[2]:
        print("ERROR: T_STEPS dimension != By T dimension")
        sys.exit(1)
    elif PROPAGATION_TYPE == "t" and Z_STEPS.shape[0] != by.shape[2]:
        print("ERROR: Z_STEPS dimension != By Z dimension")
        sys.exit(1)
    print("Input grid size: %sx%sx%s (~%sGB)" % (by.shape + (by.nbytes / 1e9,)))
    byfft_size = by.shape[0] * by.shape[1] * Z_LENGTH * 8
    estimated_gpu = byfft_size * 4
    print("Estimated max GPU usage: %.3gGB" % (estimated_gpu / 1e9))
    if estimated_gpu > 32 * 1e9:
        print("WARNING - GPU size likely exceeded. propagate might not work !")
