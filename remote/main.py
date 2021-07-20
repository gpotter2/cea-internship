"""
Script generating an animation from source files using remote server
"""

try:
    from paraview.simple import *
except ImportError:
    print("""
#########
Cannot import paraview.simple.
Make sure you are running this script using `pvpython` instead of `python` !
#########
""")

# Path
import os, sys
__DIR__ = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(__DIR__, "..", "paraview_source"))

# Connect
from connect import connect

# Source
from source import getSource

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


def main(cmd):
    """
    The main rendering pipeline
    """
    for cfg in CONFIG.values():
        getSource(**cfg)
    Render()

    if cmd == 0:
        print("OK")


def cli():
    """
    CLI: asks the user what to do
    """
    while True:
        cmd = input().lower()
        if cmd == "r":
            print("Reloading...", end="", flush=True)
            Delete()
            return 0
        elif cmd == "a":
            print("Animating now !")
            animationScene = GetAnimationScene()
            animationScene.GoToFirst()
            SaveAnimation("animation.ogv", FrameRate=24, Quality=2)
        elif cmd == "q":
            return -1
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
            print("- r\tReload")
            print("- a\tAnimate")
            print("- c\tConfig")
            print("- sc\tSet config")
            print("- q\tQuit")
        else:
            print("Unknown command '%s'" % cmd)


if __name__ == "__main__":
    # Connect then call main
    firstCLI = True
    cmd = None
    with connect():
        try:
            while True:
                main(cmd)
                if firstCLI:
                    print("### CLI ###")
                    firstCLI = False
                cmd = cli()
                if cmd == -1:
                    break
        except KeyboardInterrupt:
            pass
    print("Goodbye.")
