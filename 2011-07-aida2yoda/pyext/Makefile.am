EXTRA_DIST = ez_setup.py lighthisto.py spiresbib.py

if ENABLE_PYEXT

SUBDIRS = rivet .

all-local: rivet/rivetwrap_wrap.cc
	$(PYTHON) setup.py build

install-exec-local:
	$(PYTHON) setup.py install --prefix=$(DESTDIR)$(prefix)

## TODO: Really want DESTDIR here?
uninstall-local:
	rm -rf $(DESTDIR)$(RIVET_PYTHONPATH)/rivet
	rm -rf $(DESTDIR)$(RIVET_PYTHONPATH)/lighthisto.py*
	rm -rf $(DESTDIR)$(RIVET_PYTHONPATH)/spiresbib.py*
	rm -rf $(DESTDIR)$(RIVET_PYTHONPATH)/Rivet-*.egg-info

clean-local:
	$(PYTHON) setup.py clean --all
	@rm -f $(top_builddir)/*.pyc
	@rm -rf $(builddir)/build
	@rm -rf dist

distclean-local:
	@rm -rf rivet.egg-info

endif
