# Config

from itertools import permutations
import numpy as np

# Storage
# STORAGE_FOLDER = "/mnt/scratch/gpotter/field3d"
STORAGE_FOLDER = "/mnt/scratch/gpotter/bigfield3d"

########
# MODE #
########

# PROPAGATION_TYPE = "z"
PROPAGATION_TYPE = "t"
MAX_INSTANT = 250  # How many instants we propagate

##############################
# INFORMATIONS ON INPUT DATA #
##############################

# Data config
# 102.4 x 102.4 x 94.5231 points per wavelength (wavelength: 800nm)
Z_STEPS = np.linspace(0, 2072/102.4, 2072)
Y_STEPS = np.linspace(0, 1500/102.4, 1500)
X_STEPS = np.linspace(0, 1450/94.5231, 1450)
T_STEPS = None

# Data format: XYT for z propag, any permutation of XYZ for t propag
DATA_FORMAT = "ZYX"

#############################
# PROPAGATION Z ONLY CONFIG #
#############################

dz = -0.1  # How much we move between two z

#############################
# PROPAGATION T ONLY CONFIG #
#############################

dt = -0.1  # How much we propagate between two instants
T_OFFSET = 10  # Begin with a time offset of T_OFFSET

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

############
# CROPPING #
############

# Crop the space before propagating. You can use None to specify no cropping.
# THOSE VALUES MUST MATCH THE AXIS

# Default
x_min = None
x_max = None
y_min = None
y_max = None
z_min = None
z_max = None

# Crop
x_min = 2
x_max = 15
y_min = 2
y_max = 13
z_min = 5
z_max = 18

############
# ROTATING #
############

ROTATION_ANGLE = None

#############
# FILTERING #
#############

FILTER_OUT_LOW_FREQ = 0.5

########
# MISC #
########

# process_data/t_to_z.py
Z_OFFSET = 0

# --- End of config --- #

# Various sanity checks
assert PROPAGATION_TYPE in ["t", "z"]

assert X_STEPS is not None
assert Y_STEPS is not None

if PROPAGATION_TYPE == "t":
    assert Z_STEPS is not None
    assert DATA_FORMAT in list("".join(x) for x in permutations("XYZ"))
elif PROPAGATION_TYPE == "z":
    assert T_STEPS is not None
    assert DATA_FORMAT == "XYT"
    assert z_min is None
    assert z_max is None
    assert T_OFFSET == 0.

# Apply subsampling
if SUBSAMPLE_IN_PROPAGATE:
    X_STEPS = X_STEPS[::x_subsampling]
    Y_STEPS = Y_STEPS[::y_subsampling]

# Re-scale cropping values
if x_min is not None:
    x_min = int(x_min / (X_STEPS[1] - X_STEPS[0]))
if x_max is not None:
    x_max = int(x_max / (X_STEPS[1] - X_STEPS[0]))
if y_min is not None:
    y_min = int(y_min / (Y_STEPS[1] - Y_STEPS[0]))
if y_max is not None:
    y_max = int(y_max / (Y_STEPS[1] - Y_STEPS[0]))
if z_min is not None:
    z_min = int(z_min / (Z_STEPS[1] - Z_STEPS[0]))
if z_max is not None:
    z_max = int(z_max / (Z_STEPS[1] - Z_STEPS[0]))

# Crop axis
X_STEPS = X_STEPS[x_min:x_max]
Y_STEPS = Y_STEPS[y_min:y_max]
if PROPAGATION_TYPE == "t":
    Z_STEPS = Z_STEPS[z_min:z_max]

