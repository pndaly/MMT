#!/usr/bin/env python3


# +
# import(s)
# -
from __init__ import *
from mmt_token import MMT_TOKEN

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
    _isot = get_isot()
    target_id = kwargs['target_id'] if \
        ('target_id' in kwargs and isinstance(kwargs['target_id'], int) and kwargs['target_id'] > 0) \
        else MMT_TARGET_ID
    verbose = kwargs['verbose'] if \
        ('verbose' in kwargs and isinstance(kwargs['verbose'], bool)) \
        else False

    if verbose:
        print(f"{_isot}> delete_action(kwargs={kwargs})")

    # execute
    _data, _req = 'null', None
    try:
        if verbose:
            print(f"{_isot}> delete_action() sends {_data} to {MMT_URL}/{target_id}/")
        _req = requests.delete(url=f'{MMT_URL}/{target_id}')
    except:
        if verbose:
            print(f"failed to complete request, _req={_req}")
    else:
        parse_response(_req=_req, _verbose=verbose, _isot=_isot)


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
    verbose = kwargs['verbose'] if \
        ('verbose' in kwargs and isinstance(kwargs['verbose'], bool)) \
        else False
    _isot = get_isot()

    if verbose:
        print(f"{_isot}> get_action(kwargs={kwargs})")

    # execute
    _data, _req = 'null', None
    try:
        if verbose:
            print(f"{_isot}> get_action() sends {_data} to {MMT_URL}/{target_id}/")
        _req = requests.get(url=f'{MMT_URL}/{target_id}')
    except:
        if verbose:
            print(f"failed to complete request, _req={_req}")
    else:
        parse_response(_req=_req, _verbose=verbose, _isot=_isot)


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
    target_id = kwargs['target_id'] if \
        ('target_id' in kwargs and isinstance(kwargs['target_id'], int) and kwargs['target_id'] > 0) \
        else MMT_TARGET_ID
    token = kwargs['token'] if \
        ('token' in kwargs and isinstance(kwargs['token'], str) and kwargs['token'] != '') \
        else MMT_TOKEN
    verbose = kwargs['verbose'] if \
        ('verbose' in kwargs and isinstance(kwargs['verbose'], bool)) \
        else False
    _isot = get_isot()

    if verbose:
        print(f"{_isot}> get_action(kwargs={kwargs})")

    # execute
    _data, _req = {**payload, **{'catalog_id': catalog_id, 'program_id': program_id, 'token': token}}, None
    try:
        if verbose:
            print(f"{_isot}> post_action() sends {_data} to {MMT_URL}/{target_id}/")
        _req = requests.post(url=f'{MMT_URL}/{target_id}', data=_data)
    except:
        if verbose:
            print(f"failed to complete request, _req={_req}")
    else:
        parse_response(_req=_req, _verbose=verbose, _isot=_isot)


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
    verbose = kwargs['verbose'] if \
        ('verbose' in kwargs and isinstance(kwargs['verbose'], bool)) \
        else False
    _isot = get_isot()

    if verbose:
        print(f"{_isot}> put_action(kwargs={kwargs})")

    # change _new['mask'] to _new['maskid']
    _data, _req = {**payload, **{'catalog_id': catalog_id, 'program_id': program_id, 'token': token}}, None
    _v = _data.pop('mask', None)
    if isinstance(_v, dict) and 'id' in _v and 'maskid' not in _data:
        _data['maskid'] = _v['id']

    # execute
    try:
        if verbose:
            print(f"{_isot}> put_action() sends {_data} to {MMT_URL}/{target_id}/")
        _req = requests.put(url=f'{MMT_URL}/{target_id}/', data=_data)
    except:
        if verbose:
            print(f"failed to complete request, _req={_req}")
    else:
        parse_response(_req=_req, _verbose=verbose, _isot=_isot)


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
    verbose = kwargs['verbose'] if \
        ('verbose' in kwargs and isinstance(kwargs['verbose'], bool)) \
        else False
    _isot = get_isot()

    if verbose:
        print(f"{_isot}> upload_action(kwargs={kwargs})")

    # convert to png (if required)
    _png = None
    if file.endswith('fits') or file.endswith('fits.gz'):
        _png = fits_to_png(file, verbose)
        _png = open(_png, 'rb')
    elif file.endswith('png') or file.endswith('jpg'):
        _png = open(file, 'rb')

    # execute
    _data, _files, _req = {'type': 'finding_chart', 'token': token, 'catalog_id': str(catalog_id),
                           'program_id': str(program_id), 'target_id': str(target_id)}, \
                          {'finding_chart_file': _png}, None
    try:
        if verbose:
            print(f"{_isot}> upload_action() sends {_data} to {MMT_URL}/{target_id}")
            print(f"{_isot}> upload_action() sends {_png} to {MMT_URL}/{target_id}")
        _req = requests.post(url=f'{MMT_URL}/{target_id}', files=_files, data=_data)
    except Exception as _e:
        if verbose:
            print(f"failed to complete request, _req={_req}, error={_e}")
    else:
        parse_response(_req=_req, _verbose=verbose, _isot=_isot)


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
               program_id=MMT_PROGRAM_ID, target_id=MMT_TARGET_ID, token=MMT_TOKEN, verbose=False):

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
    _verbose = verbose if isinstance(verbose, bool) else False

    # execute
    if _action is not None:
        _action(**{'action': action.upper(), 'catalog_id': _catalog_id, 'file': _file, 'payload': _payload,
                   'program_id': _program_id, 'target_id': _target_id, 'token': _token, 'verbose': _verbose})


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

    # execute
    mmt_target(action=args.action, catalog_id=int(args.catalog_id), file=args.file, payload=args.payload,
               program_id=int(args.program_id), target_id=int(args.target_id), token=args.token,
               verbose=bool(args.verbose))
