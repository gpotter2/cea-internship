import conduit
import ascent.mpi
try:
    import cupy as cp
    import cupyx as cpx
except ImportError:
    raise ImportError("Please install ``cupy`` !")
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

#print(repr(n_mesh))

def build_grid_params(xsize, xpad,
                      ysize, ypad,
                      zsize, zpad):
    print("Building freq grid...", end="", flush=True)
    # Build frequences grid
    freqx = np.fft.fftfreq(xsize, d=xpad)
    freqy = np.fft.fftfreq(ysize, d=ypad)
    freqz = np.fft.fftfreq(zsize, d=zpad)

    KX, KY, KZ = np.meshgrid(freqx, freqy, freqz, indexing='ij')
    print("OK")
    return KX, KY, KZ

# TODO: replace the FFT/IFFT that run on CPU with builtin WarpX when it's ready.

# Process data
if count == 0:
    field = "By"
    topo = n_mesh["fields/%s/topology" % field]
    coordset_name = n_mesh["topologies/%s/coordset" % topo]
    coordset = n_mesh["coordsets/%s" % coordset_name]

    KX, KY, KZ = build_grid_params(
        coordset["dims/i"] - 1, coordset["spacing/dx"],
        coordset["dims/j"] - 1, coordset["spacing/dy"],
        coordset["dims/k"] - 1, coordset["spacing/dz"],
    )
    W = np.sqrt(KX**2 + KY**2 + KZ**2)
    print("Building propag...", end="", flush=True)
    L = np.max(W)
    propag_high = (W < L//2).ravel()
    propag_low = (W > L//4).ravel()
    print("OK")

by = cp.asarray(n_mesh["fields/%s/values" % field],
                dtype="float64")
print("FFT...", end="", flush=True)
byfft_high = cpx.scipy.fft.fftn(by,
                                axes=(0,1,2),
                                overwrite_x=True)
del by  # free
print("OK")
byfft_low = cp.copy(byfft_high)
byfft_low[propag_low] = 0.
byfft_high[propag_high] = 0.
print("IFFT...", end="", flush=True)
byfft_high = cp.real(cpx.scipy.fft.ifftn(byfft_high,
                                         axes=(0,1,2),
                                         overwrite_x=True)).get()
byfft_low = cp.real(cpx.scipy.fft.ifftn(byfft_low,
                                        axes=(0,1,2),
                                        overwrite_x=True)).get()
print("OK")

def apply_log_scale(data, threshold):
    low = data < -threshold
    high = data > threshold
    mid = (data >= -threshold) & (data <= threshold)
    data[low] = -np.log10(-data[low])
    data[high] = np.log10(data[high])
    data[mid] = 0.

apply_log_scale(byfft_high, 0.5)
apply_log_scale(byfft_low, 0.5)

n_mesh["fields/By_h/association"] = "element"
n_mesh["fields/By_h/topology"] = topo
n_mesh["fields/By_h/values"].set_external(byfft_high)
n_mesh["fields/By_l/association"] = "element"
n_mesh["fields/By_l/topology"] = topo
n_mesh["fields/By_l/values"].set_external(byfft_low)

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

## Ascent Pipelines
#pipelines = conduit.Node()
#
## Would be cool if the log filter supported positive-negative log.
## It doesn't so we build it ourselves above
#
##pipelines['pl1/f1/type'] = 'log'
##pipelines['pl1/f1/params/field'] = 'By_h'
##pipelines['pl1/f1/params/clamp_min_value'] = 0.1
##pipelines['pl1/f1/params/output_name'] = 'By_h_log'
#
#pipelines['pl1/f2/type'] = 'contour'
#pipelines['pl1/f2/params/field'] = 'By_h'  # 'By_h_log'
#pipelines['pl1/f2/params/iso_values'] = 0.25
##
##pipelines['pl2/f1/type'] = 'log'
##pipelines['pl2/f1/params/field'] = 'By_l'
##pipelines['pl2/f1/params/clamp_min_value'] = 0.1
##pipelines['pl2/f1/params/output_name'] = 'By_l_log'
#
#pipelines['pl2/f2/type'] = 'contour'
#pipelines['pl2/f2/params/field'] = 'By_l'  # 'By_l_log'
#pipelines['pl2/f2/params/iso_values'] = 0.3
#
## Scenes
#scenes  = conduit.Node()
#scenes['s1/plots/p1/type'] = 'pseudocolor'
#scenes['s1/plots/p1/pipeline'] = 'pl1'
#scenes['s1/plots/p1/field'] = 'By_h'  # By_h_log
#scenes['s1/plots/p1/min_value'] = -4
#scenes['s1/plots/p1/max_value'] = 4
##
#scenes['s1/plots/p2/type'] = 'pseudocolor'
#scenes['s1/plots/p2/pipeline'] = 'pl2'
#scenes['s1/plots/p2/field'] = 'By_l'  # By_l_log
#scenes["s1/plots/p2/color_table/name"] = "Blue to Orange"
#scenes['s1/plots/p2/min_value'] = -4
#scenes['s1/plots/p2/max_value'] = 4
##
#scenes['s1/plots/p3/type'] = 'pseudocolor'
#scenes['s1/plots/p3/field'] = 'particle_electrons_ux'
#scenes['s1/plots/p3/points/radius'] = 0.0000005
#
#scenes['s1/renders/r1/image_width'] = 1024 # 512
#scenes['s1/renders/r1/image_height'] = 1024 # 512
#scenes['s1/renders/r1/image_prefix'] = 'outimg_%05d'
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

actions.append()['action'] = 'execute'

a.execute(actions)
a.close()
