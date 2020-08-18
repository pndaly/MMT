#!/usr/bin/env python3


# +
# import(s)
# -
from astropy.coordinates import Angle
from astropy.io import fits
from datetime import datetime
from datetime import timedelta
from PIL import Image

import hashlib
import json
import logging
import logging.config
import math
import os
import requests


# +
# constant(s)
# -
ASTROPLAN_IERS_URL = 'https://datacenter.iers.org/data/9/finals2000A.all'
ASTROPLAN_IERS_URL_ALTERNATE = 'ftp://cddis.gsfc.nasa.gov/pub/products/iers/finals2000A.all'
HTTP_CODES = {100: "Continue", 101: "Switching Protocols", 102: "Processing (WebDAV)",
              200: "OK", 201: "Created", 202: "Accepted", 203: "Non-Authoritative Information",
              204: "No Content", 205: "Reset Content", 206: "Partial Content", 207: "Multi-Status (WebDAV)",
              208: "Already Reported (WebDAV)", 226: "IM Used",
              300: "Multiple Choices", 301: "Moved Permanently", 302: "Found", 303: "See Other",
              304: "Not Modified", 305: "Use Proxy", 306: "(Unused)", 307: "Temporary Redirect",
              308: "Permanent Redirect (experimental)",
              400: "Bad Request", 401: "Unauthorized", 402: "Payment Required", 403: "Forbidden", 404: "Not Found",
              405: "Method Not Allowed", 406: "Not Acceptable", 407: "Proxy Authentication Required",
              408: "Request Timeout", 409: "Conflict", 410: "Gone", 411: "Length Required", 412: "Precondition Failed",
              413: "Request Entity Too Large", 414: "Request-URI Too Long", 415: "Unsupported Media Type",
              416: "Requested Range Not Satisfiable", 417: "Expectation Failed", 418: "I'm a teapot (RFC 2324)",
              420: "Enhance Your Calm (Twitter)", 422: "Unprocessable Entity (WebDAV)", 423: "Locked (WebDAV)",
              424: "Failed Dependency (WebDAV)", 425: "Reserved for WebDAV", 426: "Upgrade Required",
              428: "Precondition Required", 429: "Too Many Requests", 431: "Request Header Fields Too Large",
              444: "No Response (Nginx)", 449: "Retry With (Microsoft)",
              450: "Blocked by Windows Parental Controls (Microsoft)", 451: "Unavailable For Legal Reasons",
              499: "Client Closed Request (Nginx)",
              500: "Internal Server Error", 501: "Not Implemented", 502: "Bad Gateway", 503: "Service Unavailable",
              504: "Gateway Timeout", 505: "HTTP Version Not Supported", 506: "Variant Also Negotiates (Experimental)",
              507: "Insufficient Storage (WebDAV)", 508: "Loop Detected (WebDAV)",
              509: "Bandwidth Limit Exceeded (Apache)", 510: "Not Extended", 511: "Network Authentication Required"}
HTTP_MAX_CODE = max([int(_k) for _k in HTTP_CODES])
HTTP_MIN_CODE = min([int(_k) for _k in HTTP_CODES])
MMT_JSON_KEYS = ('centralwavelength', 'dec', 'dec_decimal', 'details', 'disabled', 'dithersize', 'epoch', 
                 'exposuretime', 'exposuretimecompleted', 'exposuretimeremaining', 'exposuretimeremainingformatted', 
                 'filter', 'findingchartfilename', 'gain', 'grating', 'grism', 'id', 'instrumentid', 'iscomplete', 
                 'locked', 'magnitude', 'mask', 'maskid', 'modified', 'moon', 'notes', 'notify', 'numberexposures',
                 'objectid', 'observationtype', 'offsetstars', 'onevisitpernight', 'pa', 'percentcompleted',
                 'photometric', 'pm_dec', 'pm_ra', 'priority', 'ra', 'ra_decimal', 'readtab', 'reduced', 'seeing',
                 'slitwidth', 'slitwidthproperty', 'submitted', 'targetofopportunity', 'totallength',
                 'totallengthformatted', 'visits')
MMT_LOG_CLR_FMT = \
    '%(log_color)s%(asctime)-20s %(levelname)-9s %(filename)-15s %(funcName)-15s line:%(lineno)-5d Message: %(message)s'
