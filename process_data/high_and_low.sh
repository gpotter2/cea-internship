#!/bin/bash
python propagate.py --filter-lowpass 1.5 --suffix low
python propagate.py --filter-highpass 1.5 --suffix high
