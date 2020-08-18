#!/bin/bash
_id=${1:-6593}
python3 ${MMT_SRC}/mmt.py --action=GET --targetid=${_id} --verbose
