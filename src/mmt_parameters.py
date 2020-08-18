#!/usr/bin/env python3


# +
# import(s)
# -
from src import *
from src.mmt_token import *

import re


# +
# MMT parameter(s)
# -
MMT_PRIORITY = (1, 2, 3)
MMT_PHOTOMETRIC = (0, 1)
MMT_TOO = (0, 1)
MMT_OBSERVATION_TYPE = ('imaging', 'longslit', 'mask')

MMT_IMAGING_FILTERS = ('g', 'r', 'i', 'z')
MMT_IMAGING_MASKS = (110, )

MMT_SPECTROSCOPY_FILTERS = ('LP3800', 'LP3500')
MMT_SPECTROSCOPY_GRATINGS = {
    '270': [{'min': 5501.0, 'max': 7838.0}],
    '600': [{'min': 5146.0, 'max': 8783.0}],
    '1000': [
        {'min': 4108.0, 'max': 4683.0}, {'min': 5181.0, 'max': 7273.0}, {'min': 7363.0, 'max': 7967.0},
        {'min': 8153.0, 'max': 8772.0}, {'min': 8897.0, 'max': 9279.0}
    ]
}
MMT_SPECTROSCOPY_MASKS = {
    'Longslit0_75': 113, 'Longslit1': 111, 'Longslit1_25': 131, 'Longslit1_5': 114, 'Longslit5': 112}
MMT_SPECTROSCOPY_SLITWIDTH = [_k for _k in list(MMT_SPECTROSCOPY_MASKS.keys())]


# +
# default payload(s)
# -
MMT_IMAGING_PAYLOAD = {
    'centralwavelength': 'null',
    'dec': '', 
    'dec_decimal': math.nan, 
    'epoch': 2000.0, 
    'exposuretime': math.nan, 
    'filter': MMT_IMAGING_FILTERS[0], 
    'grating': 'null',
    'instrumentid': MMT_INSTRUMENTID, 
    'magnitude': math.nan, 
    'maskid': MMT_IMAGING_MASKS[0],
    'notes': 'default imaging payload', 
    'notify': 1, 
    'numberexposures': 1, 
    'objectid': get_hash(),
    'observationtype': 'imaging', 
    'onevisitpernight': 0, 
    'pa': 0.0, 
    'photometric': MMT_PHOTOMETRIC[0], 
    'pm_dec': 0.0,
    'pm_ra': 0.0, 
    'priority': MMT_PRIORITY[0], 
    'ra': '', 
    'ra_decimal': math.nan,
    'visits': 1}

MMT_SPECTROSCOPY_PAYLOAD = {
    'centralwavelength': math.nan, 
    'dec': '', 
    'dec_decimal': math.nan, 
    'epoch': 2000.0,
    'exposuretime': math.nan, 
    'filter': MMT_SPECTROSCOPY_FILTERS[0],
    'grating': list(MMT_SPECTROSCOPY_GRATINGS.keys())[0],
    'instrumentid': MMT_INSTRUMENTID, 
    'magnitude': math.nan,
    'maskid': MMT_SPECTROSCOPY_MASKS['Longslit1'], 
    'notes': 'default spectroscopy payload',
    'notify': 1, 
    'numberexposures': 1, 
    'objectid': get_hash(), 
    'observationtype': 'longslit',
    'onevisitpernight': 1, 
    'pa': 0.0,
    'photometric': MMT_PHOTOMETRIC[0], 
    'pm_dec': 0.0, 
    'pm_ra': 0.0,
    'priority': MMT_PRIORITY[0], 
    'ra': '', 
    'ra_decimal': math.nan, 
    'slitwidth': 'Longslit1',
    'visits': 1
}


# +
# function: verify_spectroscopy_wavelength()
# -
# noinspection PyBroadException
def verify_spectroscopy_wavelength(_grating='270', _value=6669.5):
    if _grating.strip() in MMT_SPECTROSCOPY_GRATINGS:
        try:
            for _i in range(len(MMT_SPECTROSCOPY_GRATINGS[_grating])):
                if MMT_SPECTROSCOPY_GRATINGS[_grating][_i]['min'] <= float(_value) \
                        <= MMT_SPECTROSCOPY_GRATINGS[_grating][_i]['max']:
                    return True
        except:
            pass
    return False


