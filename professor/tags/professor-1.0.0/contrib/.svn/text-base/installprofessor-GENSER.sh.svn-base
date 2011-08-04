# File based on rivet build scripts
. /afs/.cern.ch/sw/lcg/external/MCGenerators/.scripts/genser.rc

PROFVERSION=1.0.0a0
# This is copied from
# /afs/cern.ch/sw/lcg/external/pyanalysis/1.2_python2.5/logs/pyminuit_i686-slc5-gcc43-opt_make.log
ROOTVERSION=5.27.02

echo "LCG_PLATFORM = $LCG_PLATFORM"

# Set gcc environment
# source /afs/cern.ch/sw/lcg/contrib/gcc/4.3/${LCG_PLATFORM}/setup.sh

PYANALYSISDIR=/afs/cern.ch/sw/lcg/external/pyanalysis/1.2_python2.5/${LCG_PLATFORM}/lib/python2.5/site-packages


export PATH=/afs/cern.ch/sw/lcg/external/Python/2.5.4/${LCG_PLATFORM}/bin:$PATH
export PYTHONPATH=/$PYANALYSISDIR:$PYTHONPATH
export LD_LIBRARY_PATH=/afs/cern.ch/sw/lcg/app/releases/ROOT/${ROOTVERSION}/${LCG_PLATFORM}/root/lib/:$LD_LIBRARY_PATH

# python

GCCBASE=`which gcc`
GCCBASE=`dirname $GCCBASE`
GCCBASE=`readlink -f $GCCBASE/..`
echo "GCCBASE = $GCCBASE"

# PREFIX=${HOME}/testtarget/professor/${PROFVERSION}/${LCG_PLATFORM}
PREFIX=${MCGREPLICA}/professor/${PROFVERSION}/${LCG_PLATFORM}
TARGETDIR=${PREFIX}/lib/python2.5/site-packages

# add $TARGETDIR to PYTHONPATH to make setup.py happy
export PYTHONPATH=${PYTHONPATH}:${TARGETDIR}

mkdir -p ${TARGETDIR}

./setup-simple.py install --prefix ${PREFIX} | tee install_$LCG_PLATFORM.log

# Write an environment setup file.
cat > $PREFIX/setup.sh <<EOF
# Setup environment for Professor usage.
# Just source this file in your current shell session via
# source $PREFIX/setup.sh

# Load an up-to-date compiler version
source $GCCBASE/setup.sh

# setup up-to-date Python version
PATH=/afs/cern.ch/sw/lcg/external/Python/2.5.4/${LCG_PLATFORM}/bin:\$PATH
# setup Professor binaries
PATH=$PREFIX/bin:\$PATH
export PATH
# setup 3rd party python modules
PYTHONPATH=$PYANALYSISDIR:\$PYTHONPATH
# setup Professor imports
PYTHONPATH=$TARGETDIR:\$PYTHONPATH
export PYTHONPATH

# include ROOT for Minuit access only if ROOTSYS is not set.
if [[ -z \$ROOTSYS ]]; then
	export LD_LIBRARY_PATH=/afs/cern.ch/sw/lcg/app/releases/ROOT/${ROOTVERSION}/${LCG_PLATFORM}/root/lib/:\$LD_LIBRARY_PATH
fi
EOF
