# MMT Target of Opportunity

```bash
 % source <mmt-code-path>/etc/MMT.sh <mmt-code-path> load
```

 - \<base\>: https://scheduler.mmto.arizona.edu/APIv2/catalogTarget/

 - \<token\>: ?token=YOUR_SECRET_TOKEN

NB: You must copy `mmt_token.template.py` to `mmt_token.py` and edit the latter
file for your access credentials!

## Example scripts

Check out the `<mmt-code-path>/etc` sub-directory for examples of how to
use the code for delete, get, post, put and upload operations. For new
targets of opportunity, you would execute a POST command to set the initial
target and then an UPLOAD command to attach a finder chart.

--------------------------------------

Last Modified: 20200818

Last Author: Phil Daly (pndaly@arizona.edu)
