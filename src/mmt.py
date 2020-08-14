#!/usr/bin/env python3


# +
# import(s)
# -
from src import *
from src.mmt_token import *

import argparse
import requests


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

    # set variable(s)
    target_id = kwargs['target_id'] if \
        ('target_id' in kwargs and isinstance(kwargs['target_id'], int) and kwargs['target_id'] > 0) \
        else MMT_TARGET_ID

    # get logger
    log = kwargs['log'] if ('log' in kwargs and isinstance(kwargs['log'], logging.Logger)) else None
    if log:
        log.info(f"delete_action(kwargs={kwargs})")

    # execute
    _data, _req = 'null', None
    if log:
        log.info(f"sending {_data} to {MMT_URL}/{target_id}/")
    try:
        _req = requests.delete(url=f'{MMT_URL}/{target_id}')
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

    # set variable(s)
    target_id = kwargs['target_id'] if \
        ('target_id' in kwargs and isinstance(kwargs['target_id'], int) and kwargs['target_id'] > 0) \
        else MMT_TARGET_ID

    # get logger
    log = kwargs['log'] if ('log' in kwargs and isinstance(kwargs['log'], logging.Logger)) else None
    if log:
        log.info(f"get_action(kwargs={kwargs})")

    # execute
    _data, _req = 'null', None
    if log:
        log.info(f"sending {_data} to {MMT_URL}/{target_id}/")
    try:
        _req = requests.get(url=f'{MMT_URL}/{target_id}')
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

    # set variable(s)
    catalog_id = kwargs['catalog_id'] if \
        ('catalog_id' in kwargs and isinstance(kwargs['catalog_id'], int) and kwargs['catalog_id'] > 0) \
        else MMT_CATALOG_ID
    payload = kwargs['payload'] if \
        ('payload' in kwargs and isinstance(kwargs['payload'], dict)) \
        else {}
    program_id = kwargs['program_id'] if \
        ('program_id' in kwargs and isinstance(kwargs['program_id'], int) and kwargs['program_id'] > 0) \
        else MMT_PROGRAM_ID
    token = kwargs['token'] if \
        ('token' in kwargs and isinstance(kwargs['token'], str) and kwargs['token'] != '') \
        else MMT_TOKEN

    # get logger
    log = kwargs['log'] if ('log' in kwargs and isinstance(kwargs['log'], logging.Logger)) else None
    if log:
        log.info(f"post_action(kwargs={kwargs})")

    # execute
    _data, _req = {**MMT_NULL_IMAGING, **payload}, None
    if log:
        log.info(f"_data={_data})")
    if verify_keys(_data, MMT_JSON_KEYS):

        # add variable(s)
        _data['ra_decimal'] = ra_to_decimal(_data['ra'])
        _data['dec_decimal'] = dec_to_decimal(_data['dec'])
        _data['submitted'] = get_isot().replace('T', ' ')
        _data['modified'] = get_isot().replace('T', ' ')

        if _data['findingchartfilename'] is None or _data['findingchartfilename'].strip() == '' or \
                not os.path.abspath(os.path.expanduser(_data['findingchartfilename'])):
            _data['findingchartfilename'] = get_finder_chart(**{'ra': _data['ra'], 'dec': _data['dec']})
        _data['findingchartfilename'] = os.path.basename(_data['findingchartfilename'])
        _data['image'] = open(_data['findingchartfilename'], 'rb')
        _data['files'] = {'finding_chart_file': _data['image']}
        _data['type'] = 'finding_chart'

        _data.pop('id', None)
        _v = _data.pop('mask', None)
        if isinstance(_v, dict) and 'id' in _v and 'maskid' not in _data:
            _data['maskid'] = _v['id']

        _data = {**_data, **{'catalog_id': catalog_id, 'program_id': program_id, 'token': token}}
        if log:
            log.info(f"sending {_data} to {MMT_URL}/?token={token}")
        try:
            _req = requests.post(url=f'{MMT_URL}/?{token}', files=_data['files'], data=_data)
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

    # set variable(s)
    catalog_id = kwargs['catalog_id'] if \
        ('catalog_id' in kwargs and isinstance(kwargs['catalog_id'], int) and kwargs['catalog_id'] > 0) \
        else MMT_CATALOG_ID
    payload = kwargs['payload'] if \
        ('payload' in kwargs and isinstance(kwargs['payload'], dict)) \
        else {}
    program_id = kwargs['program_id'] if \
        ('program_id' in kwargs and isinstance(kwargs['program_id'], int) and kwargs['program_id'] > 0) \
        else MMT_PROGRAM_ID
    target_id = kwargs['target_id'] if \
        ('target_id' in kwargs and isinstance(kwargs['target_id'], int) and kwargs['target_id'] > 0) \
        else MMT_TARGET_ID
    token = kwargs['token'] if \
        ('token' in kwargs and isinstance(kwargs['token'], str) and kwargs['token'] != '') \
        else MMT_TOKEN

    # get logger
    log = kwargs['log'] if ('log' in kwargs and isinstance(kwargs['log'], logging.Logger)) else None
    if log:
        log.info(f"put_action(kwargs={kwargs})")

    # change _new['mask'] to _new['maskid']
    _data, _req = {**payload, **{'catalog_id': catalog_id, 'program_id': program_id, 'token': token}}, None
    _v = _data.pop('mask', None)
    if isinstance(_v, dict) and 'id' in _v and 'maskid' not in _data:
        _data['maskid'] = _v['id']

    # execute
    if log:
        log.info(f"sending {_data} to {MMT_URL}/{target_id}/")
    try:
        _req = requests.put(url=f'{MMT_URL}/{target_id}/', data=_data)
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

    # set variable(s)
    catalog_id = kwargs['catalog_id'] if \
        ('catalog_id' in kwargs and isinstance(kwargs['catalog_id'], int) and kwargs['catalog_id'] > 0) \
        else MMT_CATALOG_ID
    file = os.path.abspath(os.path.expanduser(kwargs['file'])) if \
        ('file' in kwargs and isinstance(kwargs['file'], str) and kwargs['file'] != '' and
         os.path.exists(os.path.abspath(os.path.expanduser(kwargs['file'])))) else ''
    program_id = kwargs['program_id'] if \
        ('program_id' in kwargs and isinstance(kwargs['program_id'], int) and kwargs['program_id'] > 0) \
        else MMT_PROGRAM_ID
    target_id = kwargs['target_id'] if \
        ('target_id' in kwargs and isinstance(kwargs['target_id'], int) and kwargs['target_id'] > 0) \
        else MMT_TARGET_ID
    token = kwargs['token'] if \
        ('token' in kwargs and isinstance(kwargs['token'], str) and kwargs['token'] != '') \
        else MMT_TOKEN

    # get logger
    log = kwargs['log'] if ('log' in kwargs and isinstance(kwargs['log'], logging.Logger)) else None
    if log:
        log.info(f"upload_action(kwargs={kwargs})")

    # if file is not specified, use SDSS
    if file == '':
        _json = get_action(**{'target_id': target_id})
        _ra, _dec = _json['ra'], _json['dec']
        file = get_finder_chart(**{'ra': _ra, 'dec': _dec, 'log': log})
        file = jpg_to_png(file, log)

    # convert to png (if required)
    elif file.endswith('fits') or file.endswith('fits.gz'):
        file = fits_to_png(file, log)

    # execute
    _img = open(os.path.basename(file), 'rb')
    _data, _files, _req = {'type': 'finding_chart', 'token': token, 'catalog_id': str(catalog_id),
                           'program_id': str(program_id), 'target_id': str(target_id),
                           'findingchartfilename': os.path.basename(file)}, {'finding_chart_file': _img}, None
    if log:
        log.info(f"file={file}")
        log.info(f"sending {_data} to {MMT_URL}/{target_id}/")
        log.info(f"sending {_img} to {MMT_URL}/{target_id}/")
    try:
        _req = requests.put(url=f'{MMT_URL}/{target_id}/', files=_files, data=_data)
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
def mmt_target(action='GET', catalog_id=MMT_CATALOG_ID, file='', payload='',
               program_id=MMT_PROGRAM_ID, target_id=MMT_TARGET_ID, token=MMT_TOKEN, log=None):

    # set variable(s)
    _action = HTTP_ACTIONS.get(action.upper(), None)
    _catalog_id = catalog_id if (isinstance(catalog_id, int) and catalog_id > 0) else MMT_CATALOG_ID
    _file = file if (isinstance(file, str) and file.strip() != '') else ''
    try:
        _payload = json.loads(payload)
    except:
        _payload = {}
    _program_id = program_id if (isinstance(program_id, int) and program_id > 0) else MMT_PROGRAM_ID
    _target_id = target_id if (isinstance(target_id, int) and target_id > 0) else MMT_TARGET_ID
    _token = token if (isinstance(token, str) and token.strip() != '') else MMT_TOKEN
    log = log if isinstance(log, logging.Logger) else None

    # execute
    if _action is not None:
        _action(**{'action': action.upper(), 'catalog_id': _catalog_id, 'file': _file, 'payload': _payload,
                   'program_id': _program_id, 'target_id': _target_id, 'token': _token, 'log': log})


