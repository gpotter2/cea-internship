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
sys.path.append(os.path.join(__DIR__, "..", "source"))

# Connect
from connect import connect

# Source
from source import getSource

CONFIG = {
    "CLIP_HALF": False,
    "CLIP_INV_QUATER": False,
    "LOG_SCALE": True,
    "LOG_THRESHOLD": 5e-5,
}

def main(cmd):
    """
    The main rendering pipeline
    """
    source = getSource(**CONFIG)
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
            ResetSession()
            return 0
        elif cmd == "q":
            return -1
        elif cmd == "c":
            print("Config:")
            for c in CONFIG.items():
                print("- %s: %s" % c)
        elif cmd == "sc":
            k = input("What config key to change: ").upper()
            if k not in CONFIG:
                print("Unknown config key")
                continue
            if isinstance(CONFIG[k], bool):
                CONFIG[k] = not CONFIG[k]
            elif isinstance(CONFIG[k], (int, float)):
                v = input("Value: ")
                try:
                    v = type(CONFIG[k])(v)
                    CONFIG[k] = v
                except ValueError:
                    print("Invalid value")
                    continue
            else:
                print("Cannot change this config value !")
            print("%s set to %s" % (k, CONFIG[k]))
        elif cmd in ["?", "h", "help"]:
            print("Commands:")
            print("- r\tReload")
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
