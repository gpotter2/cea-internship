# Config

import os, sys
from itertools import permutations
import numpy as np

PROFILE = os.environ.get('PROPAGATE_PROFILE', 'default')

# Storage
# STORAGE_FOLDER = "/mnt/scratch/gpotter/field3d"
STORAGE_FOLDER = "/mnt/scratch/gpotter/bigfield3d"

########
# MODE #
########

DEBUG_WITH_GAUSSIAN_BEAM = False

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
x_subsampling = 4
y_subsampling = 4

SUBSAMPLE_IN_PROPAGATE = True

# How much we drop of precision for the visualisation.
# This is in addition of the precision drop for the calculations.
x_drop = 3
y_drop = 3
z_drop = 2

############
# CROPPING #
############

# Crop the space before propagating. You can use None to specify no cropping.
# THOSE VALUES MUST MATCH THE AXIS.

# CROP        = the size of the box.
# USABLE-CROP = the data that is used within the first frame. What isn't in the
#               USABLE CROP box will be set to 0.

# Default
x_min = None
x_max = None
y_min = None
y_max = None
# z_min = None
# z_max = None

# x_uc_min = None
# x_uc_max = None
# y_uc_min = None
# y_uc_max = None
z_uc_min = None
# z_uc_max = None

# Crop
# x_min = 1
# x_max = 15
# y_min = 1
# y_max = 14
z_min = 5
z_max = 18

# Usable-crop
# Crop
x_uc_min = 2
x_uc_max = 15
y_uc_min = 2
y_uc_max = 13
z_uc_max = 17
if PROFILE == "high":
    x_uc_max = 11

# Extra crop
def EXTRA_CROP(x):
    pass

############
# ROTATING #
############

ROTATION_ANGLE = None

#############
# FILTERING #
#############

FILTER_OUT_LOW_FREQ = 0.5

# Cone freq filtering. In degrees. Set None to disable
cone_angle = 60
# cone_angle = None

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

assert not DEBUG_WITH_GAUSSIAN_BEAM or PROPAGATION_TYPE == "t"
if DEBUG_WITH_GAUSSIAN_BEAM:
    print("### DEBUG WITH GAUSSIAN BEAM ###")
    XMAX = 200; XLENGTH = 200
    YMAX = 200; YLENGTH = 200
    ZMAX = 400; ZLENGTH = 800
    X_STEPS = np.linspace(-XMAX, XMAX, XLENGTH, dtype="float64")
    Y_STEPS = np.linspace(-YMAX, YMAX, YLENGTH, dtype="float64")
    Z_STEPS = np.linspace(-ZMAX, ZMAX, ZLENGTH, dtype="float64")
    SUBSAMPLE_IN_PROPAGATE = False
    T_OFFSET = 10
    dt = -0.5
    DATA_FORMAT = "XYZ"
    x_drop = None
    y_drop = None
    z_drop = None
    cone_angle = None
    FILTER_OUT_LOW_FREQ = None

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

if x_uc_min is not None:
    x_uc_min = int(x_uc_min / (X_STEPS[1] - X_STEPS[0]))
    assert x_uc_min >= (x_min or 0)
if x_uc_max is not None:
    x_uc_max = int(x_uc_max / (X_STEPS[1] - X_STEPS[0]))
    assert x_uc_max <= (x_max or float("inf"))
if y_uc_min is not None:
    y_uc_min = int(y_uc_min / (Y_STEPS[1] - Y_STEPS[0]))
    assert y_uc_min >= (y_min or 0)
if y_uc_max is not None:
    y_uc_max = int(y_uc_max / (Y_STEPS[1] - Y_STEPS[0]))
    assert y_uc_max <= (y_max or float("inf"))
if z_uc_min is not None:
    z_uc_min = int(z_uc_min / (Z_STEPS[1] - Z_STEPS[0]))
    assert z_uc_min >= (z_min or 0)
if z_uc_max is not None:
    z_uc_max = int(z_uc_max / (Z_STEPS[1] - Z_STEPS[0]))
    assert z_uc_max <= (z_max or float("inf"))

# Crop axis
if not DEBUG_WITH_GAUSSIAN_BEAM:
    X_STEPS = X_STEPS[x_min:x_max]
    Y_STEPS = Y_STEPS[y_min:y_max]
    if PROPAGATION_TYPE == "t":
        Z_STEPS = Z_STEPS[z_min:z_max]
    
