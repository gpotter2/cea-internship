# Config
zlength = -1  # Crop the current image to zlength in z. Negative for no cropping (big size)
MAX_TIME = 1  # How many instants we propagate
dz = -5  # How much we move on each instant

t_drop = 4  # How much we drop of time precision for the visualisation

# Constants (unused)
foc_pos = 56
antenna_from_foc = 10
initial_dz = antenna_from_foc - foc_pos
