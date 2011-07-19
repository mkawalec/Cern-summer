#include "YODA/Scatter2D.h"
#include "YODA/Histo1D.h"
#include "YODA/Profile1D.h"

namespace YODA {


  /// Make a Scatter2D representation of a Histo1D
  Scatter2D mkScatter(const Histo1D& h) {
    Scatter2D rtn;
    rtn.setAnnotations(h.annotations());
    rtn.setAnnotation("Type", h._aotype());
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
    rtn.setAnnotation("Type", p._aotype());
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


}
