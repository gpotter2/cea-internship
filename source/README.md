# Installation

- make a conda environment, install `cupy`
- copy/paste `activate_this.py` into `.../miniconda3/bin/`
- link the missing libraries from `.../miniconda3/lib/` to `..../Paraview/lib/`:
   - `libstdc++.so*`
- change the config value in `__init__.py`
