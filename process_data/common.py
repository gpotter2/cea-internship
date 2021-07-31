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

# Read config
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config import *

def get_path(x, folder=""):
    return os.path.abspath(os.path.join(STORAGE_FOLDER, folder, x))

def build_grid_params(xsize, xpad,
                      ysize, ypad,
                      zsize, zpad):
    print("Building freq grid...", end="", flush=True)
    # Build frequences grid
    freqx = np.fft.fftfreq(xsize, d=xpad)
    freqy = np.fft.fftfreq(ysize, d=ypad)
    freqz = np.fft.fftfreq(zsize, d=zpad)

    KX, KY, KZ = np.meshgrid(freqx, freqy, freqz, indexing='ij')
    print("OK")
    return KX, KY, KZ


def build_grid(x, y, z):
    return build_grid_params(
        x.size, x[1] - x[0],
        y.size, y[1] - y[0],
        z.size, z[1] - z[0],
    )


def infos(by):
    if X_STEPS.shape[0] != by.shape[0]:
        print("ERROR: X_STEPS dimension != By X dimension")
        print(X_STEPS.shape, by.shape)
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
    byfft_size = by.shape[0] * by.shape[1] * (Z_LENGTH or by.shape[2]) * 8
    estimated_gpu = byfft_size * 4
    print("Estimated max GPU usage: %.3gGB" % (estimated_gpu / 1e9))
    if estimated_gpu > 32 * 1e9:
        print("WARNING - GPU size likely exceeded. propagate might not work !")
