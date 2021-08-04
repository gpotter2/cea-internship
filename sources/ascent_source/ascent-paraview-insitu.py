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
    from utils import showField, showPoints, setupView, getFFTFilter
    setupView()

    cam = GetActiveCamera()
    cam.Azimuth(-100)

    Filtered = getFFTFilter(OutputPort(ascentSource, 0), "By")

    # If nothing appears, it could be that the opacity is glitched.
    # Try setting it to 1.0. If that's the issue, check your paraview
    # and google "paraview opacity not working". Make sure you're using
    # the correct build (cuda...)
    showField(Filtered,
              THRESHOLD=0.25,
              CLIM=2,
              field="By_h",
              OPACITY=1.0
              )
    # See https://discourse.paraview.org/t/view-multiple-data-arrays-at-once-from-a-single-file/2770 on why we need PassArrays
    # to shallow copy the data.
    passArray = PassArrays(Input=Filtered)
    passArray.CellDataArrays = ['By_l']
    showField(passArray,
              THRESHOLD=0.3,
              CLIM=2,
              field="By_l",
              OPACITY=1.0,
              COLOR="GYPi")
    showPoints(OutputPort(ascentSource, 1),
               field="particle_electrons_w")

# Update data
ascentSource.UpdateAscentData()
ascentSource.UpdatePropertyInformation()

cycle = GetProperty(ascentSource, "Cycle").GetElement(0)
rank = GetProperty(ascentSource, "Rank").GetElement(0)

dataFieldName = "fields_{0:04d}.pvd".format(int(cycle))
dataPartName = "parts_{0:04d}.pvd".format(int(cycle))
imageName = "image_{0:04d}.png".format(int(cycle))

Render()
ResetCamera()

#SaveData(dataFieldName, OutputPort(ascentSource, 0))
#SaveData(dataPartName, OutputPort(ascentSource, 1))
SaveScreenshot(imageName, ImageResolution=(1024, 1024))
