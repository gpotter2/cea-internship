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

getSource(SUFFIX="low", THRESHOLD=0.002, OPACITY=0.01, COLOR="GYPi")
getSource(SUFFIX="high", THRESHOLD=0.002, OPACITY=0.2)
