"""
Convert hdf5 to numpy
"""

import argparse
import os
import sys

try:
    import numpy as np
    import h5py
    import evtk
except ImportError as ex:
    print("######################\nMissing dependency !\n" + str(ex) + "\n######################")
    sys.exit(1)

parser = argparse.ArgumentParser(description='Convert HDF5 to NPY')
parser.add_argument('src', type=str, nargs=1,
                    help='the file to convert')
parser.add_argument('dst', type=str, nargs=1,
                    help='the destination folder')
args = parser.parse_args()

with h5py.File(args.src[0]) as fd:
    print("Reading h5df file...")
    by = np.asarray(fd['By'], dtype='float32')
    x = np.asarray(fd['x'])/np.cos(np.pi/4)
    y = np.asarray(fd['y'])
    t = np.asarray(fd['t'])

print("Writing numpy files...")

def get_path(name):
    return os.path.abspath(os.path.join(args.dst[0], name))

np.save(get_path("By"), by)
np.save(get_path("x"), x)
np.save(get_path("y"), y)
np.save(get_path("t"), t)

print("OK!")
