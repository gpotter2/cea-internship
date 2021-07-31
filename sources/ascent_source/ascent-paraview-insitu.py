"""
Entry point for Ascent Insitu
"""

########################
# CONFIG ! IMPORTANT ! #
########################

# __file__ does not work with ascent so add it manually
__file__ = "/home/gpotter/pv_work/sources/ascent_source/ascent-paraview-insitu.py"
# The path to the paraview python module. This must have been compiled with the SAME python version
# as everything else ! watch out
PARAVIEW_SITE_PACKAGES = "/home/gpotter/spack/opt/spack/linux-rhel7-skylake_avx512/gcc-9.4.0/paraview-5.9.1-gmpub3sql6hkvibxxtxexixkuv3agmao/lib64/python3.8/site-packages"

import sys, os
__DIR__ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "paraview_source"))
PLUGIN_PATH = os.path.join(__DIR__, "internal", "paraview_ascent_source.py")

sys.path.append(__DIR__)
sys.path.append(os.path.join(__DIR__, "internal"))
sys.path.append(PARAVIEW_SITE_PACKAGES)

# See https://ascent.readthedocs.io/en/latest/Actions/ParaViewVisualization.html

# Same Python interpreter for all time steps
# We use count for one time initializations
try:
    count2 = count2 + 1
except NameError:
    count2 = 0

if count2 == 0:
    # Initialization
    import paraview
    paraview.options.batch = True
    paraview.options.symmetric = True
    from paraview.simple import *

    LoadPlugin(PLUGIN_PATH, remote=True, ns=globals())

    # Setup source
    ascentSource = AscentSource()

    # Setup View
    CreateRenderView()

    # Configure View
    from utils import showField, showPoints, setupView
    setupView()

    cam = GetActiveCamera()
    cam.Azimuth(-90)

    showField(OutputPort(ascentSource, 0),
              THRESHOLD=1,
              CLIM=2e4,
              field="By_l",
              OPACITY=0.01, COLOR="GYPi")
    showField(OutputPort(ascentSource, 0),
              THRESHOLD=1,
              CLIM=2e4,
              field="By_h",
              OPACITY=0.3)
    showPoints(OutputPort(ascentSource, 1), field="particle_electrons_ux")

# Update data
ascentSource.UpdateAscentData()
ascentSource.UpdatePropertyInformation()

cycle = GetProperty(ascentSource, "Cycle").GetElement(0)
rank = GetProperty(ascentSource, "Rank").GetElement(0)
if (rank == 0):
    print(
        "=======================================Called: {} {} {}".format(
            GetProperty(ascentSource, "TimeStep"),
            GetProperty(ascentSource, "Cycle"),
            GetProperty(ascentSource, "Time")))

dataFieldName = "fields_{0:04d}.pvd".format(int(cycle))
dataPartName = "parts_{0:04d}.pvd".format(int(cycle))
imageName = "image_{0:04d}.png".format(int(cycle))

Render()
ResetCamera()

#SaveData(dataFieldName, OutputPort(ascentSource, 0))
#SaveData(dataPartName, OutputPort(ascentSource, 1))
SaveScreenshot(imageName, ImageResolution=(1024, 1024))
