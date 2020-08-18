#!/usr/bin/env python3


# +
# import(s)
# -
from src.mmt_token import *

import argparse
import shutil


# +
# __doc__
# -
__doc__ = """
  % python3 mmt.py --help
"""


# +
# function: delete_action()
# -
# noinspection PyBroadException
def delete_action(**kwargs):

    # check input(s)
    if kwargs is None or not isinstance(kwargs, dict) or kwargs == {}:
        return

    # get variable(s)
    targetid = kwargs['targetid'] if \
        ('targetid' in kwargs and isinstance(kwargs['targetid'], int) and kwargs['targetid'] > 0) \
        else MMT_TARGETID
    log = kwargs['log'] if ('log' in kwargs and isinstance(kwargs['log'], logging.Logger)) else None
    if log:
        log.debug(f"delete_action(kwargs={kwargs})")

    # execute
    _data, _req = 'null', None
    if log:
        log.debug(f"sending {_data} to {MMT_URL}/{targetid}/")
    try:
        _req = requests.delete(url=f'{MMT_URL}/{targetid}')
    except Exception as _e:
        if log:
            log.error(f"failed to complete DELETE request, _req={_req}, error={_e}")
    else:
        return parse_response(_req=_req, _log=log)


# +
# function: get_action()
# -
# noinspection PyBroadException
def get_action(**kwargs):

    # check input(s)
    if kwargs is None or not isinstance(kwargs, dict) or kwargs == {}:
        return

    # get variable(s)
    targetid = kwargs['targetid'] if \
        ('targetid' in kwargs and isinstance(kwargs['targetid'], int) and kwargs['targetid'] > 0) \
        else MMT_TARGETID
    log = kwargs['log'] if ('log' in kwargs and isinstance(kwargs['log'], logging.Logger)) else None
    if log:
        log.debug(f"get_action(kwargs={kwargs})")

    # execute
    _data, _req = 'null', None
    if log:
        log.debug(f"sending {_data} to {MMT_URL}/{targetid}/")
    try:
        _req = requests.get(url=f'{MMT_URL}/{targetid}')
    except Exception as _e:
        if log:
            log.error(f"failed to complete GET request, _req={_req}, error={_e}")
    else:
        return parse_response(_req=_req, _log=log)


# +
# function: post_action()
# -
# noinspection PyBroadException
def post_action(**kwargs):

    # check input(s)
    if kwargs is None or not isinstance(kwargs, dict) or kwargs == {}:
        return

    # get variable(s)
    catalogid = kwargs['catalogid'] if \
        ('catalogid' in kwargs and isinstance(kwargs['catalogid'], int) and kwargs['catalogid'] > 0) \
        else MMT_CATALOGID
    payload = kwargs['payload'] if \
        ('payload' in kwargs and isinstance(kwargs['payload'], dict)) \
        else {}
    programid = kwargs['programid'] if \
        ('programid' in kwargs and isinstance(kwargs['programid'], int) and kwargs['programid'] > 0) \
        else MMT_PROGRAMID
    token = kwargs['token'] if \
        ('token' in kwargs and isinstance(kwargs['token'], str) and kwargs['token'] != '') \
        else MMT_TOKEN
    log = kwargs['log'] if ('log' in kwargs and isinstance(kwargs['log'], logging.Logger)) else None
    if log:
        log.debug(f"post_action(kwargs={kwargs})")

    # execute
    _data, _req, _otype = None, None, None
    if 'observationtype' not in payload:
        if log:
            log.error(f"failed to find key 'observationtype' in {payload}")
        return
    else:
        _otype = payload['observationtype'].strip().lower()
        if _otype == 'imaging':
            _data = verify_imaging_payload(payload=payload, _log=log)
        elif _otype == 'longslit':
            _data = verify_spectroscopy_payload(payload=payload, _log=log)
        elif _otype == 'mask':
            _data = verify_imaging_payload(payload=payload, _log=log)
        else:
            if log:
                log.error(f"invalid key 'observationtype'={_otype}")
            return

    _data = {**_data, **{'catalogid': catalogid, 'program_id': programid, 'token': token}}

    if log:
        log.debug(f"sending {_data} to {MMT_URL}/?token={token}")
    try:
        _req = requests.post(url=f'{MMT_URL}/?{token}', json=_data)
    except Exception as _e:
        if log:
            log.error(f"failed to complete POST request, _req={_req}, error={_e}")
    else:
        return parse_response(_req=_req, _log=log)