MMT_LOG_CSL_FMT = \
    '%(asctime)-20s %(levelname)-9s %(filename)-15s %(funcName)-15s line:%(lineno)-5d Message: %(message)s'
MMT_LOG_FIL_FMT = \
    '%(asctime)-20s %(levelname)-9s %(filename)-15s %(funcName)-15s line:%(lineno)-5d Message: %(message)s'
MMT_LOG_LEVELS = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
MMT_LOG_MAX_BYTES = 9223372036854775807

SDSS_URL = 'http://skyserver.sdss.org/dr16/SkyServerWS/ImgCutout/getjpeg'


# +
# pattern(s)
# -
# +/-dd:mm:ss.ssssss
DEC_PATTERN = '^[+-]?[0-8][0-9]:[0-5][0-9]:[0-5][0-9](\.[0-9]*)?'
# YYYY-MM-DDThh:mm:ss.ssssss
ISO_PATTERN = '(1[89][0-9]{2}|2[0-9]{3})-(0[13578]-[012][0-9]|0[13578]-3[0-1]|' \
                  '1[02]-[012][0-9]|1[02]-3[0-1]|02-[012][0-9]|0[469]-[012][0-9]|' \
                  '0[469]-30|11-[012][0-9]|11-30)[ T](0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9](\.[0-9]*)?'
# HH:MM:SS.SSSSSS
RA_PATTERN = '^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9](\.[0-9]*)?'


# +
# class: Logger() inherits from the object class
# -
# noinspection PyBroadException,PyPep8
class Logger(object):

    # +
    # method: __init__
    # -
    def __init__(self, name='', level='DEBUG'):

        # get arguments(s)
        self.name = name
        self.level = level

        # define some variables and initialize them
        self.__msg = None
        self.__logconsole = f'/tmp/console-{self.__name}.log'
        self.__logdir = os.getenv("MMT_LOG")
        if not os.path.exists(self.__logdir) or not os.access(self.__logdir, os.W_OK):
            self.__logdir = os.getcwd()
        self.__logfile = f'{self.__logdir}/{self.__name}.log'

        # logger dictionary
        utils_logger_dictionary = {

            # logging version
            'version': 1,

            # do not disable any existing loggers
            'disable_existing_loggers': False,

            # use the same formatter for everything
            'formatters': {
                'ObsColoredFormatter': {
                    '()': 'colorlog.ColoredFormatter',
                    'format': MMT_LOG_CLR_FMT,
                    'log_colors': {
                        'DEBUG': 'cyan',
                        'INFO': 'green',
                        'WARNING': 'yellow',
                        'ERROR': 'red',
                        'CRITICAL': 'white,bg_red',
                    }
                },
                'ObsConsoleFormatter': {
                    'format': MMT_LOG_CSL_FMT
                },
                'ObsFileFormatter': {
                    'format': MMT_LOG_FIL_FMT
                }
            },

            # define file and console handlers
            'handlers': {
                'colored': {
                    'class': 'logging.StreamHandler',
                    'formatter': 'ObsColoredFormatter',
                    'level': self.__level,
                },
                'console': {
                    'class': 'logging.StreamHandler',
                    'formatter': 'ObsConsoleFormatter',
                    'level': self.__level,
                    'stream': 'ext://sys.stdout'
                },
                'file': {
                    'backupCount': 10,
                    'class': 'logging.handlers.RotatingFileHandler',
                    'formatter': 'ObsFileFormatter',
                    'filename': self.__logfile,
                    'level': self.__level,
                    'maxBytes': MMT_LOG_MAX_BYTES
                },
                'utils': {
                    'backupCount': 10,
                    'class': 'logging.handlers.RotatingFileHandler',
                    'formatter': 'ObsFileFormatter',
                    'filename': self.__logconsole,
                    'level': self.__level,
                    'maxBytes': MMT_LOG_MAX_BYTES
                }
            },

            # make this logger use file and console handlers
            'loggers': {
                self.__name: {
                    'handlers': ['colored', 'file', 'utils'],
                    'level': self.__level,
                    'propagate': True
                }
            }
        }

        # configure logger
        logging.config.dictConfig(utils_logger_dictionary)

        # get logger
        self.logger = logging.getLogger(self.__name)

    # +
    # Decorator(s)
    # -
    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name=''):
        self.__name = name if (isinstance(name, str) and name.strip() != '') else os.getenv('USER')

    @property
    def level(self):
        return self.__level

    @level.setter
    def level(self, level=''):
        self.__level = level.upper() if \
            (isinstance(level, str) and level.strip() != '' and level.upper() in MMT_LOG_LEVELS) else MMT_LOG_LEVELS[0]


