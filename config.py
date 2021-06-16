# Config
zlength = -1  # Crop the current image to zlength in z. Negative for no cropping (big size)
MAX_TIME = 10  # How many instants we propagate
dz = -10  # How much we move on each instant

# How much we drop of precision for the visualisation.
# Note that there is already a /2 for X and Y before the calculus to make
# them fit on the GPU.
x_drop = 2
y_drop = 2
time_drop = 8

STORAGE_FOLDER = "/mnt/scratch/gpotter/field3d"

# Constants (unused)
foc_pos = 56
antenna_from_foc = 10
initial_dz = antenna_from_foc - foc_pos
