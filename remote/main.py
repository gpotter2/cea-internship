"""
Script generating an animation from source files using remote server
"""

try:
    from paraview.simple import *
    import paraview.servermanager
    from paraview.servermanager import SetProgressPrintingEnabled, vtkProcessModule
except ImportError:
    print("""
#########
Cannot import paraview.simple.
Make sure you are running this script using `pvpython` instead of `python` !
#########
""")

import sys
sys.path.append('/home/gpotter/.local/lib/python3.9/site-packages')
from tqdm import tqdm

# Path
import os, sys
__DIR__ = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(__DIR__, "..", "paraview_source"))

# Connect
from connect import connect

# Source
from source import getSource

progressBar = None

CONFIG = {
    "low": {
        "SUFFIX": "low",
        "LOG_SCALE": True,
        "LOG_THRESHOLD": 1e-4,
        "THRESHOLD": 4,
        "CLIM": 5.7,
        "OPACITY": 0.01,
        "COLOR": "GYPi",
    },
    "high": {
        "SUFFIX": "high",
        "LOG_SCALE": True,
        "LOG_THRESHOLD": 1e-4,
        "THRESHOLD": 4.5,
        "CLIM": 6,
        "OPACITY": 0.3
    }
}

class ProgressBar:
    def __init__(self, eventname):
        self.progress = 0
        self.bar = None
        self.eventname = eventname
        self.total = len(GetActiveSource().TimestepValues)

    def __enter__(self):
        global progressBar
        self.bar = tqdm(total=self.total)
        self.bar.__enter__()
        progressBar = self
        SetProgressPrintingEnabled(True)

    def __exit__(self, *args):
        SetProgressPrintingEnabled(False)
        return self.bar.__exit__(*args)

    def setProg(self, prog):
        self.bar.update(prog - self.progress)
        self.progress = prog

class CLI:
    def __init__(self):
        self.shown = False
        self.view = None

    def loadSources(self):
        """
        The main rendering pipeline
        """
        for cfg in CONFIG.values():
            getSource(**cfg)
        self.view = GetActiveView()

    def cli(self):
        """
        CLI: asks the user what to do
        """
        self.loadSources()
        print("Welcome to the CLI ! ? for help")
        while True:
            cmd = input().lower()
            if cmd == "r":
                print("Reloading...", end="", flush=True)
                ResetSession()
                self.loadSources()
            elif cmd == "s":
                Interact(self.view)
            elif cmd == "a":
                print("Animating now !")
                animationScene = GetAnimationScene()
                animationScene.GoToFirst()
                with ProgressBar("SceneImageWriterMovie"):
                    SaveAnimation("animation.ogv", FrameRate=24, Quality=2)
            elif cmd == "q":
                return
            elif cmd == "c":
                print("Config:")
                for name, cfg in CONFIG.items():
                    print("- %s" % name)
                    for c in cfg.items():
                        print("  - %s: %s" % c)
            elif cmd == "sc":
                print("Available configs: %s" % list(CONFIG.keys()))
                name = input("What config to use: ")
                if name not in CONFIG:
                    print("Unknown config name !")
                    continue
                cfg = CONFIG[name]
                k = input("What config key to change: ").upper()
                if k not in cfg:
                    print("Unknown config key")
                    continue
                if isinstance(cfg[k], bool):
                    cfg[k] = not cfg[k]
                elif isinstance(cfg[k], (int, float)):
                    v = input("Value: ")
                    try:
                        v = type(cfg[k])(v)
                        cfg[k] = v
                    except ValueError:
                        print("Invalid value")
                        continue
                else:
                    print("Cannot change this config value !")
                print("%s set to %s" % (k, cfg[k]))
            elif cmd in ["?", "h", "help"]:
                print("Commands:")
                print("- s\tShow (interactive)")
                print("- r\tReload")
                print("- a\tAnimate")
                print("- c\tConfig")
                print("- sc\tSet config")
                print("- q\tQuit")
            else:
                print("Unknown command '%s'" % cmd)


def _printProgress(caller, event):
    progress = caller.GetLastProgress()
    alg = caller.GetLastProgressText()
    global progressBar
    if alg == progressBar.eventname:
        progressBar.setProg(progress)

paraview.servermanager._printProgress = _printProgress

if __name__ == "__main__":
    # Connect then call main
    with connect():
        # Run main loop
        cli = CLI()
        try:
            cli.cli()
        except KeyboardInterrupt:
            pass
    print("Goodbye.")
