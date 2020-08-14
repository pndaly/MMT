#!/bin/sh


# +
# edit as required
# -
export MMT_HOME=${1:-${PWD}}
export MMT_BIN=${MMT_HOME}/bin
export MMT_ETC=${MMT_HOME}/etc
export MMT_LOG=${MMT_HOME}/log
export MMT_IMG=${MMT_HOME}/img
export MMT_SRC=${MMT_HOME}/src

# +
# PYTHONPATH
# -
_pythonpath=$(env | grep PYTHONPATH | cut -d'=' -f2)
if [[ -z "${_pythonpath}" ]]; then
  export PYTHONPATH=`pwd`
fi
export PYTHONPATH=${MMT_HOME}:${MMT_SRC}:${PYTHONPATH}


# +
# update ephemeris (any value will do but I use "load")
# -
if [[ ! -z ${2} ]]; then
  python3 -c 'from src import *; get_iers()'
fi
