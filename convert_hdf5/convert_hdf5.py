"""
Convert hdf5 to numpy
"""

import argparse
import os
import sys

try:
    import numpy as np
    import h5py
except ImportError as ex:
    print("######################\nMissing dependency !\n" + str(ex) + "\n######################")
    sys.exit(1)

# Read config
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config import (
    cnob,
    cnoe,
    x_subsampling,
    y_subsampling,
)

parser = argparse.ArgumentParser(description='Convert HDF5 to NPY')
parser.add_argument('src', type=str, nargs=1,
                    help='the file to convert')
parser.add_argument('dst', type=str, nargs=1,
                    help='the destination folder')
args = parser.parse_args()

with h5py.File(args.src[0]) as fd:
    print("Reading h5df file...")
    by = np.asarray(fd['By']) * cnob / cnoe
    x = np.asarray(fd['x'])/np.cos(np.pi/4)
    y = np.asarray(fd['y'])
    t = np.asarray(fd['t'])

print("Subsampling plane...")
by = by[::y_subsampling, ::x_subsampling, ::]
x = x[::x_subsampling]
y = y[::y_subsampling]

print("Writing numpy files...")

def get_path(name):
    return os.path.abspath(os.path.join(args.dst[0], name))

np.save(get_path("By"), by)
np.save(get_path("x"), x)
np.save(get_path("y"), y)
np.save(get_path("t"), t)

print("OK!")