# +
# function: get_isot()
# -
# noinspection PyBroadException
def get_isot(ndays=0):
    try:
        return (datetime.utcnow() + timedelta(days=ndays)).isoformat()
    except:
        return None


# +
# function: get_hash()
# -
# noinspection PyBroadException,PyPep8
def get_hash(seed=get_isot()):
    """ return unique 64-character string """
    try:
        return hashlib.sha256(seed.encode('utf-8')).hexdigest()
    except:
        return None


# +
# function: ra_to_decimal()
# -
# noinspection PyBroadException
def ra_to_decimal(ra='22:35:57.6 hours'):
    """ return RA H:M:S as a decimal """
    try:
        ra = f'{ra} hours' if 'hours' not in ra.lower() else ra
        return float(Angle(ra).degree)
    except:
        return math.nan


# +
# function: dec_to_decimal()
# -
# noinspection PyBroadException,PyPep8
def dec_to_decimal(dec='33:57:56.0 degrees'):
    """ return Dec d:m:s as a decimal """
    try:
        dec = f'{dec} degrees' if 'degrees' not in dec.lower() else dec
        return float(Angle(dec).degree)
    except:
        return math.nan


# +
# function: fits_to_png()
# -
# noinspection PyBroadException
def fits_to_png(fits_file='', _log=None):

    # check input(s)
    if not isinstance(fits_file, str) or fits_file.strip() == '':
        raise Exception(f'invalid input, fits_file={fits_file}')
    _log = _log if isinstance(_log, logging.Logger) else None

    # set default(s)
    fits_file = os.path.abspath(os.path.expanduser(fits_file))
    if not os.path.exists(fits_file):
        raise Exception(f'input not found, fits_file={fits_file}')

    # message
    if _log:
        _log.info(f"fits_file={fits_file}, log={_log}")

    # get data
    _data = None
    try:
        _data = fits.getdata(fits_file)
    except:
        raise Exception(f'unable to read {fits_file}')

    # write output
    if _data is not None:
        _img = Image.fromarray(_data)
        _img.save(fits_file.replace('.fits', '.png'))
        return os.path.abspath(os.path.expanduser(fits_file.replace('.fits', '.png')))


# +
# function: get_finder_chart()
# -
# noinspection PyBroadException
def get_finder_chart(**kw):

    # get critical input(s): RA, Dec
    try:
        _ra = kw['ra']
        _dec = kw['dec']
    except Exception as _v:
        print(f"invalid input(s), error={_v}")
        return ''

    # get logger
    _log = kw['log'] if ('log' in kw and isinstance(kw['log'], logging.Logger)) else None

    # set default(s) [NB: plate scale default is 2x the SDSS value]
    _ra_str = _ra.replace('.', '').replace(':', '').replace(' ', '').strip()[:6]
    _dec_str = _dec.replace('.', '').replace(':', '').replace(' ', '').replace('-', '').replace('+', '').strip()[:6]
    _scale = kw['scale'] if ('scale' in kw and isinstance(kw['scale'], float) and kw['scale'].strip != '') else 0.79224
    _width = kw['width'] if ('width' in kw and isinstance(kw['width'], int) and kw['width'].strip != '') else 400
    _height = kw['height'] if ('height' in kw and isinstance(kw['height'], int) and kw['height'].strip != '') else 400
    _opt = kw['opt'] if ('opt' in kw and isinstance(kw['opt'], str) and kw['opt'].strip != '') else 'GL'
    _query = kw['query'] if ('query' in kw and isinstance(kw['query'], str) and kw['query'].strip != '') else ''
    _jpg = kw['jpg'] if ('jpg' in kw and isinstance(kw['jpg'], str) and kw['jpg'].strip != '') else \
        f'sdss_{_ra_str}_{_dec_str}.jpg'
    _url, _req = f"{SDSS_URL}?ra={ra_to_decimal(_ra)}&dec={dec_to_decimal(_dec)}&scale={_scale}&" \
                 f"width={_width}&height={_height}&opt={_opt}&query={_query}", None

    # request data
    if _log:
        _log.debug(f"_url={_url}, _jpg={_jpg}")
    try:
        _req = requests.get(url=f'{_url}')
    except Exception as _e:
        raise Exception(f"failed to complete request, _req={_req}, error={_e}")

    # if everything is ok, create the jpg image and return the path
    if _req is not None and hasattr(_req, 'status_code') and _req.status_code == 200 and hasattr(_req, 'content'):
        try:
            with open(_jpg, 'wb') as _f:
                _f.write(_req.content)
            return os.path.abspath(os.path.expanduser(_jpg))
        except:
            return ''


