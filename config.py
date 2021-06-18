# Config

# Select mode

# PROPAGATION_TYPE = "z"
PROPAGATION_TYPE = "t"

MAX_INSTANT = 100  # How many instants we propagate
dz = -1  # How much we move between two z

# How much we drop of precision for the visualisation.
# Note that there is already a /2 for X and Y before the calculus to make
# them fit on the GPU.
x_drop = 2
y_drop = 2

# PROPAGATION Z ONLY CONFIG
time_drop = 8  # Only used when propagating on z

# PROPAGATION T ONLY CONFIG
z_length = 100


STORAGE_FOLDER = "/mnt/scratch/gpotter/field3d"

# Constants (unused)
foc_pos = 56
antenna_from_foc = 10
initial_dz = antenna_from_foc - foc_pos
