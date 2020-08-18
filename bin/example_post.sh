#!/bin/bash

python3 ${MMT_SRC}/mmt.py --action=POST --payload='{"dec": "+33:57:36", "epoch": 2000.0, "exposuretime": 300.0, "filter": "r", "magnitude": 15.0, "notes": "Stephans Quintet is a grouping of five galaxies of which contains the first compact galaxy group discovered",
"numberexposures": 5, "objectid": "Stephans_Quintet", "observationtype": "imaging", "pa": 0.0, "ra": "22:35:58", "visits": 1}' --verbose
