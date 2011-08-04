#!/bin/bash

SEDSCRIPT="s/sS'runs'$/sS'_runs'/;s/sS'obs'$/sS'_obs'/;s/sS'HITLIMIT_FLAG'$/sS'f_hitlimit'/;s/sS'OUTSIDE_FLAG'$/sS'f_extrapolation'/;s/sS'LIMITSUSED_FLAG'$/sS'f_limits'/;s/tbsS'FIXED_PARAMS'$/tbsS'fixedparams'/"

while test $# -gt 0; do
    TMP=`mktemp`
    sed -e $SEDSCRIPT $1 > $TMP
    mv $1 ${1}.bak
    mv $TMP $1
    echo $1
    shift
done
