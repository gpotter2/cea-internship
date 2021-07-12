"""
File to run when using the Paraview GUI
"""

import sys, os
__DIR__ = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(__DIR__))

import source
from importlib import reload
reload(source)

from source import getSource

getSource(SUFFIX="low",
          LOG_SCALE=True, LOG_THRESHOLD=1e-04,
          THRESHOLD=1.,
          CLIM=4,
          OPACITY=0.01, COLOR="GYPi")
getSource(SUFFIX="high",
          LOG_SCALE=True, LOG_THRESHOLD=4e-04,
          THRESHOLD=3.,
          CLIM=4,
          OPACITY=0.2)
