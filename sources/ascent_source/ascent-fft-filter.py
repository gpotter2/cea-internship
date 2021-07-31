import conduit
import ascent.mpi
import cupy as cp
import cupyx as cpx
import numpy as np

try:
    count = count + 1
except NameError:
    count = 0

# Load data

# we treat everything as a multi_domain in ascent so grab child 0
n_mesh = ascent_data().child(0)
ascent_opts = conduit.Node()
ascent_opts['mpi_comm'].set(ascent_mpi_comm_id()) 
ascent_opts["actions_file"] = ""
    
#### DATA ####

a = ascent.mpi.Ascent()
a.open(ascent_opts)

# Process data
if count == 0:
    __DIR__ = "/home/gpotter/pv_work/sources/ascent_source/"
    
    import sys, os
    sys.path.append(os.path.join(__DIR__, "..", "..", "process_data"))

    #print(repr(n_mesh))
    field = "By"
    topo = n_mesh["fields/%s/topology" % field]
    coordset_name = n_mesh["topologies/%s/coordset" % topo]
    coordset = n_mesh["coordsets/%s" % coordset_name]

    from common import build_grid_params
    KX, KY, KZ = build_grid_params(
        coordset["dims/i"] - 1, coordset["spacing/dx"],
        coordset["dims/j"] - 1, coordset["spacing/dy"],
        coordset["dims/k"] - 1, coordset["spacing/dz"],
    )
    W = np.sqrt(KX**2 + KY**2 + KZ**2)
    print("Building propag...", end="", flush=True)
    L = np.max(W)
    propag_high = (W < 3*L//4).ravel()
    propag_low = (W > L//4).ravel()
    print("OK")

by = cp.asarray(n_mesh["fields/%s/values" % field],
                dtype="float64")
print(by)
print("  - Applying discrete fast fourier transform...", end="", flush=True)
byfft_high = cpx.scipy.fft.fftn(by,
                                axes=(0,1,2),
                                overwrite_x=True)
del by
print("OK")
byfft_low = cp.copy(byfft_high)
byfft_low[propag_low] = 0.
byfft_high[propag_high] = 0.
print("  - IFFT...", end="", flush=True)
byfft_high = cp.real(cpx.scipy.fft.ifftn(byfft_high,
                                         axes=(0,1,2),
                                         overwrite_x=True)).get()
byfft_low = cp.real(cpx.scipy.fft.ifftn(byfft_low,
                                        axes=(0,1,2),
                                        overwrite_x=True)).get()
print("OK")

print(np.max(byfft_low))
print(np.max(byfft_high))

def apply_log_scale(data, threshold):
    low = data < -threshold
    high = data > threshold
    mid = (data >= -threshold) & (data <= threshold)
    data[low] = -np.log10(-data[low])
    data[high] = np.log10(data[high])
    data[mid] = 0.

apply_log_scale(byfft_high, 1)
apply_log_scale(byfft_low, 1)

n_mesh["fields/By_h/association"] = "element"
n_mesh["fields/By_h/topology"] = topo
n_mesh["fields/By_h/values"].set_external(byfft_high)
del byfft_high
n_mesh["fields/By_l/association"] = "element"
n_mesh["fields/By_l/topology"] = topo
n_mesh["fields/By_l/values"].set_external(byfft_low)
del byfft_low

# Publish data
a.publish(n_mesh)

#### VISU ####

## Actions
actions = conduit.Node()

# Pipe into paraview

extract = actions.append()
extract["action"] = "add_extracts"
extract["extracts/e1/type"] = "python"
extract["extracts/e1/params/file"] = "/home/gpotter/pv_work/sources/ascent_source/ascent-paraview-insitu.py"

## Pipelines
#pipelines = conduit.Node()
#pipelines['pl1/f1/type'] = 'contour'
#pipelines['pl1/f1/params/field'] = 'By'
#pipelines['pl1/f1/params/levels'] = 5
#
## Scenes
#scenes  = conduit.Node()
#scenes['s1/plots/p1/type'] = 'volume'
#scenes['s1/plots/p1/pipeline'] = 'pl1'
#scenes['s1/plots/p1/field'] = 'By'
#scenes['s1/plots/p1/min_value'] = -2e4
#scenes['s1/plots/p1/max_value'] = 2e4
###
##scenes['s1/plots/p2/type'] = 'pseudocolor'
##scenes['s1/plots/p2/field'] = 'particle_electrons_ux'
##scenes['s1/plots/p2/points/radius'] = 0.0000005
##scenes['s1/plots/p2/min_value'] = 1e8
##scenes['s1/plots/p2/max_value'] = 1e8
#
#scenes['s1/renders/r1/image_width'] = 512
#scenes['s1/renders/r1/image_height'] = 512
#scenes['s1/renders/r1/image_prefix'] = 'out_render_3d_%06d'
#scenes['s1/renders/r1/camera/azimuth'] = 100
#scenes['s1/renders/r1/camera/elevation'] = 10
#
#add_act = actions.append()
#add_act['action'] = 'add_pipelines'
#add_act['pipelines'] = pipelines
#
#add_act = actions.append()
#add_act['action'] = 'add_scenes'
#add_act['scenes'] = scenes
#
#actions.append()['action'] = 'execute'

a.execute(actions)
a.close()