# +
# function: jpg_to_png()
# -
# noinspection PyBroadException
def jpg_to_png(_jpg='', _log=None):

    # check input(s)
    if not isinstance(_jpg, str) or _jpg.strip() == '':
        raise Exception(f'invalid input, _jpg={_jpg}')
    _jpg = os.path.abspath(os.path.expanduser(_jpg))
    if not os.path.exists(_jpg):
        raise Exception(f'file not found, _jpg={_jpg}')
    _log = _log if isinstance(_log, logging.Logger) else None

    # convert
    try:
        _png = _jpg.replace('.jpg', '.png')
        _data = Image.open(_jpg)
        _data.save(_png)
        return _png
    except:
        return ''


# +
# function: http_status()
# -
# noinspection PyBroadException
def http_status(_code=-1):
    try:
        return True if HTTP_CODES.get(_code, None) is not None else False
    except:
        return False


# +
# function: verify_keys()
# -
# noinspection PyBroadException
def verify_keys(_input=None, _keys=None):
    try:
        return all(_k in _keys for _k in _input)
    except:
        return False


# +
# function: parse_response()
# -
# noinspection PyBroadException
def parse_response(_req=None, _log=None):
    _log = _log if isinstance(_log, logging.Logger) else None
    if _req is not None and hasattr(_req, 'status_code') and \
            http_status(int(_req.status_code)) and hasattr(_req, 'text'):
        if _req.status_code == 200:
            try:
                _json = json.loads(_req.text)
            except:
                _json = {}
            if verify_keys(_json, MMT_JSON_KEYS):
                if _log:
                    _log.info(f"received (json) {_json}")
                return _json
            else:
                if _log:
                    _log.info(f"received (text) {_req.text}")
                return _req.text
        else:
            if _log:
                _log.info(f"received (text) {_req.text}, status={_req.status_code}")
            return _req.text


# +
# function: get_iers_1():
# -
# noinspection PyBroadException
def get_iers_1(url=ASTROPLAN_IERS_URL):

    # check input(s)
    if not isinstance(url, str) or url.strip() == '':
        raise Exception(f'invalid input, url={url}')
    if not (url.strip().lower().startswith('ftp') or url.strip().lower().startswith('http')):
        raise Exception(f'invalid address, url={url}')

    # astroplan download
    try:
        print(f'IERS updating from astroplan from {url}')
        from astroplan import download_IERS_A
        download_IERS_A()
        print(f'IERS updated from astroplan from {url}')
    except:
        print(f'failed IERS update from astroplan from {url}')


# +
# function: get_iers_2():
# -
# noinspection PyBroadException
def get_iers_2(url=ASTROPLAN_IERS_URL_ALTERNATE):

    # check input(s)
    if not isinstance(url, str) or url.strip() == '':
        raise Exception(f'invalid input, url={url}')
    if not (url.strip().lower().startswith('ftp') or url.strip().lower().startswith('http')):
        raise Exception(f'invalid address, url={url}')

    # astropy download
    try:
        print(f'IERS updating from astropy from {url}')
        from astroplan import download_IERS_A
        from astropy.utils import iers
        from astropy.utils.data import clear_download_cache
        clear_download_cache()
        iers.IERS_A_URL = f'{url}'
        download_IERS_A()
        print(f'IERS updated from astropy from {url}')
    except:
        print(f'failed IERS update from astropy from {url}')


# +
# function: get_iers():
# -
# noinspection PyBroadException
def get_iers():
    try:
        get_iers_1()
    except:
        get_iers_2()
