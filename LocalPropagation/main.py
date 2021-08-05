"""
File to run when using the Paraview GUI
"""

import sys, os
__DIR__ = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(__DIR__))

import utils
from importlib import reload
reload(utils)

from utils import getSource

getSourceRead(SUFFIX="low",
              LOG_SCALE=True, LOG_THRESHOLD=1e-04,
              THRESHOLD=4,
              CLIM=6,
              OPACITY=0.01, COLOR="GYPi")
getSourceRead(SUFFIX="high",
              LOG_SCALE=True, LOG_THRESHOLD=4e-04,
              THRESHOLD=4.9,
              CLIM=7,
              OPACITY=0.3)
