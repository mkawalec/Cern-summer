#!/bin/bash

set -e

usage () {
    echo "usage:  $0  MCDIR  REF.aida [REF2.aida ...]"
    echo "Call gap_removal for all out.aida files under MCDIR and every reference AIDA file."
}

if [[ $# -lt 2 ]]; then
    usage
    exit 1
fi

MCDIR="$1"
shift


for AIDA in "$MCDIR"/*/out.aida ; do
    echo $AIDA
    cp "$AIDA" "${AIDA}.orig"
    for REF in $@; do
        echo "  $REF"
        rivet-rmgaps "$REF" "${AIDA}" "$AIDA"
    done
done
