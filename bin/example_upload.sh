#!/bin/bash
_id=${1:-6621}
python3 ${MMT_SRC}/mmt.py --action=UPLOAD --targetid=${_id} --verbose
