#include "YODA/Scatter2D.h"
#include "YODA/Histo1D.h"
#include "YODA/Profile1D.h"

namespace YODA {


  /// Make a Scatter2D representation of a Histo1D
  Scatter2D mkScatter(const Histo1D& h) {
    Scatter2D rtn;
    rtn.setAnnotations(h.annotations());
    rtn.setAnnotation("Type", h.type());
    foreach (const HistoBin1D& b, h.bins()) {
      const double x = b.focus();
      const double ex_m = b.focus() - b.lowEdge();
      const double ex_p = b.highEdge() - b.focus();
      const double y = b.height();
      const double ey = b.heightError();
      const Point2D pt(x, ex_m, ex_p, y, ey, ey);
      rtn.addPoint(pt);
    }
    assert(h.numBins() == rtn.numPoints());
    return rtn;
  }


  /// Make a Scatter2D representation of a Profile1D
  Scatter2D mkScatter(const Profile1D& p) {
    Scatter2D rtn;
    rtn.setAnnotations(p.annotations());
    rtn.setAnnotation("Type", p.type());
    foreach (const ProfileBin1D& b, p.bins()) {
      const double x = b.focus();
      const double ex_m = b.focus() - b.lowEdge();
      const double ex_p = b.highEdge() - b.focus();
      const double y = b.mean();
      const double ey = b.stdErr();
      const Point2D pt(x, ex_m, ex_p, y, ey, ey);
      rtn.addPoint(pt);
    }
    assert(p.numBins() == rtn.numPoints());
    return rtn;
  }


  ////////////////////////////////////////


  /// @todo Lots of boilerplate shared between these three functions, but I can't think of a
  ///   C++ way to do it better, since functors for value and error combination are *so* heavy.


  /// Subtract two scatters
  inline Scatter2D operator + (const Scatter2D& first, const Scatter2D& second) {
    Scatter2D tmp;
    for (size_t i = 0; i < first.numPoints(); ++i) {
      const Point2D& p1 = first.point(i);
      const Point2D& p2 = second.point(i);
      assert(fuzzyEquals(p1.xMin(), p2.xMin()));
      assert(fuzzyEquals(p1.xMax(), p2.xMax()));
      const double x = (p1.x() + p2.x())/2.0;
      //
      const double y = p1.y() + p2.y();
      /// @todo Deal with +/- errors separately?
      const double ey = sqrt( sqr(p1.yErrAvg()) + sqr(p2.yErrAvg()) );
      tmp.addPoint(x, p1.xErrMinus(), p1.xErrPlus(), y, ey, ey);
    }
    assert(tmp.numPoints() == first.numPoints());
    return tmp;
  }


  /// Subtract two scatters
  inline Scatter2D operator - (const Scatter2D& first, const Scatter2D& second) {
    Scatter2D tmp;
    for (size_t i = 0; i < first.numPoints(); ++i) {
      const Point2D& p1 = first.point(i);
      const Point2D& p2 = second.point(i);
      assert(fuzzyEquals(p1.xMin(), p2.xMin()));
      assert(fuzzyEquals(p1.xMax(), p2.xMax()));
      const double x = (p1.x() + p2.x())/2.0;
      //
      const double y = p1.y() - p2.y();
      /// @todo Deal with +/- errors separately?
      const double ey = sqrt( sqr(p1.yErrAvg()) + sqr(p2.yErrAvg()) );
      tmp.addPoint(x, p1.xErrMinus(), p1.xErrPlus(), y, ey, ey);
    }
    assert(tmp.numPoints() == first.numPoints());
    return tmp;
  }


  /// Divide two scatters
  Scatter2D operator / (const Scatter2D& numer, const Scatter2D& denom) {
    Scatter2D tmp;
    for (size_t i = 0; i < numer.numPoints(); ++i) {
      const Point2D& p1 = numer.point(i);
      const Point2D& p2 = denom.point(i);
      assert(fuzzyEquals(p1.xMin(), p2.xMin()));
      assert(fuzzyEquals(p1.xMax(), p2.xMax()));
      const double x = (p1.x() + p2.x())/2.0;
      //
      const double y = p1.y() / p2.y();
      /// @todo Deal with +/- errors separately
      const double ey = y * sqrt( sqr(p1.yErrAvg()/p1.y()) + sqr(p2.yErrAvg()/p2.y()) );
      tmp.addPoint(x, p1.xErrMinus(), p1.xErrPlus(), y, ey, ey);
    }
    assert(tmp.numPoints() == numer.numPoints());
    return tmp;
  }


}
