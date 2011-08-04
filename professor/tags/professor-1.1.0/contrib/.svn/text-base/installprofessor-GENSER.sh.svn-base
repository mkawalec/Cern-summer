#!/bin/sh

# File based on rivet build scripts
source /afs/.cern.ch/sw/lcg/external/MCGenerators/.scripts/genser.rc

# Fake the LCG_PLATFORM for i686 installation. And don't forget to source the
# GCC setup.sh below!
#LCG_PLATFORM="i686-slc5-gcc43-opt"
echo "LCG_PLATFORM = $LCG_PLATFORM"

PROFVERSION=1.0.0
# This is copied from
# /afs/cern.ch/sw/lcg/external/pyanalysis/1.2_python2.5/logs/pyminuit_i686-slc5-gcc43-opt_make.log
# to match the ROOT version PyMinuit was compiled against.
ROOTVERSION=5.27.02
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

# Set gcc environment
# source /afs/cern.ch/sw/lcg/contrib/gcc/4.3/${LCG_PLATFORM}/setup.sh

PYANALYSISDIR=/afs/cern.ch/sw/lcg/external/pyanalysis/1.2_python${PYTHONVERSION}/${LCG_PLATFORM}/lib/python${PYTHONVERSION}/site-packages
test -d ${PYANALYSISDIR} || { echo "PYANALYSISDIR=$PYANALYSISDIR not found" ; exit 1 ; }
export PYTHONPATH=${PYANALYSISDIR}:${PYTHONPATH}

# Uncomment the following line for i686 installations on a x86_64 machine.
# source /afs/cern.ch/sw/lcg/contrib/gcc/4.3/$LCG_PLATFORM/setup.sh

GCCSETUP=`which gcc`
GCCSETUP=`dirname ${GCCSETUP}`
GCCSETUP=`readlink -f ${GCCSETUP}/..`
GCCSETUP="${GCCSETUP}/setup.sh"
test -f ${GCCSETUP}
echo "GCCSETUP = ${GCCSETUP}"

RIVETSETUP="${MCGREPLICA}/rivet/1.3.0/${LCG_PLATFORM}/rivetenv.sh"
test -f ${RIVETSETUP}

# PREFIX=${HOME}/public/testtarget/professor/${PROFVERSION}/${LCG_PLATFORM}
PREFIX=${MCGREPLICA}/professor/${PROFVERSION}/${LCG_PLATFORM}
TARGETDIR=${PREFIX}/lib/python${PYTHONVERSION}/site-packages

# For i686 installations work around that PyMinuit is linked against
# non-existant libMinui2.so.0 . We create a link to libMinuit2.so in 
#mkdir -p ${PREFIX}/lib
#ln -s ${ROOTLIB}/libMinuit2.so ${PREFIX}/lib/libMinuit2.so.0
#LD_LIB_ADD=${PREFIX}/lib:${LD_LIB_ADD}

export LD_LIBRARY_PATH=${LD_LIB_ADD}:${LD_LIBRARY_PATH}

echo "PYANALYSISDIR = ${PYANALYSISDIR}"
echo "TARGETDIR = ${TARGETDIR}"
echo "Using rivet from ${RIVETSETUP}"

# Add $TARGETDIR to PYTHONPATH to make setup.py happy.
export PYTHONPATH=${PYTHONPATH}:${TARGETDIR}

mkdir -p ${TARGETDIR}

# Clean up from previous installations.
test -d build && rm -rf build
python setup-simple.py install --prefix ${PREFIX} | tee install_prof${PROFVERSION}_${LCG_PLATFORM}.log

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
EOF
