EXTRA_DIST = __init__.py yodawrap.i

all-local: yodawrap_wrap.cc yodawrap.py
	@true

yodawrap_wrap.cc yodawrap.py: yodawrap.i
	$(SWIG) -c++ -python -I$(top_srcdir)/include -o yodawrap_wrap.cc $<

clean-local:
	@rm -f *.pyc
	@rm -f yodawrap.py
	@rm -f yodawrap_wrap.cc
