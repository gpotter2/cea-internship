"""
Util functions
"""

from paraview.simple import *

import sys, os, pickle
__DIR__ = os.path.abspath(os.path.dirname(__file__))

import config
from importlib import reload
reload(config)

from config import *

def getSourceRead(CLIP_HALF=False,
                  CLIP_QUARTER=False,
                  CLIP_INV_QUARTER=False,
                  LOG_SCALE=False,
                  LOG_THRESHOLD=5e-5,
                  SUFFIX="",
                  **kwargs):
    """
    Returns a programmable source that automatically imports image files.
    """
    # https://docs.paraview.org/en/latest/ReferenceManual/pythonProgrammableFilter.html#programmable-filter

    if len(list(x for x in [CLIP_HALF, CLIP_QUARTER, CLIP_INV_QUARTER] if x)) >= 2:
        raise ValueError("Cannot stack CLIPs !")

    HEADER = """
### GENERATED HEADER ###
import os, pickle

def get_path(x, folder=""):
    return os.path.abspath(os.path.join("%s", folder, x))

# Build-specific config
PROPAGATION_TYPE = "%s"
TOT_Z = %s
T_STEPS = %s
X_STEPS = pickle.loads(%s)
Y_STEPS = pickle.loads(%s)
Z_STEPS = pickle.loads(%s)
Z_LENGTH = %s
dt = %s
dz = %s
x_drop = %s
y_drop = %s
z_drop = %s
### END OF HEADER ###
    """.strip() % (
        STORAGE_FOLDER,
        #
        PROPAGATION_TYPE,
        TOT_Z,
        T_STEPS,
        pickle.dumps(X_STEPS),
        pickle.dumps(Y_STEPS),
        pickle.dumps(Z_STEPS),
        Z_LENGTH,
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
    
    source = ProgrammableSource(registrationName='AnimatedLaserBeam')
    source.OutputDataSetType = 'vtkImageData'
    with open(os.path.join(__DIR__, 'script_read.py')) as fd:
        source.Script = "\n".join([HEADER, fd.read()])
    with open(os.path.join(__DIR__, 'reqscript_read.py')) as fd:
        source.ScriptRequestInformation = "\n".join([CONFIG_HDR, HEADER, fd.read()])

    # Trigger RequestInformation
    source.UpdatePipelineInformation()
    
    paraview.simple._DisableFirstRenderCameraReset()

    setupView(animated=kwargs.pop("animated", None))
    showField(source, **kwargs)

    return source
