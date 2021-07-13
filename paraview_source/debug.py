"""
File to run when using the Paraview GUI
"""

import sys, os
__DIR__ = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(__DIR__))
sys.path.append(os.path.join(__DIR__, ".."))

import source
from importlib import reload
reload(source)

from config import DEBUG_WITH_GAUSSIAN_BEAM
if not DEBUG_WITH_GAUSSIAN_BEAM:
    print("Debug mode is not enabled ! Arborting")
else:
    from source import getSource
    getSource(LOG_SCALE=True, LOG_THRESHOLD=4e-04,
              THRESHOLD=0.1,
              CLIM=4.3)
