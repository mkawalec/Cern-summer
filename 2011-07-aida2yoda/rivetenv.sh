# These variables need to exist
prefix=/usr/local
exec_prefix=${prefix}
datarootdir=${prefix}/share

export PATH="$exec_prefix/bin:$PATH"
export LD_LIBRARY_PATH="${exec_prefix}/lib:/usr/local/lib:/usr/local/lib:$LD_LIBRARY_PATH"
export PYTHONPATH="/usr/local/lib/python2.7/site-packages:$PYTHONPATH"
export TEXMFHOME="${datarootdir}/Rivet/texmf:$TEXMFHOME"
export HOMETEXMF="${datarootdir}/Rivet/texmf:$HOMETEXMF"
export TEXMFCNF="${datarootdir}/Rivet/texmf/cnf:$TEXMFCNF"

if (complete &> /dev/null); then
    test -e "${datarootdir}/Rivet/rivet-completion" && source "${datarootdir}/Rivet/rivet-completion"
fi
