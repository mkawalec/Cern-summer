## bash completion
if ENABLE_PYEXT

dist_pkgdata_DATA = rivet-completion
bashcomp_dir = $(prefix)/etc/bash_completion.d
install-data-local:
	if [[ -d "$(bashcomp_dir)" && -w "$(bashcomp_dir)" ]]; then \
      install --mode 644 rivet-completion $(bashcomp_dir)/; fi
uninstall-local:
	rm -f $(bashcomp_dir)/rivet-completion

else

EXTRA_DIST = rivet-completion

endif


SUBDIRS = refdata anainfo plotinfo texmf