# +
# function: put_action()
# -
# noinspection PyBroadException
def put_action(**kwargs):

    # check input(s)
    if kwargs is None or not isinstance(kwargs, dict) or kwargs == {}:
        return

    # get variable(s)
    catalogid = kwargs['catalogid'] if \
        ('catalogid' in kwargs and isinstance(kwargs['catalogid'], int) and kwargs['catalogid'] > 0) \
        else MMT_CATALOGID
    payload = kwargs['payload'] if \
        ('payload' in kwargs and isinstance(kwargs['payload'], dict)) \
        else {}
    programid = kwargs['programid'] if \
        ('programid' in kwargs and isinstance(kwargs['programid'], int) and kwargs['programid'] > 0) \
        else MMT_PROGRAMID
    targetid = kwargs['targetid'] if \
        ('targetid' in kwargs and isinstance(kwargs['targetid'], int) and kwargs['targetid'] > 0) \
        else MMT_TARGETID
    token = kwargs['token'] if \
        ('token' in kwargs and isinstance(kwargs['token'], str) and kwargs['token'] != '') \
        else MMT_TOKEN
    log = kwargs['log'] if ('log' in kwargs and isinstance(kwargs['log'], logging.Logger)) else None
    if log:
        log.debug(f"put_action(kwargs={kwargs})")

    # execute
    _data, _req = {**payload, **{'catalogid': catalogid, 'program_id': programid, 'token': token}}, None
    if log:
        log.debug(f"sending {_data} to {MMT_URL}/{targetid}/")
    try:
        _req = requests.put(url=f'{MMT_URL}/{targetid}/', json=_data)
    except Exception as _e:
        if log:
            log.error(f"failed to complete PUT request, _req={_req}, error={_e}")
    else:
        return parse_response(_req=_req, _log=log)


# +
# function: upload_action()
# -
# noinspection PyBroadException
def upload_action(**kwargs):

    # check input(s)
    if kwargs is None or not isinstance(kwargs, dict) or kwargs == {}:
        return

    # get variable(s)
    catalogid = kwargs['catalogid'] if \
        ('catalogid' in kwargs and isinstance(kwargs['catalogid'], int) and kwargs['catalogid'] > 0) \
        else MMT_CATALOGID
    file = os.path.abspath(os.path.expanduser(kwargs['file'])) if \
        ('file' in kwargs and isinstance(kwargs['file'], str) and kwargs['file'] != '' and
         os.path.exists(os.path.abspath(os.path.expanduser(kwargs['file'])))) else ''
    programid = kwargs['programid'] if \
        ('programid' in kwargs and isinstance(kwargs['programid'], int) and kwargs['programid'] > 0) \
        else MMT_PROGRAMID
    targetid = kwargs['targetid'] if \
        ('targetid' in kwargs and isinstance(kwargs['targetid'], int) and kwargs['targetid'] > 0) \
        else MMT_TARGETID
    token = kwargs['token'] if \
        ('token' in kwargs and isinstance(kwargs['token'], str) and kwargs['token'] != '') \
        else MMT_TOKEN
    log = kwargs['log'] if ('log' in kwargs and isinstance(kwargs['log'], logging.Logger)) else None
    if log:
        log.debug(f"upload_action(kwargs={kwargs})")

    # if file is not specified, use SDSS
    if file == '':
        _json = get_action(**{'targetid': targetid})
        _ra, _dec = _json['ra'], _json['dec']
        file = get_finder_chart(**{'ra': _ra, 'dec': _dec, 'log': log, 'jpg': f'{targetid}.jpg'})
        file = jpg_to_png(_jpg=file, _log=log)

    # convert to png (if required)
    elif file.endswith('fits') or file.endswith('fits.gz'):
        file = fits_to_png(fits_file=file, _log=log)
        _file = f'{os.getcwd()}/{targetid}.png'
        file = shutil.move(file, _file)

    # execute
    _img = open(os.path.basename(file), 'rb')
    _data, _files, _req = {'type': 'finding_chart', 'token': token, 'catalogid': catalogid,
                           'program_id': programid, 'target_id': targetid,
                           'findingchartfilename': os.path.basename(file)}, {'finding_chart_file': _img}, None
    if log:
        log.debug(f"file={file}")
        log.debug(f"sending {_data} to {MMT_URL}/{targetid}/")
        log.debug(f"sending {_img} to {MMT_URL}/{targetid}/")
    try:
        _req = requests.post(url=f'{MMT_URL}/{targetid}/', files=_files, data=_data)
    except Exception as _e:
        if log:
            log.error(f"failed to complete UPLOAD request, _req={_req}, error={_e}")
    else:
        return parse_response(_req=_req, _log=log)


