#!/bin/bash
_id=${1:-6593}
python3 ${MMT_SRC}/mmt.py --action=PUT --payload='{"filter": "z"}' --targetid=${_id} --verbose
