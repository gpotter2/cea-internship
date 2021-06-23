# Config

import numpy as np

# Select mode

# PROPAGATION_TYPE = "z"
PROPAGATION_TYPE = "t"

MAX_INSTANT = 500  # How many instants we propagate

# How much we drop precision for the calculations
x_subsampling = 2
y_subsampling = 2

# How much we drop of precision for the visualisation.
# Note that there is already a /2 for X and Y before the calculus to make
# them fit on the GPU.
x_drop = 4
y_drop = 4

# PROPAGATION Z ONLY CONFIG
dz = -0.1  # How much we move between two z

# PROPAGATION T ONLY CONFIG
dt = 1  # How much we propagate between two instants
z_length = None  # Set to None for all points
z_drop = 1

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
