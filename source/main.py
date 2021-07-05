"""
File to run when using the Paraview GUI
"""

import sys, os
__DIR__ = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(__DIR__))

from source import getSource

getSource(SUFFIX="low", OPACITY=0.01, LOG_THRESHOLD=2e-5, COLOR="GYPi")
getSource(SUFFIX="high", OPACITY=0.2)
