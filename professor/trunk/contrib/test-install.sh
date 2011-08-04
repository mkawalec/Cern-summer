#!/bin/sh

set -e

# check that we have all executables
RM=`which rm`
STAT=`which stat`
TAR=`which tar`
WGET=`which wget`

# check professor scripts are available
PROFRUNCOMBS=`which prof-runcombs`
PROFINTERPOLATE=`which prof-interpolate`
PROFTUNE=`which prof-tune`

LEPEXC_URL="http://users.hepforge.org/~holsch/examples/LEP/lep-exercise.tar.gz"
LEPEXC_SIZE="2499399"

# prepare excercise dir
EXC_FILE=`basename $LEPEXC_URL`
EXC_DIR="${EXC_FILE%%.*}"
if [ -f "$EXC_FILE" ]; then
    echo "Found $EXC_FILE"
    if [ $LEPEXC_SIZE != `stat --format "%s" "$EXC_FILE"` ]; then
        echo "Wrong file size. Removing!"
        $RM -f "$EXC_FILE"
    fi
fi

if [ ! -f "$EXC_FILE" ]; then
    $WGET "$LEPEXC_URL"
fi

if [ $LEPEXC_SIZE != `stat --format "%s" "$EXC_FILE"` ]; then
    echo "Failed to download file from $LEPEXC_URL"
    echo "Wrong file size. Removing!"
    $RM -f "$EXC_FILE"
    exit 1
fi

if [ -d "$EXC_DIR" ]; then
    echo "Found directory $EXC_DIR. Removing!"
    $RM -rf "$EXC_DIR"
fi

$TAR xzf "$EXC_FILE"


# test basic professor working
RUNSFILE="$EXC_DIR/runcombs.dat" 

"$PROFRUNCOMBS" -c "0:1" --datadir "$EXC_DIR" --outfile "$RUNSFILE" || { echo "Failed to run prof-runcombs" ; exit 1 ; }
echo "prof-runcombs suceeded"

"$PROFINTERPOLATE" --datadir "$EXC_DIR" --runs "$RUNSFILE" --outdir "$EXC_DIR" --ipol-method quadratic || { echo "Failed to run prof-interpolate" ; exit 1 ; } 
echo "prof-interpolate suceeded"

# "$PROFTUNE" --datadir "$EXC_DIR" --runs "$RUNSFILE" --outdir "$EXC_DIR" --no-ipolhistos --no-params || { echo "Failed to run prof-tune" ; exit 1 ; } 
"$PROFTUNE" --datadir "$EXC_DIR" --runs "$RUNSFILE" --outdir "$EXC_DIR" --ipol-method quadratic || { echo "Failed to run prof-tune" ; exit 1 ; } 
echo "prof-tune suceeded"

echo "Successfully finished all tests. Removing directory $EXC_DIR"
rm -rf "$EXC_DIR"
