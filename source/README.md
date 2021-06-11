# Installation

- make a conda environment, install `cupy`, `libgcc`
- copy/paste `installation/activate_this.py` into `.../miniconda3/bin/`
- add to your .bashrc:

```
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/user/miniconda3/lib/
```

- `ln -s /home/user/miniconda3/lib/libstdc++.so* /home/user/Paragiew/lib/`
- change the config values in `__init__.py`
