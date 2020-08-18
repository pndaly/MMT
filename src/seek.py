#!/usr/bin/env python3


# +
# import(s)
# -
from astropy.time import Time
from datetime import datetime
from datetime import timedelta

import argparse
import hashlib
import math
import os
import re
import time


# +
# __doc__
# -
__doc__ = """
    % python3.7 seek.py --help
"""


# +
# constant(s)
# -
ISO_PATTERN = '[0-9]{4}-[0-9]{2}-[0-9]{2}[ T?][0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{6}'


# +
# function: get_isot()
# -
# noinspection PyBroadException
def get_isot(ndays=0):
    try:
        return (datetime.now() + timedelta(days=ndays)).isoformat()
    except:
        return None


# +
# function: get_jd()
# -
# noinspection PyBroadException
def get_jd(ndays=0):
    try:
        return Time(get_isot(ndays)).jd
    except:
        return math.nan


# +
# function: isot_to_jd()
# -
# noinspection PyBroadException
def isot_to_jd(isot=get_isot()):
    try:
        return Time(isot).jd
    except:
        return math.nan


# +
# function: jd_to_isot()
# -
# noinspection PyBroadException
def jd_to_isot(jd=math.nan):
    try:
        return Time(jd, format='jd', precision=6).isot
    except:
        return None


# +
# function: get_hash()
# -
# noinspection PyBroadException
def get_hash(seed=get_isot()):
    try:
        return hashlib.sha256(seed.encode('utf-8')).hexdigest()
    except:
        return None


# +
# function: seek()
# -
# noinspection PyBroadException
def seek(_begin='', _end='', _nelms=0, _path=os.getcwd(), _type=get_hash()):
    """ return dictionary {jd: filename} of files or None """

    # check input(s)
    if not isinstance(_begin, str) or (re.match(ISO_PATTERN, _begin) is None):
        return None
    if not isinstance(_end, str) or (re.match(ISO_PATTERN, _end) is None):
        return None
    if not isinstance(_nelms, int) or _nelms < 0:
        return None
    if not isinstance(_type, str) or _type.strip() == '':
        return None
    if not isinstance(_path, str) or _path.strip() == '':
        return None

    # verify input(s)
    _path = os.path.abspath(os.path.expanduser(f'{_path}'))
    if not os.path.isdir(_path):
        return None
    _begin_jd, _end_jd = isot_to_jd(_begin), isot_to_jd(_end)
    if _begin_jd > _end_jd:
        _begin_jd, _end_jd = _end_jd, _begin_jd

    # generator code
    _fw = (
        os.path.join(_root, _file)
        for _root, _dirs, _files in os.walk(_path)
        for _file in _files
    )

    # get all files within jd period of given type
    try:
        _ret = {
            isot_to_jd(f"{time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(os.stat(_k).st_ctime))}.000000"): f'{_k}'
            for _k in _fw if (
                    not os.path.islink(f'{_k}') and os.path.exists(f'{_k}') and _k.endswith(f'{_type}') and
                    int(os.stat(f'{_k}').st_size) > 0 and
                    (_begin_jd <
                     isot_to_jd(f"{time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(os.stat(_k).st_ctime))}.000000")
                     < _end_jd))
        }
    except Exception:
        return None

    # return (all if nelms == 0)
    return {_k: _ret[_k] for _k in sorted(_ret.keys(), reverse=True)[:len(_ret) if _nelms == 0 else _nelms]}


# +
# main()
# -
if __name__ == '__main__':

    # noinspection PyTypeChecker
    _p = argparse.ArgumentParser(description=f'Seek File(s)', formatter_class=argparse.RawTextHelpFormatter)
    _p.add_argument(f'--begin', default=get_isot(-1), help=f"""begin date, defaults to %(default)s""")
    _p.add_argument(f'--end', default=get_isot(), help=f"""end date, defaults to %(default)s""")
    _p.add_argument(f'--nelms', default=0, help=f"""number of elements, defaults to %(default)s""")
    _p.add_argument(f'--path', default=os.getcwd(), help=f"""root path, defaults to %(default)s""")
    _p.add_argument(f'--type', default='.fits', help=f"""file type, defaults to %(default)s""")
    args = _p.parse_args()

    # execute
    _ans = seek(_begin=args.begin, _end=args.end, _nelms=int(args.nelms), _path=args.path, _type=args.type)
    if _ans is not None:
        print(f"{_ans}")
