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

getSource(SUFFIX="low", OPACITY=0.01, LOG_THRESHOLD=2e-5, COLOR="GYPi")
getSource(SUFFIX="high", OPACITY=0.2)
