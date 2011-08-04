# These variables need to exist
set prefix=/usr/local
set exec_prefix=${prefix}
set datarootdir=${prefix}/share

setenv PATH "$exec_prefix/bin:$PATH"
setenv LD_LIBRARY_PATH "${exec_prefix}/lib:/usr/local/lib:/usr/local/lib:$LD_LIBRARY_PATH"

if ($?PYTHONPATH) then
setenv PYTHONPATH "/usr/local/lib/python2.7/site-packages:$PYTHONPATH"
else
setenv PYTHONPATH "/usr/local/lib/python2.7/site-packages"
endif

if ($?TEXMFHOME) then
setenv TEXMFHOME "${datarootdir}/Rivet/texmf:$TEXMFHOME"
else
setenv TEXMFHOME "${datarootdir}/Rivet/texmf"
endif

if ($?HOMETEXMF) then
setenv HOMETEXMF "${datarootdir}/Rivet/texmf:$HOMETEXMF"
else
setenv HOMETEXMF "${datarootdir}/Rivet/texmf"
endif
