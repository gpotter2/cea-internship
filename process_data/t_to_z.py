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

infos(by)

KY, KX, W = build_grid(x, y, t)
byfft = build_fft(by)

# Propagate
data = []
print("Building KZ (slow).", end="", flush=True)

propag = np.zeros(by.shape, dtype="complex64")

print(propag.nbytes)

# Create propag vector
KZ2 = W**2 - KX**2 - KY**2
KZ2[KZ2 < 0] = 0.
print(".", end="", flush=True)
KZ = np.sqrt(KZ2)

Z_LENGTH = Z_LENGTH or t.shape[0]
dz = TOT_Z / Z_LENGTH
print("OK")

print("Apply offset..", end="", flush=True)
propag_offset = np.exp(-np.pi * 2j * KZ * Z_OFFSET)
propag_offset[W < 0] = 0.  # Get rid of negative frequencies
print(".", end="", flush=True)

byfft *= cp.asarray(propag_offset, dtype="complex64")
del propag_offset
print("OK")

print("Building propag vector...")
propag = np.exp(-np.pi * 2j * KZ * dz)
propag[W < 0] = 0.  # Get rid of negative frequencies
print("OK")

print("Copying propagation vector to GPU...", end="", flush=True)
propag = cp.asarray(propag,
                    dtype="complex64")
print("OK")

# First propagate on z
prog = tqdm(range(Z_LENGTH))
prog.set_description("Building XYZ matrix")
frame = np.empty(byfft.shape[:2] + (Z_LENGTH,), dtype="float32")
for i in prog:
    byfft *= propag
    v = cpx.scipy.fft.ifftn(byfft,
                            axes=(0,1,2))
    frame[:,:,i] = cp.real(v)[:,:,0].get()
    del v

np.save(get_path("By_xyz.npy", "npy_files"), frame)

