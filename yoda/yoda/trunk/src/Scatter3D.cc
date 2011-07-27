#include "YODA/Scatter3D.h"
#include "YODA/Histo2D.h"

namespace YODA {


  /// Make a Scatter3D representation of a Histo2D
  Scatter3D mkScatter(const Histo2D& h) {
    Scatter3D rtn;
    rtn.setAnnotations(h.annotations());
    rtn.setAnnotation("Type", h.type());
    foreach (const HistoBin2D& b, h.bins()) {
      const double x = b.focus().first;
      const double ex_m = b.focus().first - b.lowEdgeX();
      const double ex_p = b.highEdgeX() - b.focus().first;

      const double y = b.focus().second;
      const double ey_m = b.focus().second - b.lowEdgeY();
      const double ey_p = b.highEdgeY() - b.focus().second;

      const double z = b.height();
      const double ez = b.heightErr();
      const Point3D pt(x, ex_m, ex_p, y, ey_m, ey_p, z, ez, ez);
      rtn.addPoint(pt);
    }
    //assert(h.numBins() == rtn.numPoints());
    return rtn;
  }

  ////////////////////////////////////////


  /// Subtract two scatters
  inline Scatter3D operator + (const Scatter3D& first, const Scatter3D& second) {
    /// @todo Implement
    Scatter3D tmp;
    return tmp;
  }


  /// Subtract two scatters
  inline Scatter3D operator - (const Scatter3D& first, const Scatter3D& second) {
    /// @todo Implement
    Scatter3D tmp;
    return tmp;
  }


  /// Divide two scatters
  Scatter3D operator / (const Scatter3D& numer, const Scatter3D& denom) {
    Scatter3D tmp;
    for (size_t i = 0; i < numer.numPoints(); ++i) {
      const Point3D& p1 = numer.point(i);
      const Point3D& p2 = denom.point(i);
      
      assert(fuzzyEquals(p1.xMin(), p2.xMin()));
      assert(fuzzyEquals(p1.xMax(), p2.xMax()));

      assert(fuzzyEquals(p1.yMin(), p2.yMin()));
      assert(fuzzyEquals(p1.yMax(), p2.yMax()));

      const double x = (p1.x() + p2.x())/2.0;
      const double y = (p1.y() + p2.y())/2.0;
      //
      const double z = p1.z() / p2.z();
      /// @todo Generally deal with +/- errors separately
      const double ez = z * sqrt( sqr(p1.yErrAvg()/p1.z()) + sqr(p2.yErrAvg()/p2.z()) );
      tmp.addPoint(x, p1.xErrMinus(), p1.xErrPlus(), 
                   y, p1.yErrMinus(), p1.yErrPlus(), z, ez, ez);
    }
    assert(tmp.numPoints() == numer.numPoints());
    return tmp;
  }


}
