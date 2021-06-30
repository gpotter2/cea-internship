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
)

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
)

CONFIG_HDR = """
###### CONFIG ######
# User configurable
self.MAX_INSTANT = %s
self.CLIP_HALF = False
""".strip() % (
    MAX_INSTANT,
)

def process(data):
    return HEADER + data

source = ProgrammableSource()
source.OutputDataSetType = 'vtkImageData'
with open(os.path.join(__DIR__, 'script.py')) as fd:
    source.Script = "\n".join([HEADER, fd.read()])
with open(os.path.join(__DIR__, 'reqscript.py')) as fd:
    source.ScriptRequestInformation = "\n".join([CONFIG_HDR, HEADER, fd.read()])
