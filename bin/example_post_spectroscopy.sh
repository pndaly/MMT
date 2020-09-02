#!/bin/bash

python3 ${MMT_SRC}/mmt.py --action=POST --payload='{"centralwavelength": 6436.92, "dec": "+33:57:36", "epoch": 2000.0, "exposuretime": 360.0, "filter": "LP3800", "grating": 600, "magnitude": 20.0, "maskid": 111, "notes": "Stephans Quintet is a grouping of five galaxies of which contains the first compact galaxy group discovered",
"numberexposures": 10, "objectid": "Stephans_Quintet", "observationtype": "longslit", "pa": 0.0, "ra": "22:35:58", "slitwidth": "Longslit1", "visits": 1}' --verbose
