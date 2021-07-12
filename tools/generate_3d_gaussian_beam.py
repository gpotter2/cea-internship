"""
Script to generate a 3D gaussian beam
"""

# Import other files
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "process_data")))
from config import *
from common import build_grid

if not DEBUG_WITH_GAUSSIAN_BEAM:
    print("Cannot run this script with DEBUG_WITH_GAUSSIAN_BEAM to False !")
    sys.exit(1)

X, Y, Z = build_grid(X_STEPS, Y_STEPS, Z_STEPS)

print("Generating beam...", end="", flush=True)
X0 = X[len(X)//2]
Y0 = Y[len(Y)//2]
R = np.sqrt((X - X0)**2 + (Y - Y0)**2)

dz = 1

Z[Z==0.] = 0.01
lmb = 3*1e8 * 1e-7
E0 = 1
w0 = 20
print("W0/lmb: %s" % (w0 / lmb))
ZR = np.pi*w0**2/lmb
k = 2*np.pi/lmb
wz = w0*np.sqrt(1+(Z / ZR)**2)
Rz = Z*(1+(ZR/Z)**2)
phiz = np.arctan(Z / ZR)
byz = E0*w0/wz*np.exp(-R**2/wz**2)*np.exp(-1j*(k*Z+k*R**2/(2*Rz)-phiz))
byz = byz*np.exp(-np.abs(Z**2)/10000)
frame = np.real(byz)
print("OK")

print("Writing...", end="", flush=True)
np.save(get_path('GaussianBy.npy', "npy_files"), frame)
print("OK")
