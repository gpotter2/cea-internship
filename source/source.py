"""
A ProgramableSource object to read H5DF files into paraview
"""

# Config

PATH_TO_NPY = "/home/gpotter/pv_work/npy_files/"
PATH_TO_FRAMES = "/home/gpotter/pv_work/process_data/frames/"
ACTIVATE_THIS_ENV = "/home/gpotter/.miniconda3/bin/activate_this.py"

# https://docs.paraview.org/en/latest/ReferenceManual/pythonProgrammableFilter.html#programmable-filter

from paraview.simple import *
import sys, os
__DIR__ = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(__DIR__, ".."))

from config import (
    MAX_INSTANT,
    PROPAGATION_TYPE,
    STORAGE_FOLDER,
    TOT_Z,
    T_STEPS,
    X_STEPS,
    Y_STEPS,
    Z_LENGTH,
    Z_STEPS,
    cnob,
    cnoe,
    dt,
    dz,
    x_drop,
    y_drop,
    z_drop,
)

def getSource(CLIP_HALF=False,
              CLIP_QUARTER=False,
              CLIP_INV_QUARTER=False,
              LOG_SCALE=True,
              LOG_THRESHOLD=5e-5,
              SUFFIX="",
              COLOR="Cool to Warm (Extended)",
              OPACITY=1.0):
    ##################################
    ### CREATE PROGRAMMABLE SOURCE ###
    ##################################


    if len(list(x for x in [CLIP_HALF, CLIP_QUARTER, CLIP_INV_QUARTER] if x)) >= 2:
        raise ValueError("Cannot stack CLIPs !")

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
T_STEPS = %s
X_STEPS = %s
Y_STEPS = %s
Z_LENGTH = %s
Z_STEPS = %s
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
        T_STEPS,
        X_STEPS,
        Y_STEPS,
        Z_LENGTH,
        Z_STEPS,
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
self.CLIP_HALF = %s
self.CLIP_QUARTER = %s
self.CLIP_INV_QUARTER = %s
self.LOG_SCALE = %s
self.LOG_THRESHOLD = %s
self.SUFFIX = "%s"
    """.strip() % (
        MAX_INSTANT,
        CLIP_HALF,
        CLIP_QUARTER,
        CLIP_INV_QUARTER,
        LOG_SCALE,
        LOG_THRESHOLD,
        SUFFIX,
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
    
    displayProperties = Show(source)
    
    # Without log
    # clim = 0.0004
    # threshold = 7e-5
    
    # With log
    clim = 4
    threshold = 0.7
    
    # Color table
    byLUT = GetColorTransferFunction('By', displayProperties, separate=True)
    byLUT.ApplyPreset(COLOR)
    byLUT.RescaleTransferFunction([-clim, clim])
    byLUT.AutomaticRescaleRangeMode = 'Never'
    
    # Opacity map
    byPWF = GetOpacityTransferFunction('By', displayProperties, separate=True)
    byPWF.Points = [
        # format: val, opacity, 0.5, 0.0 (last 2?!)
        -clim,      OPACITY, 0.5, 0.0,
        -threshold, OPACITY, 0.5, 0.0,
        -threshold, 0.0, 0.5, 0.0,
        threshold,  0.0, 0.5, 0.0,
        threshold,  OPACITY, 0.5, 0.0,
        clim,       OPACITY, 0.5, 0.0,
    ]
    byPWF.ScalarRangeInitialized = 1
    
    # Display properties
    displayProperties.Representation = 'Volume'
    
    # Color
    displayProperties.ColorArrayName = 'By'
    displayProperties.LookupTable = byLUT
    
    # Opacity
    displayProperties.OpacityArrayName = 'By'
    displayProperties.ScalarOpacityFunction = byPWF

    # Separate color map
    displayProperties.UseSeparateColorMap = True

    return source
