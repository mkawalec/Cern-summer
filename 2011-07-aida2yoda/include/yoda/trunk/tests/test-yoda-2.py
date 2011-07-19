#! /usr/bin/env python

import yoda

h1 = yoda.Histo1D(10, 0.0, 20.0)
h1.addAnnotation("Foo", "Bar")
yoda.WriterAIDA.create().write("test.py.aida", h1)

#s2 = yoda.Scatter2D(h1)
