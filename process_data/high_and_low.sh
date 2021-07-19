#!/bin/bash
PROPAGATE_PROFILE='high' python propagate.py --filter-highpass 2.5 --suffix high
python propagate.py --filter-lowpass 1.5 --suffix low
