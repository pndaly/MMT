# MMT Target of Opportunity

 - \<base\>: https://scheduler.mmto.arizona.edu/APIv2/catalogTarget/

 - \<token\>: ?token=YOUR_SECRET_TOKEN

## Delete Target
HTTP verb: DELETE, Route: \<base\>/\<target_id\>\<token\>

 % python3 mmt.py --action=DELETE --target_id=6221 --verbose

## Get Target
HTTP verb: GET, Route: \<base\>/\<target_id\>\<token\>

 % python3 mmt.py --action=DELETE --target_id=6221 --verbose

## Create New Target
HTTP verb: POST, Route: \<base\>/\<token\>

TBD

## Update Target
HTTP verb: PUT, Route: \<base\>/\<target_id\>\<token\>

 % python3 mmt.py --action=PUT --payload='{"filter": "r", "visits": 3}' --target_id=6221 --verbose

## Upload Finding Chart
HTTP verb: POST, Route: \<base\>/\<target_id\>\<token\>

 % python3 MMT.py --action=UPLOA' --target_id=6238 --file=M31.png --program_id=997 --catalog_id=486 --verbose

--------------------------------------

Last Modified: 20200714
Last Author: Phil Daly (pndaly@arizona.edu)
