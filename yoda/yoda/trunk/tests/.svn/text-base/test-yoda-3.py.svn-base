#!/usr/bin/env python

import yoda

h2 = yoda.Histo2D(100, 0, 100, 100, 0, 100);
h2.addAnnotation("Foo", "Bar");
yoda.WriterAIDA.create().write("test.py.aida", h2)

