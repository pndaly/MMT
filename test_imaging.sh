#!/bin/bash

python3 mmt.py --action=POST --catalog_id=486 --token=0f3732fcfb1c8577c390e71a176f3c8f --program_id=977 --payload='{"dec": "+33:57:36", "epoch": 2000.0, "exposuretime": 300.0, "filter": "r", "magnitude": 15.0, "notes": "Stephans Quintet is a visual grouping of five galaxies of which four form the first compact galaxy group ever discovered", "numberexposures": 5, "observationtype": "imaging", "objectid": "Stephans Quintet", "onevisitpernight": "true", "pa": 0.0, "pm_dec": 0.0, "pm_ra": 0.0, "priority": 1, "ra": "22:35:58", "visits": 1}' --verbose
