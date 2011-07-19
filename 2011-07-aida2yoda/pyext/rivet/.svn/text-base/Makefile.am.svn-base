EXTRA_DIST = __init__.py rivetwrap.i

all-local: rivetwrap_wrap.cc rivetwrap.py
	@true

rivetwrap_wrap.cc rivetwrap.py: rivetwrap.i
	$(SWIG) -c++ -python -I$(top_srcdir)/include -o rivetwrap_wrap.cc $<

clean-local:
	@rm -f *.pyc
	@rm -f rivetwrap.py
	@rm -f rivetwrap_wrap.cc
