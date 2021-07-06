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
X_STEPS = np.linspace(0, 2072/102.4, 2072)
Y_STEPS = np.linspace(0, 1500/102.4, 1500)
T_STEPS = None
Z_STEPS = np.linspace(0, 1450/94.5231, 1450)

DATA_FORMAT = "XYZ"  # XYZ, YXZ, XYT

#############################
# PROPAGATION Z ONLY CONFIG #
#############################

dz = -0.1  # How much we move between two z

#############################
# PROPAGATION T ONLY CONFIG #
#############################

dt = 0 #0.5  # How much we propagate between two instants
TOT_Z = None  # The size of the frame. None for exactly the size of the wave
Z_LENGTH = None  # Set to None for all points

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
x_drop = 4
y_drop = 4
z_drop = 2

########
# MISC #
########

# process_data/t_to_z.py
Z_OFFSET = 0

# --- End of config --- #

assert PROPAGATION_TYPE in ["t", "z"]

assert X_STEPS is not None
assert Y_STEPS is not None

if PROPAGATION_TYPE == "t":
    assert Z_STEPS is not None
    assert DATA_FORMAT in ["XYZ", "YXZ"]
elif PROPAGATION_TYPE == "z":
    assert T_STEPS is not None
    assert DATA_FORMAT == "XYT"

if SUBSAMPLE_IN_PROPAGATE:
    X_STEPS = X_STEPS[::x_subsampling]
    Y_STEPS = Y_STEPS[::y_subsampling]
