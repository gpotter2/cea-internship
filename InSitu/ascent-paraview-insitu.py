"""
Entry point for Ascent Insitu when using the ParaView plugin
"""

########################
# CONFIG ! IMPORTANT ! #
########################

# __file__ does not currently work with ascent so add it manually
__file__ = "/home/gpotter/pv_work/InSitu/ascent-paraview-insitu.py"
# The path to the paraview python module. This must have been compiled with the SAME python version
# as everything else ! watch out
PARAVIEW_SITE_PACKAGES = "/home/gpotter/spack/opt/spack/linux-rhel7-skylake_avx512/gcc-9.4.0/paraview-5.9.1-gmpub3sql6hkvibxxtxexixkuv3agmao/lib64/python3.8/site-packages"

import sys, os
__DIR__ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "ParaViewObjects"))
PLUGIN_PATH = os.path.join(__DIR__, "paraview_ascent_source.py")

sys.path.append(__DIR__)
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
    from WarpXFreqFilter import getFormatFilter
    setupView()

    cam = GetActiveCamera()
    cam.Azimuth(-70)

    Filtered = getFormatFilter(
        OutputPort(ascentSource, 0),
        "By",
        "By_lowfreq",
        "By_highfreq",
    )

    # If nothing appears, it could be that the opacity is glitched.
    # Try setting it to 1.0. If that's the issue, check your paraview
    # and google "paraview opacity not working". Make sure you're using
    # the correct build (cuda...)
    showField(Filtered,
              THRESHOLD=0.2,
              CLIM=2,
              field="By_highfreq",
              OPACITY=1.0
              )
    # See https://discourse.paraview.org/t/view-multiple-data-arrays-at-once-from-a-single-file/2770 on why we need PassArrays
    # to shallow copy the data.
    passArray = PassArrays(Input=Filtered)
    passArray.CellDataArrays = ['By_lowfreq']
    showField(passArray,
              THRESHOLD=0.1,
              CLIM=2,
              field="By_lowfreq",
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
