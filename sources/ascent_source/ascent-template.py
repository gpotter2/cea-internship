import conduit
import ascent.mpi

try:
    count = count + 1
except NameError:
    count = 0

# Load data

n_mesh = ascent_data()
acent_opts = conduit.Node()
ascent_opts['mpi_comm'].set(ascent_mpi_comm_id()) 
ascent_opts["actions_file"] = ""  # Do not loop

#### DATA ####

a = ascent.mpi.Ascent()
a.open(ascent_opts)
a.publish(n_mesh)

#### VISU ####

actions = conduit.Node()
pipelines = conduit.Node()

# Would be cool if the log filter supported positive-negative log.
# It doesn't so we build it ourselves above

# pipelines['pl1/f1/type'] = 'log'
# pipelines['pl1/f1/params/field'] = 'By_h'
# pipelines['pl1/f1/params/clamp_min_value'] = 0.1
# pipelines['pl1/f1/params/output_name'] = 'By_h_log'

pipelines['pl1/f2/type'] = 'contour'
pipelines['pl1/f2/params/field'] = 'By_h'  # 'By_h_log'
pipelines['pl1/f2/params/iso_values'] = 0.25

# pipelines['pl2/f1/type'] = 'log'
# pipelines['pl2/f1/params/field'] = 'By_l'
# pipelines['pl2/f1/params/clamp_min_value'] = 0.1
# pipelines['pl2/f1/params/output_name'] = 'By_l_log'

pipelines['pl2/f2/type'] = 'contour'
pipelines['pl2/f2/params/field'] = 'By_l'  # 'By_l_log'
pipelines['pl2/f2/params/iso_values'] = 0.3

# Scenes
scenes  = conduit.Node()
scenes['s1/plots/p1/type'] = 'pseudocolor'
scenes['s1/plots/p1/pipeline'] = 'pl1'
scenes['s1/plots/p1/field'] = 'By_h'  # By_h_log
scenes['s1/plots/p1/min_value'] = -4
scenes['s1/plots/p1/max_value'] = 4
#
scenes['s1/plots/p2/type'] = 'pseudocolor'
scenes['s1/plots/p2/pipeline'] = 'pl2'
scenes['s1/plots/p2/field'] = 'By_l'  # By_l_log
scenes["s1/plots/p2/color_table/name"] = "Blue to Orange"
scenes['s1/plots/p2/min_value'] = -4
scenes['s1/plots/p2/max_value'] = 4
#
scenes['s1/plots/p3/type'] = 'pseudocolor'
scenes['s1/plots/p3/field'] = 'particle_electrons_w'
scenes['s1/plots/p3/points/radius'] = 0.0000005

scenes['s1/renders/r1/image_width'] = 1024 # 512
scenes['s1/renders/r1/image_height'] = 1024 # 512
scenes['s1/renders/r1/image_prefix'] = 'outimg_%05d'
scenes['s1/renders/r1/camera/azimuth'] = 100
scenes['s1/renders/r1/camera/elevation'] = 10

add_act = actions.append()
add_act['action'] = 'add_pipelines'
add_act['pipelines'] = pipelines

add_act = actions.append()
add_act['action'] = 'add_scenes'
add_act['scenes'] = scenes

actions.append()['action'] = 'execute'

a.execute(actions)
a.close()
