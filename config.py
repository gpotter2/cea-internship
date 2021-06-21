# Config

# Select mode

# PROPAGATION_TYPE = "z"
PROPAGATION_TYPE = "t"

MAX_INSTANT = 1000  # How many instants we propagate
dz = -1  # How much we move between two z

# How much we drop of precision for the visualisation.
# Note that there is already a /2 for X and Y before the calculus to make
# them fit on the GPU.
x_drop = 2
y_drop = 2

# PROPAGATION Z ONLY CONFIG

# PROPAGATION T ONLY CONFIG
z_length = 100

# Storage
STORAGE_FOLDER = "/mnt/scratch/gpotter/field3d"

# Constants (unused)
foc_pos = 56
antenna_from_foc = 10
initial_dz = antenna_from_foc - foc_pos

# Constants
c = 299792458 
me = 9.11e-31
mi = 1836. * me
e = 1.6e-19
kb = 1.38064852e-23
eps0 = 8.854187817620e-12
mu0 = 1.25663706e-6

# Experimental parameter
las_lambda = 0.8e-6
las_time = las_lambda / c
las_omega = 2 * np.pi / las_time

# Normalisation
cnoe = 1 / (me * las_omega * c / e)  # normalisation E --> unites a0
cnob = 1 / (me * las_omega / e)  # normalisation B --> unites a0

# --- End of config --- #
