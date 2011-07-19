ACLOCAL_AMFLAGS = -I m4
SUBDIRS = src pyext data include bin doc test

#dist_pkgdata_DATA = rivetenv.sh rivetenv.csh
EXTRA_DIST = GUIDELINES

doc:
	cd doc && $(MAKE) doc

.PHONY : doc dox pyclean

clean-local:
	@rm -rf a.out


## Doxygen
if WITH_DOXYGEN
dox:
	@echo "Running Doxygen..."
	@$(DOXYGEN) $(top_srcdir)/Doxyfile || true
#all-local: dox
#	@true
install-dox:
	$(install_sh_DATA) doxy/html/* $(DESTDIR)$(pkgdatadir)/doc/html
mostlyclean-local:
	@rm -rf $(top_builddir)/doxy
uninstall-local:
	@rm -rf $(DESTDIR)$(pkgdatadir)/doc; \
	test ! -d $(DESTDIR)$(pkgdatadir) || rmdir --ignore-fail-on-non-empty $(DESTDIR)$(pkgdatadir)
endif


pyclean:
	cd pyext && $(MAKE) clean


## Remove SVN dirs
dist-hook:
	@rm -rf `find $(distdir) -name ".svn"`


## Upload to HepForge
RSH=rsync
DEST=login.hepforge.org:rivet/downloads/
upload: dist
	$(RSH) $(DIST_ARCHIVES) $(DEST)
