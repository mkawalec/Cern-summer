#!/bin/bash
#
# usage:
# $0 configfile1 configfile2

CMD="/home/eike/projects/professor/trunk/professor/test/chi2_vs_dp/genchi2data.py"

function runcmd () {
    #echo "Starting $CMD ${CONF}.${1}"
    #nice $CMD ${CONF}.${1} &> ${LOG}.${1}

    LOG="${1/conf/log}"
    echo "Starting $CMD $1 &> $LOG"
    nice "$CMD" "$1" &> "$LOG" &
}

while [ -n "$1" ]; do
    runcmd "$1"
    shift
done
