#! /usr/bin/env bash

if [[ -z "$PYTHON_BUILD_DIR" ]]; then
    echo "\$PYTHON_BUILD_DIR must be defined" 1>&2
    exit 1
fi
export PYTHONPATH=$(ls -d $PYTHON_BUILD_DIR/lib.*):$PYTHONPATH

#echo PYTHONPATH=$PYTHONPATH \
#    PYTHON_BUILD_DIR=$PYTHON_BUILD_DIR \
#    LD_LIBRARY_PATH=$LD_LIBRARY_PATH \
#    PATH=$PATH \
#    RIVET_REF_PATH=$RIVET_REF_PATH \
#    RIVET_INFO_PATH=$RIVET_INFO_PATH \
#    RIVET_ANALYSIS_PATH=$RIVET_ANALYSIS_PATH


function _clean() {
    rm -f fifo.hepmc
    rm -f file2.hepmc
}

function _setup() {
    _clean
    cp testApi.hepmc file2.hepmc
    mkfifo fifo.hepmc
}

function _check() {
    CODE=$?
    if [[ $CODE -ne 0 ]]; then
        _clean
        _exit $CODE
    fi
}


_setup

rivet --list-analyses > log || exit $?

rivet -a D0_2008_S7554427 testApi.hepmc file2.hepmc > log || exit $?
grep -q "20 events" log
_check

cat testApi.hepmc | rivet -a D0_2008_S7554427 > log || exit $?
grep -q "10 events" log
_check

cat testApi.hepmc > fifo.hepmc &
rivet -a D0_2008_S7554427 fifo.hepmc > log || exit $?
grep -q "10 events" log
_check
_clean
