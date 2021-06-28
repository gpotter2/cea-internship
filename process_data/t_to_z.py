"""
Convert a X,Y,T grid to a X,Y,Z grid
"""

from common import *

print("""
 __   ____     _________       __    __   ____     ________
 \ \ / /\ \   / /__   __|      \ \   \ \ / /\ \   / /___  /
  \ V /  \ \_/ /   | |     _____\ \   \ V /  \ \_/ /   / /
   > <    \   /    | |    |______> >   > <    \   /   / /
  / . \    | |     | |          / /   / . \    | |   / /
 /_/ \_\   |_|     |_|         /_/   /_/ \_\   |_|  /_____|
------------------------------------------------------------
""")

# Load files
print("Loading files...", end="", flush=True)
by = np.load(get_path('By.npy', "npy_files"))
x = np.load(get_path('x.npy', "npy_files"))
y = np.load(get_path('y.npy', "npy_files"))
t = np.load(get_path('t.npy', "npy_files"))
print("OK")

KY, KX, W, byfft = build_fft(x, y, t, by)

# Propagate
data = []
print("Building propagation vector (slow).", end="", flush=True)

propag = np.zeros(by.shape, dtype="complex64")

# Create propag vector
KZ2 = W**2 - KX**2 - KY**2
KZ2[KZ2 < 0] = 0.
KZ = np.sqrt(KZ2)

Z_LENGTH = Z_LENGTH or t.shape[0]
dz = TOT_Z / Z_LENGTH

print(".", end="", flush=True)
# See PROPAGATION_DEMO.md for explanation of this formula
propag = np.exp(-np.pi * 2j * KZ * dz)
propag[W < 0] = 0.  # Get rid of negative frequencies
print(".", end="", flush=True)
print("OK")

print("Copying propagation vector to GPU...", end="", flush=True)
propag = cp.asarray(propag,
                    dtype="complex64")
print("OK")

# First propagate on z
prog = tqdm(range(Z_LENGTH))
prog.set_description("Building XYZ matrix")
frame = np.empty(byfft.shape)
for i in prog:
    byfft *= propag
    v = cpx.scipy.fft.ifftn(byfft,
                            axes=(0,1,2))
    frame[:,:,i] = cp.real(v)[:,:,0].get()
    del v

np.save(get_path("By_xyz.npy", "npy_files"), frame)

