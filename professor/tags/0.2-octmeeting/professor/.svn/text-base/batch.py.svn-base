#!/usr/bin/python
# vim:fileencoding=utf-8
"""batch.py

"""

from professor.competition import CompetitionFileWriter


cfw = CompetitionFileWriter('/home/eike/uni/professor/trunk/testdata/2d/testref1a/',
                            '/home/eike/uni/professor/trunk/testdata/2d/out',
                            '/tmp/comp.txt')

cfw.openFile()
cfw.runAllGuesses(maxiter=10)
cfw.closeFile()
