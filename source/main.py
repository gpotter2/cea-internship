"""
A ProgramableSource object to read H5DF files into paraview
"""

# Config

PATH_TO_NPY = "/home/gpotter/pv_work/npy_files/"
PATH_TO_FRAMES = "/home/gpotter/pv_work/process_data/frames/"
ACTIVATE_THIS_ENV = "/home/gpotter/.miniconda3/bin/activate_this.py"

# https://docs.paraview.org/en/latest/ReferenceManual/pythonProgrammableFilter.html#programmable-filter

from paraview.simple import *
import os
__DIR__ = os.path.abspath(os.path.dirname(__file__))

# Read config
import sys, os
sys.path.append(os.path.join(__DIR__, ".."))
from config import (
    MAX_INSTANT,
    PROPAGATION_TYPE,
    STORAGE_FOLDER,
    TOT_Z,
    Z_LENGTH,
    cnob,
    cnoe,
    dt,
    dz,
    x_drop,
    y_drop,
    z_drop,
)

##################################
### CREATE PROGRAMMABLE SOURCE ###
##################################

HEADER = """
### GENERATED HEADER ###
import os
activate_this="%s"
exec(open(activate_this).read(), dict(__file__=activate_this))

def get_path(x, folder=""):
    return os.path.abspath(os.path.join("%s", folder, x))

# Build-specific config
PROPAGATION_TYPE = "%s"
TOT_Z = %s
Z_LENGTH = %s
cnob = %s
cnoe = %s
dt = %s
dz = %s
x_drop = %s
y_drop = %s
z_drop = %s
### END OF HEADER ###
""".strip() % (
    ACTIVATE_THIS_ENV,
    STORAGE_FOLDER,
    #
    PROPAGATION_TYPE,
    TOT_Z,
    Z_LENGTH,
    cnob,
    cnoe,
    dt,
    dz,
    x_drop,
    y_drop,
    z_drop,
)

CONFIG_HDR = """
###### CONFIG ######
# User configurable
self.MAX_INSTANT = %s
self.CLIP_HALF = False
self.LOG_SCALE = True
self.LOG_THRESHOLD = 5e-5
""".strip() % (
    MAX_INSTANT,
)

def process(data):
    return HEADER + data

source = ProgrammableSource(registrationName='AnimatedLaserBeam')
source.OutputDataSetType = 'vtkImageData'
with open(os.path.join(__DIR__, 'script.py')) as fd:
    source.Script = "\n".join([HEADER, fd.read()])
with open(os.path.join(__DIR__, 'reqscript.py')) as fd:
    source.ScriptRequestInformation = "\n".join([CONFIG_HDR, HEADER, fd.read()])

########################
### CONFIGURE RENDER ###
########################

# Trigger RequestInformation
source.UpdatePipelineInformation()

Show()

clim = 0.0004
threshold = 7e-5

# Color table
byLUT = GetColorTransferFunction('By')
byLUT.ApplyPreset("Cool to Warm (Extended)")
byLUT.RescaleTransferFunction([-clim, clim])
byLUT.AutomaticRescaleRangeMode = 'Never'

# Opacity map
byPWF = GetOpacityTransferFunction('By')
byPWF.Points = [
    # format: val, opacity, 0.5, 0.0 (last 2?!)
    -clim,      1.0, 0.5, 0.0,
    -threshold, 1.0, 0.5, 0.0,
    -threshold, 0.0, 0.5, 0.0,
    threshold,  0.0, 0.5, 0.0,
    threshold,  1.0, 0.5, 0.0,
    clim,       1.0, 0.5, 0.0,
]
byPWF.ScalarRangeInitialized = 1

# Display properties
displayProperties = GetDisplayProperties(source)
displayProperties.Representation = 'Volume'

# Color
displayProperties.ColorArrayName = 'By'
displayProperties.LookupTable = byLUT

# Opacity
displayProperties.OpacityArrayName = 'By'
displayProperties.ScalarOpacityFunction = byPWF

Render()
