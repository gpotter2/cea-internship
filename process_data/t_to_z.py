"""
Convert a X,Y,T grid to a X,Y,Z grid
"""

from common import *

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
byfft[KZ2 < 0] = 0.
KZ2[KZ2 < 0] = 0.

# ns = pln_matrix(byfft)
print(".", end="", flush=True)
# See PROPAGATION_DEMO.md for explanation of this formula
dz = t[1] - t[0]
propag = np.exp(-np.pi * 2j * np.sqrt(KZ2) * dz)
propag[W > 1.2] = 0
print(".", end="", flush=True)
print("OK")

print("Copying propagation vector to GPU...", end="", flush=True)
propag = cp.asarray(propag,
                    dtype="complex64")
print("OK")

# First propagate on z
prog = tqdm(range(t.shape[0]))
prog.set_description("Building XYZ matrix")
frame = np.empty(byfft.shape)
for i in prog:
    byfft *= propag
    v = cpx.scipy.fft.ifftn(byfft,
                            axes=(0,1,2))
    frame[:,:,t.shape[0] - 1 - i] = cp.real(v)[:,:,0].get()
    del v

np.save(get_path("By_xyz.npy", "npy_files"), frame)

