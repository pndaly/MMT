#!/usr/bin/env python3


# +
# import(s)
# -
from seek import *

import math
import random


# +
# doc string(s)
# -
__doc__ = """
  % python3 -m pytest -p no:warnings test_seek.py
"""


# +
# constant(s)
# -
INVALID_INPUTS = [None, get_hash(), {}, [], (), math.pi, -9223372036854775807]
RANDOM_SEED = random.seed(os.getpid())
LOWER_BOUND = random.randint(-1000, 0)
UPPER_BOUND = random.randint(0, 1000)


# +
# test: seek(_begin='', _end='', _nelms=0, _path=os.getcwd(), _type='')
# -
def test_seek_0():
    """ invalid _begin argument """
    assert all(seek(_begin=_k) is None for _k in INVALID_INPUTS)


def test_seek_1():
    """ invalid _end argument """
    _b = get_isot(random.randint(LOWER_BOUND, UPPER_BOUND))
    assert all(seek(_begin=_b, _end=_k) is None for _k in INVALID_INPUTS)


def test_seek_2():
    """ invalid _nelms argument """
    _b = get_isot(random.randint(LOWER_BOUND, UPPER_BOUND))
    _e = get_isot(random.randint(LOWER_BOUND, UPPER_BOUND))
    assert all(seek(_begin=_b, _end=_e, _nelms=_k) is None for _k in INVALID_INPUTS)


def test_seek_3():
    """ invalid _path argument """
    _b = get_isot(random.randint(LOWER_BOUND, UPPER_BOUND))
    _e = get_isot(random.randint(LOWER_BOUND, UPPER_BOUND))
    _n = abs(random.randint(LOWER_BOUND, UPPER_BOUND))
    assert all(seek(_begin=_b, _end=_e, _nelms=_n, _path=_k) is None for _k in INVALID_INPUTS)


def test_seek_4():
    """ invalid _type argument """
    _b = get_isot(random.randint(LOWER_BOUND, UPPER_BOUND))
    _e = get_isot(random.randint(LOWER_BOUND, UPPER_BOUND))
    _n = abs(random.randint(LOWER_BOUND, UPPER_BOUND))
    _p = os.path.abspath(os.path.expanduser('~'))
    assert all(seek(_begin=_b, _end=_e, _nelms=_n, _path=_p, _type=_k) in [None, {}] for _k in INVALID_INPUTS)


def test_seek_5():
    """ valid argument(s) """
    _b = '2020-06-04T00:00:00.000000'
    _e = '2020-06-04T23:59:59.999999'
    _p = '/rts2data/Kuiper/Mont4k/20200604'
    _n = 0
    _t = '.fits'
    assert seek(_begin=_b, _end=_e, _nelms=_n, _path=_p, _type=_t).keys() is not None
