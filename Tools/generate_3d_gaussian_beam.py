"""
Script to generate a 3D gaussian beam
"""

# Import other files
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "LocalPropagation")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "LocalPropagation", "process_data")))
from config import *
from common import build_grid, get_path

if not DEBUG_WITH_GAUSSIAN_BEAM:
    print("Cannot run this script with DEBUG_WITH_GAUSSIAN_BEAM to False !")
    sys.exit(1)

X, Y, Z = np.meshgrid(X_STEPS,
                      Y_STEPS,
                      Z_STEPS,
                      indexing="ij")

# Parameters
lmb = 3*1e8 * 1e-7
E0 = 1
w0 = 20
n = 1.2
print("W0/lmb: %s" % (w0 / lmb))

print("Generating beam.", end="", flush=True)
R = np.sqrt(X**2 + Y**2)
del X
del Y
print(".", end="", flush=True)

# See https://en.wikipedia.org/wiki/Gaussian_beam#Mathematical_form

Z[Z==0.] = 0.01
ZR = np.pi * w0**2 * n / lmb
k = 2 * np.pi * n / lmb
wz = w0 * np.sqrt(1 + (Z / ZR) ** 2)
print(".", end="", flush=True)
Rz = Z*( 1 + (ZR / Z)**2 )
print(".", end="", flush=True)
phiz = np.arctan(Z / ZR)
print(".", end="", flush=True)
byz = E0 * w0 / wz * np.exp(-R ** 2 / wz ** 2) * np.exp(-1j * (k*Z + k*R**2 / (2 * Rz) - phiz))
print(".", end="", flush=True)
del phiz, Rz, wz
byz = byz * np.exp(-np.abs(Z**2) / 10000)
print(".", end="", flush=True)
frame = np.real(byz)
print("OK")

print("Writing...", end="", flush=True)
np.save(get_path('GaussianBy.npy', "npy_files"), frame)
print("OK")
