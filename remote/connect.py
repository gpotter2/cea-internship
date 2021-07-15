"""
Script generating an animation from source files using remote server
"""

import select
import subprocess
import sys
import time

from paraview.simple import *

class connect:
    def __init__(self):
        # Config
        self.INSTALL_PATH = "/home/gpotter/ParaView-5.9.1-egl-MPI-Linux-Python3.8-64bit"
        self.USER = "gpotter"
        self.HOST = "iram-na-002657.extra.cea.fr"
        self.PORT = 11111

    def __enter__(self):
        print("Launching paraview server remotely...")
        self.process = subprocess.Popen([
            "ssh",
            "-L%s:%s:%s" % (self.PORT, self.HOST, self.PORT),
            "-l",
            self.USER,
            self.HOST,
            "%s/bin/mpiexec -np 8 %s/bin/pvserver" % ((self.INSTALL_PATH, ) * 2)
        ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE, encoding="utf-8")
        print("Waiting for it to start...")
        try:
            buf = ""
            t = time.time()
            while "accepting connection" not in buf:
                if select.select([self.process.stdout], [], [], 0):
                    buf += self.process.stdout.read(1).lower()
                if (time.time() - t) >= 10:
                    print("Connection timed out !")
                    raise ValueError
            print("Server started. Connecting...")
            Connect("localhost", self.PORT)
            print("Connected")
        except KeyboardInterrupt:
            self.__exit__(None, None, None)

    def __exit__(self, type, value, tb):
        print("Disconnecting...")
        Disconnect()
        self.process.terminate()
        self.process.wait(timeout=3)
        if self.process.poll() is None:
            print("Warning: Process is still running !")
        else:
            print("Process successfully terminated.")
