import unittest
import tempfile

import numpy
from professor.params import (ParameterPoint, ParameterRange, ParameterErrors,
                              ParameterMatrix)

## Examples of good and badly formatted parameter definitions.
GOODRANGE = """\
# This is a test parameter range file with intermixed tabs and spaces,
# comments, and unsorted parameter names.
PAR1    0.1     0.4
PAR3    0.3     0.6
PAR6    0.6     0.7  # A comment.
PAR2 -0.2	0.5
AAAA    0.9     0.8
"""

GOODPOINT = """\
# This is a test parameter point file with intermixed tabs and spaces,
# comments, and unsorted parameter names.
PAR1  = 0.1
PAR3==0.3
PAR6	0.6# A comment and a tab.
AAAA    0.9
"""

BADPOINT = """\
# This file contains a comma as decimal delimiter and parsing should fail.
PAR1 0,4
"""

class TestParams(unittest.TestCase):
    def setUp(self):
        """
        Create some temporary file storage objects to test parameter file
        IO.
        """
        self.rangefile = tempfile.NamedTemporaryFile()
        self.rangefile.write(GOODRANGE)

        self.pointfile = tempfile.NamedTemporaryFile()
        self.pointfile.write(GOODPOINT)

        self.badpointfile = tempfile.NamedTemporaryFile()
        self.badpointfile.write(BADPOINT)

        # Seek back to the start of the files, not sure if really necessary.
        self.rangefile.seek(0)
        self.pointfile.seek(0)
        self.badpointfile.seek(0)

    def tearDown(self):
        """Close the temporary files to delete them automatically."""
        self.rangefile.close()
        self.pointfile.close()
        self.badpointfile.close()

    def testRangeFileIO(self):
        rng = ParameterRange.mkFromFile(self.rangefile.name)
        self.assertEqual(rng.names,
                         ("AAAA", "PAR1", "PAR2", "PAR3", "PAR6"))
        self.assertEqual(rng.dim, 5)
        for idx, name in enumerate(["AAAA", "PAR1", "PAR2", "PAR3", "PAR6"]):
            self.assertEqual(rng.getIndex(name), idx)
        for idx, val in enumerate([0.9, 0.1, -0.2, 0.3, 0.6]):
            self.assertEqual(rng[idx, 0], val)
        for idx, val in enumerate([0.8, 0.4, 0.5, 0.6, 0.7]):
            self.assertEqual(rng[idx, 1], val)

        self.assertRaises(ValueError,
                          ParameterRange.mkFromFile, self.pointfile.name)

    def testPointFileIO(self):
        self.assertRaises(ValueError,
                          ParameterPoint.mkFromFile, self.rangefile.name)

        pp = ParameterPoint.mkFromFile(self.pointfile.name)
        self.assertEqual(pp.names,
                         ("AAAA", "PAR1", "PAR3", "PAR6"))
        for idx, name in enumerate(("AAAA", "PAR1", "PAR3", "PAR6")):
            self.assertEqual(pp.getIndex(name), idx)
        for idx, val in enumerate([0.9, 0.1, 0.3, 0.6]):
            self.assertEqual(pp[idx], val)

        self.assertRaises(ValueError,
                          ParameterPoint.mkFromFile, self.badpointfile.name)

    def testIndexingAndSlicingRange(self):
        rng = ParameterRange(["P1", "P2", "P3", "P4"],
                             [[1., 2.], [-1., 3.], [1., 2.], [3., 4.]])
        # get row by index
        self.assert_( (rng[1] == numpy.array([-1., 3.])).all() )
        # get row by parameter name
        self.assert_( (rng["P2"] == numpy.array([-1., 3.])).all() )
        # get one entry
        self.assertEqual(rng[1,1], 3.)

        subrng = rng[1:3]
        self.assertEqual(subrng.dim, 2)
        self.assertEqual(subrng.names, ("P2", "P3"))
        self.assert_( (subrng[0] == numpy.array([-1, 3.])).all() )

    def testIndexingAndSlicingPoint(self):
        pp = ParameterPoint(["P1", "P2", "P3", "P4"],
                            [0.0, 0.1, 0.2, 0.3])
        self.assert_( (pp == numpy.array([0.0, 0.1, 0.2, 0.3])).all() )
        self.assertEqual(pp["P1"], 0.0)
        self.assertEqual(pp[2], 0.2)

        subpp = pp[1:3]
        self.assertEqual(subpp.dim, 2)
        self.assertEqual(subpp.names, ("P2", "P3"))
        self.assert_( (subpp == numpy.array([0.1, 0.2])).all() )

    def testIndexingAndSlicingErrors(self):
        errors = ParameterErrors(["P1", "P2", "P3", "P4"],
                             [[1., 2.], [-1., 3.], [1., 2.], [3., 4.]])
        # get row by index
        self.assert_( (errors[1] == numpy.array([-1., 3.])).all() )
        # get row by parameter name
        self.assert_( (errors["P2"] == numpy.array([-1., 3.])).all() )
        # get one entry
        self.assertEqual(errors[1,1], 3.)
        # get one entry by strings
        self.assertEqual(errors["P2", "high"], 3.)

        suberrors = errors[1:3]
        self.assertEqual(suberrors.dim, 2)
        self.assertEqual(suberrors.names, ("P2", "P3"))
        self.assert_( (suberrors[0] == numpy.array([-1, 3.])).all() )

    def testMatrix(self):
        d = { ("PAR1","PAR1"): 11, ("PAR1","PAR2"): 12, ("PAR1","PAR3"): 13,
              ("PAR2","PAR1"): 21, ("PAR2","PAR2"): 22, ("PAR2","PAR3"): 23,
              ("PAR3","PAR1"): 31, ("PAR3","PAR2"): 32, ("PAR3","PAR3"): 33 }
        mat = ParameterMatrix.mkFromDict(d)
        for i in range(1,4):
            ni = "PAR%i" % (i)

            # test indexing rows
            rowvals = 10.0 * i + numpy.arange(1, 4)
            self.assert_( (mat[i-1] == rowvals).all() )
            # test indexing columns
            colvals = i + 10.0 * numpy.arange(1, 4)
            self.assert_( (mat[:,i-1] == colvals).all() )

            for j in range(1,4):
                nj = "PAR%i" % (j)
                # test indexing by names
                self.assertEqual(mat[ni, nj], 10.0 * i + j)
                # test indexing by int
                self.assertEqual(mat[i-1, j-1], 10.0 * i + j)
        self.assertRaises(ValueError,
                          ParameterMatrix.mkFromDict,
                          { ("P1", "P2"): 11 })

    def testStringParsing(self):
        strpoint = "Par1=1.0,Par3=3.0,Par2=2.5"
        p = ParameterPoint.mkFromString(strpoint)

        self.assertEqual(p.names, ("Par1", "Par2", "Par3"))

        self.assertEqual(p["Par1"], 1.0)
        self.assertEqual(p[0], 1.0)

        self.assertEqual(p["Par2"], 2.5)
        self.assertEqual(p[1], 2.5)

        self.assertEqual(p["Par3"], 3.0)
        self.assertEqual(p[2], 3.0)

        strrange = "Par1=1.0=3.0,Par3=3.0=4.0,Par2=2.5=1.5"
        r = ParameterRange.mkFromString(strrange)

        self.assertEqual(r.names, ("Par1", "Par2", "Par3"))

        self.assertEqual(r["Par1"][0], 1.0)
        self.assertEqual(r[0,0], 1.0)

        self.assertEqual(r["Par2"][0], 2.5)
        self.assertEqual(r[1,0], 2.5)

        self.assertEqual(r["Par3"][0], 3.0)
        self.assertEqual(r[2,0], 3.0)



if __name__ == "__main__":
    unittest.main()
