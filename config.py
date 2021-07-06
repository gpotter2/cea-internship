# Config

import numpy as np

# Storage
# STORAGE_FOLDER = "/mnt/scratch/gpotter/field3d"
STORAGE_FOLDER = "/mnt/scratch/gpotter/bigfield3d"

########
# MODE #
########

# PROPAGATION_TYPE = "z"
PROPAGATION_TYPE = "t"
MAX_INSTANT = 200  # How many instants we propagate

##############################
# INFORMATIONS ON INPUT DATA #
##############################

# Data config
# 102.4 x 102.4 x 94.5231 points per wavelength (wavelength: 800nm)
X_STEPS = np.linspace(0, 2072/102.4*8e-7, 2072)
Y_STEPS = np.linspace(0, 1500/102.4*8e-7, 1500)
T_STEPS = None
Z_STEPS = np.linspace(0, 1450/94.5231*8e-7, 1450)

#############################
# PROPAGATION Z ONLY CONFIG #
#############################

dz = -0.1  # How much we move between two z

#############################
# PROPAGATION T ONLY CONFIG #
#############################

dt = 0.5  # How much we propagate between two instants
TOT_Z = None  # The size of the frame. None for exactly the size of the wave
Z_LENGTH = 2000  # Set to None for all points

###############
# SUBSAMPLING #
###############

# How much we drop precision for the calculations. This is required
# if the data doesn't fit the GPU..
x_subsampling = 3
y_subsampling = 3

SUBSAMPLE_IN_PROPAGATE = True

# How much we drop of precision for the visualisation.
# This is in addition of the precision drop for the calculations.
x_drop = 2
y_drop = 2
z_drop = 2

########
# MISC #
########

# process_data/t_to_z.py
Z_OFFSET = 0

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

assert PROPAGATION_TYPE in ["t", "z"]

assert X_STEPS is not None
assert Y_STEPS is not None

if PROPAGATION_TYPE == "t":
    assert Z_STEPS is not None
elif PROPAGATION_TYPE == "z":
    assert T_STEPS is not None

if SUBSAMPLE_IN_PROPAGATE:
    X_STEPS = X_STEPS[::x_subsampling]
    Y_STEPS = Y_STEPS[::y_subsampling]