# +
# action(s)
# -
HTTP_ACTIONS = {'DELETE': delete_action, 'GET': get_action, 'POST': post_action, 'PUT': put_action,
                'UPLOAD': upload_action}


# +
# function: mmt_target()
# -
# noinspection PyBroadException
def mmt_target(action='GET', catalogid=MMT_CATALOGID, file='', payload='',
               programid=MMT_PROGRAMID, targetid=MMT_TARGETID, token=MMT_TOKEN, log=None):

    # set variable(s)
    _action = HTTP_ACTIONS.get(action.upper(), None)
    _catalogid = catalogid if (isinstance(catalogid, int) and catalogid > 0) else MMT_CATALOGID
    _file = file if (isinstance(file, str) and file.strip() != '') else ''
    try:
        _payload = json.loads(payload)
    except:
        _payload = {}
    _programid = programid if (isinstance(programid, int) and programid > 0) else MMT_PROGRAMID
    _targetid = targetid if (isinstance(targetid, int) and targetid > 0) else MMT_TARGETID
    _token = token if (isinstance(token, str) and token.strip() != '') else MMT_TOKEN
    log = log if isinstance(log, logging.Logger) else None

    # execute
    if _action is not None:
        _action(**{'action': action.upper(), 'catalogid': _catalogid, 'file': _file, 'payload': _payload,
                   'programid': _programid, 'targetid': _targetid, 'token': _token, 'log': log})


# +
# main()
# -
if __name__ == '__main__':

    # noinspection PyTypeChecker
    _p = argparse.ArgumentParser(description=f'MMT Target Loader', formatter_class=argparse.RawTextHelpFormatter)
    _p.add_argument(f'--action', default='GET',
                    help=f"""Action, defaults to '%(default)s', choices: {list(HTTP_ACTIONS.keys())}""")
    _p.add_argument(f'--catalogid', default=MMT_CATALOGID, help=f"""Catalog ID, defaults to %(default)s""")
    _p.add_argument(f'--file', default='', help=f"""File, defaults to '%(default)s'""")
    _p.add_argument(f'--payload', default='{}', help=f"""Payload, defaults to %(default)s""")
    _p.add_argument(f'--programid', default=MMT_PROGRAMID, help=f"""Program ID, defaults to %(default)s""")
    _p.add_argument(f'--targetid', default=MMT_TARGETID, help=f"""Target ID, defaults to %(default)s""")
    _p.add_argument(f'--token', default=MMT_TOKEN, help=f"""Token, defaults to %(default)s""")
    _p.add_argument(f'--verbose', default=False, action='store_true', help=f'if present, produce verbose output')

    # get command line argument(s)
    args = _p.parse_args()

    # get logger (if required)
    _log = Logger('MMT').logger if bool(args.verbose) else None

    # execute
    mmt_target(action=args.action, catalogid=int(args.catalogid), file=args.file, payload=args.payload,
               programid=int(args.programid), targetid=int(args.targetid), token=args.token, log=_log)
