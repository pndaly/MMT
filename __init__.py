#!/usr/bin/env python3


# +
# import(s)
# -
from astropy.io import fits
from datetime import datetime
from datetime import timedelta
from PIL import Image

import json
import os


# +
# constant(s)
# -
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
MMT_CATALOG_ID = 486
MMT_PROGRAM_ID = -1
MMT_TARGET_ID = -1
MMT_JSON_KEYS = ("id", "ra", "objectid", "observationtype", "moon", "seeing", "photometric", "priority", "dec",
                 "ra_decimal", "dec_decimal", "pm_ra", "pm_dec", "magnitude", "exposuretime", "numberexposures",
                 "visits", "onevisitpernight", "filter", "grism", "grating", "centralwavelength", "readtab",
                 "gain", "dithersize", "epoch", "submitted", "modified", "notes", "pa", "maskid", "slitwidth",
                 "slitwidthproperty", "iscomplete", "disabled", "notify", "locked", "findingchartfilename",
                 "instrumentid", "targetofopportunity", "reduced", "exposuretimeremaining", "totallength",
                 "totallengthformatted", "exposuretimeremainingformatted", "exposuretimecompleted",
                 "percentcompleted", "offsetstars", "details", "mask")
MMT_URL = 'https://scheduler.mmto.arizona.edu/APIv2/catalogTarget'


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
# function: fits_to_png()
# -
# noinspection PyBroadException
def fits_to_png(fits_file='', verbose=False):

    # check input(s)
    if not isinstance(fits_file, str) or fits_file.strip() == '':
        raise Exception(f'invalid input, fits_file={fits_file}')
    verbose = verbose if isinstance(verbose, bool) else False

    # set default(s)
    fits_file = os.path.abspath(os.path.expanduser(fits_file))
    if not os.path.exists(fits_file):
        raise Exception(f'input not found, fits_file={fits_file}')

    # message
    if verbose:
        print(f"fits_file={fits_file}, verbose={verbose}")

    # get data
    _data = None
    try:
        _data = fits.getdata(fits_file)
    except:
        raise Exception(f'unable to read {fits_file}')

    # write output
    if _data is not None:
        _d, _f = os.path.dirname(fits_file), os.path.basename(fits_file)
        _png_path = os.path.join(_d, f"{_f.split('.')[0]}.png")
        if verbose:
            print(f"_d={_d}, _f={_f}, _png_path={_png_path}")
        _img = Image.fromarray(_data)
        _img.save(_png_path)
        return _png_path


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
def parse_response(_req=None, _verbose=False, _isot=get_isot()):
    if _req is not None and hasattr(_req, 'status_code') and \
            http_status(int(_req.status_code)) and hasattr(_req, 'text'):
        if _req.status_code == 200:
            try:
                _json = json.loads(_req.text)
            except:
                _json = {}
            if verify_keys(_json, MMT_JSON_KEYS):
                if _verbose:
                    print(f"{_isot}> received (json) {_json}")
                return _json
            else:
                if _verbose:
                    print(f"{_isot}> received (text) {_req.text}")
                return _req.text
        else:
            if _verbose:
                print(f"{_isot}> received (text) {_req.text}, status={_req.status_code}")
            return _req.text
