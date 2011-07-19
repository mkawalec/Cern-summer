## TODO: make variable names POSIX-compliant in rivet-manual.pdf target!

dist_noinst_SCRIPTS = mk-analysis-html mk-analysis-latex

DOCSOURCES = compare-histos.txt  heppennames.sty warning.png thinker.png cone.png \
  h-physrev3.bst hepnames.sty JHEP3.cls bend.png hepnicenames.sty JHEP.bst \
  make-plots.txt rivet-manual.tex preamble.tex hepparticles.sty maybemath.sty \
  rivet-manual.pdf hepunits.sty underscore.sty microtype.sty

## TODO: replace readplot with lighthisto/YODA functionality
EXTRA_DIST = $(DOCSOURCES) readplot.py

if WITH_ASCIIDOC
EXTRA_DIST += compare-histos.html make-plots.html
endif

DOCS =

if ENABLE_PYEXT

DOCS += analyses.html
analyses.html: $(top_srcdir)/src/Analyses mk-analysis-html
	LD_LIBRARY_PATH=$(top_srcdir)/src/.libs:$(top_srcdir)/src/Tools/yaml-cpp/.libs:$(FASTJETLIBPATH):$(HEPMCLIBPATH):$(LD_LIBRARY_PATH):$(prefix)/lib \
DYLD_LIBRARY_PATH=$(top_srcdir)/src/.libs:$(top_srcdir)/src/Tools/yaml-cpp/.libs:$(FASTJETLIBPATH):$(HEPMCLIBPATH):$(DYLD_LIBRARY_PATH):$(prefix)/lib \
RIVET_INFO_PATH=$(top_srcdir)/data/anainfo \
PYTHONPATH=$(top_srcdir)/pyext:$(PYTHONPATH) \
$(PYTHON) mk-analysis-html analyses.html

endif


if ENABLE_PDFMANUAL
if WITH_PDFLATEX

DOCS += rivet-manual.pdf
EXTRA_DIST += analyses.tex analyses.bib refs.bib


if ENABLE_PYEXT

analyses.bib analyses.tex: $(top_srcdir)/src/Analyses $(top_srcdir)/data/plotinfo $(top_srcdir)/data/anainfo mk-analysis-latex
	LD_LIBRARY_PATH=$(top_srcdir)/src/.libs:$(FASTJETLIBPATH):$(HEPMCLIBPATH):$(LD_LIBRARY_PATH) \
DYLD_LIBRARY_PATH=$(top_srcdir)/src/.libs:$(FASTJETLIBPATH):$(HEPMCLIBPATH):$(DYLD_LIBRARY_PATH) \
RIVET_INFO_PATH=$(top_srcdir)/data/anainfo \
$(PYTHON) mk-analysis-latex

else

analyses.bib analyses.tex:
	> analyses.tex
	> analyses.bib

endif


#LATEX	= pdflatex
LATEX	= pdflatex --interaction=nonstopmode
BIBTEX	= bibtex
MAKEINDEX = makeindex
RERUN = "(There were undefined references|Rerun to get (cross-references|the bars) right)"
RERUNBIB = "No file.*\.bbl|Citation.*undefined"
MAKEIDX = "^[^%]*\\makeindex"
RM = rm -f

DOCNAME = rivet-manual
$(DOCNAME).pdf : $(DOCNAME).tex preamble.tex analyses.tex refs.bib analyses.bib
	$(LATEX) $<; true
	egrep $(MAKEIDX) $< && ($(MAKEINDEX) $(DOCNAME) && cp $(DOCNAME).toc $(DOCNAME).toc.bak && $(LATEX) $<) > /dev/null; true
	egrep -c $(RERUNBIB) $(DOCNAME).log && ($(BIBTEX) $(DOCNAME) && cp $(DOCNAME).toc $(DOCNAME).toc.bak && $(LATEX) $<); true
	for i in `seq 5`; do if egrep $(RERUN) $(DOCNAME).log; then echo "LaTeX re-run $i"; cp $(DOCNAME).toc $(DOCNAME).toc.bak; $(LATEX) $<; else break; fi; done; true
	if cmp -s $(DOCNAME).toc $(DOCNAME).toc.bak; then true; else $(LATEX) $<; true; fi
	$(RM) $(DOCNAME).toc.bak; true

endif
endif


if WITH_ASCIIDOC

DOCS += compare-histos.html make-plots.html

compare-histos.html: compare-histos.txt
	asciidoc -a toc compare-histos.txt

make-plots.html: make-plots.txt
	asciidoc -a toc make-plots.txt

endif


################


.PHONY = all doc upload arxivtar

#all:
#	@echo "Default make rule does nothing: use 'make doc'"

doc: $(DOCS)
	@true

## TODO: Put Rivet version string in PDF filename for upload?
RSH=rsync
DEST=login.hepforge.org:rivet/public_html/
upload: $(DOCS)
	$(RSH) $? $(DEST)

arxivtar: $(DOCSOURCES) rivet-manual.bbl
	for i in *.png; do convert $$i $${i/.png/.eps}; done
	tar czf rivet-manual.tar.gz \
rivet-manual.tex preamble.tex analyses.tex rivetversion.sty rivet-manual.bbl \
hepnames.sty hepnicenames.sty hepparticles.sty heppennames.sty hepunits.sty maybemath.sty microtype.sty underscore.sty \
bend.eps cone.eps thinker.eps warning.eps \
h-physrev3.bst JHEP3.cls JHEP.bst

mostlyclean-local:
	rm -rf *.aux *.log *.toc

clean-local:
	rm -rf $(DOCS)


## Install!
pkgdata_DATA = $(DOCS)
