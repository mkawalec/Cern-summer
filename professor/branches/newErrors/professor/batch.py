"""batch.py

"""

from professor.competition import CompetitionFileWriter


cfw = CompetitionFileWriter('/home/eike/uni/professor/trunk/testdata/2d/testref1a/',
                            '/home/eike/uni/professor/trunk/testdata/2d/out',
                            '/tmp/comp.txt')

cfw.openFile()
try:
    cfw.runAllGuesses(maxiter=10)
finally:
    cfw.closeFile()
