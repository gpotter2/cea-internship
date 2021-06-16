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
    MAX_TIME,
    STORAGE_FOLDER,
    dz,
    time_drop,
    x_drop,
    y_drop,
    zlength,
)

HEADER = """
### GENERATED HEADER ###
import os
activate_this="%s"
exec(open(activate_this).read(), dict(__file__=activate_this))

def get_path(x, folder=""):
    return os.path.abspath(os.path.join("%s", folder, x))

dz = %s
zlength = %s
MAX_TIME = %s
x_drop = %s
y_drop = %s
time_drop = %s

### END OF HEADER ###

""" % (
    ACTIVATE_THIS_ENV,
    STORAGE_FOLDER,
    dz,
    zlength,
    MAX_TIME,
    x_drop,
    y_drop,
    time_drop
)

def process(data):
    return HEADER + data

source = ProgrammableSource()
source.OutputDataSetType = 'vtkImageData'
with open(os.path.join(__DIR__, 'script.py')) as fd:
    source.Script = process(fd.read())
with open(os.path.join(__DIR__, 'reqscript.py')) as fd:
    source.ScriptRequestInformation = process(fd.read())
