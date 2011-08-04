#!/bin/sh

set -e

# File based on rivet build scripts
MCGREPLICA="/afs/cern.ch/sw/lcg/external/MCGenerators"

# Fake the LCG_PLATFORM for i686 installation. And don't forget to source the
# GCC setup.sh below!
LCG_PLATFORM="x86_64-slc5-gcc43-opt"
# LCG_PLATFORM="i686-slc5-gcc43-opt"
echo "LCG_PLATFORM = $LCG_PLATFORM"

## Program versions
PROFVERSION=1.2.1
RIVETVERSION=1.5.0
ROOTVERSION=5.27.02

# This is copied from
# /afs/cern.ch/sw/lcg/external/pyanalysis/1.2_python2.5/logs/pyminuit_i686-slc5-gcc43-opt_make.log
# to match the ROOT version PyMinuit was compiled against.
ROOTLIB=/afs/cern.ch/sw/lcg/app/releases/ROOT/${ROOTVERSION}/${LCG_PLATFORM}/root/lib
test -d ${ROOTLIB} || { echo "ROOTLIB=$ROOTLIB not found" ; exit 1 ; }

LD_LIB_ADD="${ROOTLIB}"
PYTHONVERSION=2.6
LCG_PYTHON=/afs/cern.ch/sw/lcg/external/Python/2.6.5/${LCG_PLATFORM}
#PYTHONVERSION=2.5
#LCG_PYTHON=/afs/cern.ch/sw/lcg/external/Python/2.5.4/${LCG_PLATFORM}
test -d ${LCG_PYTHON} || { echo "LCG_PYTHON=$LCG_PYTHON not fount" ; exit 1 ; }
export PATH=${LCG_PYTHON}/bin:${PATH}
# Python2.6 needs its .../lib directory.
LD_LIB_ADD=${LCG_PYTHON}/lib:${LD_LIB_ADD}

PYANALYSISDIR=/afs/cern.ch/sw/lcg/external/pyanalysis/1.2_python${PYTHONVERSION}/${LCG_PLATFORM}/lib/python${PYTHONVERSION}/site-packages
test -d ${PYANALYSISDIR} || { echo "PYANALYSISDIR=$PYANALYSISDIR not found" ; exit 1 ; }
export PYTHONPATH=${PYANALYSISDIR}:${PYTHONPATH}

# Use the gcc version rivet was compiled with.
GCCSETUP=/afs/cern.ch/sw/lcg/contrib/gcc/4.3/$LCG_PLATFORM/setup.sh
test -f $GCCSETUP
source $GCCSETUP
echo "GCCSETUP = $GCCSETUP"

RIVETSETUP="$MCGREPLICA/rivet/$RIVETVERSION/$LCG_PLATFORM/rivetenv.sh"
test -f $RIVETSETUP

PREFIX=/tmp/${USER}/testtarget/professor/${PROFVERSION}/${LCG_PLATFORM}
# PREFIX=${MCGREPLICA}/professor/${PROFVERSION}/${LCG_PLATFORM}
TARGETDIR=${PREFIX}/lib/python${PYTHONVERSION}/site-packages

# For i686 installations work around that PyMinuit is linked against
# non-existant libMinui2.so.0 . We create a link to libMinuit2.so in
if [ ! -f ${ROOTLIB}/libMinuit2.so.0 ]; then
  mkdir -p ${PREFIX}/lib
  ln -s ${ROOTLIB}/libMinuit2.so ${PREFIX}/lib/libMinuit2.so.0
  LD_LIB_ADD=${PREFIX}/lib:${LD_LIB_ADD}
fi

export LD_LIBRARY_PATH=${LD_LIB_ADD}:${LD_LIBRARY_PATH}

# Test that pyminuit can be imported. This must be done after the
# LD_LIBRARY_PATH is exported in this script.
python -c "import minuit2" || python -c "import minuit"

echo "PYANALYSISDIR = $PYANALYSISDIR"
echo "TARGETDIR = $TARGETDIR"
echo "Using rivet from $RIVETSETUP"

# Add $TARGETDIR to PYTHONPATH to make setup.py happy.
export PYTHONPATH="$PYTHONPATH:$TARGETDIR"

mkdir -p $TARGETDIR

# Clean up from previous installations.
test -d build && rm -rf build
python setup-simple.py install --prefix $PREFIX | tee install_prof${PROFVERSION}_${LCG_PLATFORM}.log

# Write an environment setup file.
cat > $PREFIX/setup.sh <<EOF
# Setup environment for Professor usage.
# Just source this file in your current shell session via
# source ${PREFIX}/setup.sh

# Load an up-to-date compiler version
source ${GCCSETUP}

# Load a current Rivet installation for make-plots and rivet-config.
source ${RIVETSETUP}

# setup up-to-date Python version
PATH=${LCG_PYTHON}/bin:\${PATH}
# setup Professor binaries
PATH=${PREFIX}/bin:\${PATH}
export PATH
# setup 3rd party python modules
PYTHONPATH=${PYANALYSISDIR}:\${PYTHONPATH}
# setup Professor imports
PYTHONPATH=${TARGETDIR}:\${PYTHONPATH}
export PYTHONPATH

# Include ROOT for Minuit access even if ROOTSYS is set to get the Minuit version PyMinuit was compiled with.
export LD_LIBRARY_PATH=${LD_LIB_ADD}:\${LD_LIBRARY_PATH}

# Source the tab completion script if possible
if (complete &> /dev/null); then
    test -e "${PREFIX}/prof-completion" && source "${PREFIX}/prof-completion"
fi
EOF