# +
# main()
# -
if __name__ == '__main__':

    # noinspection PyTypeChecker
    _p = argparse.ArgumentParser(description=f'MMT Target Loader', formatter_class=argparse.RawTextHelpFormatter)
    _p.add_argument(f'--action', default='GET',
                    help=f"""Action, defaults to '%(default)s', choices: {list(HTTP_ACTIONS.keys())}""")
    _p.add_argument(f'--catalog_id', default=MMT_CATALOG_ID, help=f"""Catalog ID, defaults to %(default)s""")
    _p.add_argument(f'--file', default='', help=f"""File, defaults to '%(default)s'""")
    _p.add_argument(f'--payload', default='{}', help=f"""Payload, defaults to %(default)s""")
    _p.add_argument(f'--program_id', default=MMT_PROGRAM_ID, help=f"""Program ID, defaults to %(default)s""")
    _p.add_argument(f'--target_id', default=MMT_TARGET_ID, help=f"""Target ID, defaults to %(default)s""")
    _p.add_argument(f'--token', default=MMT_TOKEN, help=f"""Token, defaults to %(default)s""")
    _p.add_argument(f'--verbose', default=False, action='store_true', help=f'if present, produce verbose output')

    # get command line argument(s)
    args = _p.parse_args()

    # get logger (if required)
    _log = Logger('MMT').logger if bool(args.verbose) else None

    # execute
    mmt_target(action=args.action, catalog_id=int(args.catalog_id), file=args.file, payload=args.payload,
               program_id=int(args.program_id), target_id=int(args.target_id), token=args.token, log=_log)
