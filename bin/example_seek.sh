#!/bin/bash
_begin='2020-06-04T00:00:00.000000'
_end='2020-06-04T23:59:59.999999'
python3 ${MMT_SRC}/seek.py --begin=${_begin} --end=${_end} --nelms=0 --path=~ --type=.fits
python3 ${MMT_SRC}/seek.py --begin=${_begin} --end=${_end} --nelms=1 --path=~ --type=.fits
python3 ${MMT_SRC}/seek.py --begin=${_begin} --end=${_end} --nelms=2 --path=~ --type=.fits
python3 ${MMT_SRC}/seek.py --begin=${_begin} --end=${_end} --nelms=3 --path=~ --type=.fits
python3 ${MMT_SRC}/seek.py --begin=${_begin} --end=${_end} --nelms=4 --path=~ --type=.fits
python3 ${MMT_SRC}/seek.py --begin=${_begin} --end=${_end} --nelms=5 --path=~ --type=.fits
