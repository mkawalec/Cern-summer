import unittest
import numpy
from professor.tools.pointsampling import ScanPointGenerator
from professor.params import ParameterRange, ParameterPoint

class TestSampling(unittest.TestCase):
    def setUp(self):
        self.ranges = ParameterRange(["Par1", "Par2", "Par3"],
                                     [[0.0, 1.0], [0.0, 1.0], [0.0, 1.0]])

    def testDiagonal(self):
        diag = ScanPointGenerator.mkDiagonal(self.ranges)
        for i, p in enumerate(diag.generate(11)):
            for n in p.names:
                self.assertEqual(p[n], 0.1*i)

    def testSubRangeDiagonal(self):
        center = ParameterPoint(self.ranges.names,
                                0.25 * numpy.ones(self.ranges.dim))
        diag = ScanPointGenerator.mkSubRangeDiagonal(self.ranges, center)
        for i, p in enumerate(diag.generate(11)):
            for n in p.names:
                self.assertEqual(p[n], 0.05*i)


if __name__ == "__main__":
    unittest.main()
