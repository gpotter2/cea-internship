# Config
zlength = -1  # Crop the current image to zlength in z. Negative for no cropping (big size)
MAX_TIME = 10  # How many instants we propagate
dz = -10  # How much we move on each instant

time_drop = 4  # How much we drop of time precision for the visualisation

STORAGE_FOLDER = "/mnt/scratch/gpotter/field3d"

# Constants (unused)
foc_pos = 56
antenna_from_foc = 10
initial_dz = antenna_from_foc - foc_pos