# +
# function: verify_common_payload()
# -
def verify_common_payload(_data=None, _log=None):

    # check input(s)
    _log = _log if isinstance(_log, logging.Logger) else None
    if _data is None or not isinstance(_data, dict) or _data == {}:
        return {}

    # reject critical value(s) that are not set properly
    if re.match(DEC_PATTERN, _data['dec']) is None:
        if _log:
            _log.error(f"invalid dec {_data['dec']}")
        return {}
    if not isinstance(_data['exposuretime'], float) or _data['exposuretime'] == math.nan or _data['exposuretime'] < 0.0:
        if _log:
            _log.error(f"invalid exposuretime {_data['exposuretime']}")
        return {}
    if not isinstance(_data['magnitude'], float) or _data['magnitude'] == math.nan:
        if _log:
            _log.error(f"invalid magnitude {_data['magnitude']}")
        return {}
    if not isinstance(_data['observationtype'], str) or \
            _data['observationtype'].strip().lower() not in MMT_OBSERVATION_TYPE:
        if _log:
            _log.error(f"invalid observationtype {_data['observationtype']}")
        return {}
    if not isinstance(_data['objectid'], str) or _data['objectid'].strip() == '':
        if _log:
            _log.error(f"invalid objectid {_data['objectid']}")
        return {}
    if re.match(RA_PATTERN, _data['ra']) is None:
        if _log:
            _log.error(f"invalid ra {_data['ra']}")
        return {}

    # set value(s)
    _data['dec_decimal'] = dec_to_decimal(_data['dec'])
    _data['ra_decimal'] = ra_to_decimal(_data['ra'])

    # reset value(s) that are out-of-range
    if not isinstance(_data['numberexposures'], int) or _data['numberexposures'] < 0:
        _data['numberexposures'] = 1
    if not isinstance(_data['photometric'], int) or _data['photometric'] not in MMT_PHOTOMETRIC:
        _data['photometric'] = MMT_IMAGING_PAYLOAD['photometric']
    if not isinstance(_data['priority'], int) or _data['priority'] not in MMT_PRIORITY:
        _data['priority'] = MMT_IMAGING_PAYLOAD['priority']

    # return
    return _data


# +
# function: verify_imaging_payload()
# -
def verify_imaging_payload(payload=None, _log=None):

    # check input(s)
    _log = _log if isinstance(_log, logging.Logger) else None
    if payload is None or not isinstance(payload, dict) or payload == {}:
        return {}

    # combine payload(s)
    _data = {**MMT_IMAGING_PAYLOAD, **payload}
    _data = verify_common_payload(_data=_data, _log=_log)

    # reject critical value(s) that are not set properly
    if _data['filter'] not in MMT_IMAGING_FILTERS:
        if _log:
            _log.error(f"invalid filter {_data['filter']}")
        return {}

    # reset value(s) that are out-of-range
    if not isinstance(_data['maskid'], int) or _data['maskid'] not in MMT_IMAGING_MASKS:
        _data['maskid'] = MMT_IMAGING_MASKS[0]
    if not isinstance(_data['pa'], float) or _data['pa'] == math.nan or -360.0 <= _data['pa'] <= 360.0:
        _data['pa'] = MMT_IMAGING_PAYLOAD['pa']
    if not isinstance(_data['pm_dec'], float) or _data['pm_dec'] == math.nan:
        _data['pm_dec'] = MMT_IMAGING_PAYLOAD['pm_dec']
    if not isinstance(_data['pm_ra'], float) or _data['pm_ra']:
        _data['pm_ra'] = MMT_IMAGING_PAYLOAD['pm_ra']

    # return
    return _data


# +
# function: verify_spectroscopy_payload()
# -
def verify_spectroscopy_payload(payload=None, _log=None):

    # check input(s)
    _log = _log if isinstance(_log, logging.Logger) else None
    if payload is None or not isinstance(payload, dict) or payload == {}:
        return {}

    # combine payload(s)
    _data = {**MMT_SPECTROSCOPY_PAYLOAD, **payload}
    _data = verify_common_payload(_data=_data, _log=_log)

    # reject critical value(s) that are not set properly
    if _data['filter'] not in MMT_SPECTROSCOPY_FILTERS:
        if _log:
            _log.error(f"invalid filter {_data['filter']}")
        return {}
    if not isinstance(_data['centralwavelength'], float) or _data['centralwavelength'] == math.nan:
        if _log:
            _log.error(f"invalid central wavelength {_data['centralwavelength']}")
        return {}
    if not isinstance(_data['grating'], str) or _data['grating'] not in MMT_SPECTROSCOPY_GRATINGS:
        if _log:
            _log.error(f"invalid grating {_data['grating']}")
        return {}
    if not isinstance(_data['maskid'], int) or _data['maskid'] not in MMT_SPECTROSCOPY_MASKS.values():
        if _log:
            _log.error(f"invalid maskid {_data['maskid']}")
        return {}
    if not isinstance(_data['slitwidth'], str) or _data['slitwidth'] not in MMT_SPECTROSCOPY_GRATINGS:
        if _log:
            _log.error(f"invalid slit width {_data['slitwidth']}")
        return {}

    # check wavelength / grating combination
    if not verify_spectroscopy_wavelength(_data['grating'], _data['centralwavelength']):
        if _log:
            _log.error(f"invalid grating wavelength {_data['grating']} / {_data['centralwavelength']}")
        return {}

    # reset value(s) that are out-of-range
    if not isinstance(_data['pa'], float) or _data['pa'] == math.nan or -360.0 <= _data['pa'] <= 360.0:
        _data['pa'] = MMT_SPECTROSCOPY_PAYLOAD['pa']
    if not isinstance(_data['pm_dec'], float) or _data['pm_dec'] == math.nan:
        _data['pm_dec'] = MMT_SPECTROSCOPY_PAYLOAD['pm_dec']
    if not isinstance(_data['pm_ra'], float) or _data['pm_ra']:
        _data['pm_ra'] = MMT_SPECTROSCOPY_PAYLOAD['pm_ra']

    # return
    return _data
