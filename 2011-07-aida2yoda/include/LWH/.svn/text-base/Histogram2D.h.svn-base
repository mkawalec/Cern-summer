// -*- C++ -*-
#ifndef LWH_Histogram2D_H
#define LWH_Histogram2D_H
//
// This is the declaration of the Histogram1D class.
//

#include "AIHistogram2D.h"
#include "ManagedObject.h"
#include "Axis.h"
#include "VariAxis.h"
#include <vector>
#include <stdexcept>

#include <iostream>
#ifdef HAVE_ROOT
  #include "TH2D.h"
#endif



namespace LWH {

  using namespace AIDA;


  /**
   * User level interface to 1D Histogram.
   */
  class Histogram2D: public IHistogram2D, public ManagedObject {

  public:

    /** HistFactory is a friend. */
    friend class HistogramFactory;

  public:

    /**
     * Standard constructor.
     */
    Histogram2D(int nx, double lox, double upx,
                int ny, double loy, double upy)
      : xfax(new Axis(nx, lox, upx)), xvax(0), yfax(new Axis(ny, loy, upy)),
        sum(nx + 2, std::vector<int>(ny + 2)),
        sumw(nx + 2, std::vector<double>(ny + 2)),
        sumw2(nx + 2, std::vector<double>(ny + 2)),
        sumxw(nx + 2, std::vector<double>(ny + 2)),
        sumx2w(nx + 2, std::vector<double>(ny + 2)),
        sumyw(nx + 2, std::vector<double>(ny + 2)),
        sumy2w(nx + 2, std::vector<double>(ny + 2)) {
      xax = xfax;
      yax = yfax;
    }

    /**
     * Standard constructor for variable bin width.
     */
    Histogram2D(const std::vector<double> & xedges,
                const std::vector<double> & yedges)
      : xfax(0), xvax(new VariAxis(xedges)),
        yfax(0), yvax(new VariAxis(xedges)),
        sum(xedges.size() + 1, std::vector<int>(yedges.size() + 1)),
        sumw(xedges.size() + 1, std::vector<double>(yedges.size() + 1)),
        sumw2(xedges.size() + 1, std::vector<double>(yedges.size() + 1)),
        sumxw(xedges.size() + 1, std::vector<double>(yedges.size() + 1)),
        sumx2w(xedges.size() + 1, std::vector<double>(yedges.size() + 1)),
        sumyw(xedges.size() + 1, std::vector<double>(yedges.size() + 1)),
        sumy2w(xedges.size() + 1, std::vector<double>(yedges.size() + 1)) {
      xax = xvax;
      yax = yvax;
    }

    /**
     * Copy constructor.
     */
    Histogram2D(const Histogram2D & h)
      : IBaseHistogram(h), IHistogram(h), IHistogram2D(h), ManagedObject(h),
        xfax(0), xvax(0),  yfax(0), yvax(0),
        sum(h.sum), sumw(h.sumw), sumw2(h.sumw2),
        sumxw(h.sumxw), sumx2w(h.sumx2w) ,
        sumyw(h.sumyw), sumy2w(h.sumy2w){
      const VariAxis * hxvax = dynamic_cast<const VariAxis *>(h.xax);
      if ( hxvax ) xax = xvax = new VariAxis(*hxvax);
      else xax = xfax = new Axis(dynamic_cast<const Axis &>(*h.xax));
      const VariAxis * hyvax = dynamic_cast<const VariAxis *>(h.yax);
      if ( hyvax ) yax = yvax = new VariAxis(*hyvax);
      else yax = yfax = new Axis(dynamic_cast<const Axis &>(*h.yax));
  }

    /// Destructor.
    virtual ~Histogram2D() {
      delete xax;
      delete yax;
    }

    /**
     * Get the Histogram's title.
     * @return The Histogram's title.
     */
    // std::string title() const {
    //   return theTitle;
    // }

    /**
     * Get the Histogram's name.
     * @return The Histogram's name
     */
    std::string name() const {
      return title();
    }

    /**
     * Set the histogram title.
     * @param title The title.
     * @return false If title cannot be changed.
     */
    // bool setTitle(const std::string & title) {
    //   theTitle = title;
    //   return true;
    // }

    /**
     * Not implemented in LWH. will throw an exception.
     */
    IAnnotation & annotation() {
      throw std::runtime_error("LWH cannot handle annotations");
      return *anno;
    }

    /**
     * Not implemented in LWH. will throw an exception.
     */
    const IAnnotation & annotation() const {
      throw std::runtime_error("LWH cannot handle annotations");
      return *anno;
    }

    /**
     * Get the Histogram's dimension.
     * @return The Histogram's dimension.
     */
    int dimension() const {
      return 2;
    }

    /**
     * Reset the Histogram; as if just created.
     * @return false If something goes wrong.
     */
    bool reset() {
      const int nx = xax->bins() + 2;
      const int ny = yax->bins() + 2;
      sum = std::vector< std::vector<int> >(nx, std::vector<int>(ny));
      sumw = std::vector< std::vector<double> >(nx, std::vector<double>(ny));
      sumw2 = sumw;
      sumxw = sumw;
      sumx2w = sumw;
      sumyw = sumw;
      sumy2w = sumw;
      return true;
    }

    /**
     * Get the number of in-range entries in the Histogram.
     * @return The number of in-range entries.
     *
     */
    int entries() const {
      int si = 0;
      for ( int ix = 2; ix < xax->bins() + 2; ++ix )
        for ( int iy = 2; iy < yax->bins() + 2; ++iy ) si += sum[ix][iy];
      return si;
    }

    /**
     * Sum of the entries in all the IHistogram's bins,
     * i.e in-range bins, UNDERFLOW and OVERFLOW.
     * This is equivalent to the number of times the
     * method fill was invoked.
     * @return The sum of all the entries.
     */
    int allEntries() const {
      return entries() + extraEntries();
    }

    /**
     * Number of entries in the UNDERFLOW and OVERFLOW bins.
     * @return The number of entries outside the range of the IHistogram.
     */
    int extraEntries() const {
      int esum = sum[0][0] + sum[1][0] + sum[0][1] + sum[1][1];
      for ( int ix = 2; ix < xax->bins() + 2; ++ix )
        esum += sum[ix][0] + sum[ix][1];
      for ( int iy = 2; iy < yax->bins() + 2; ++iy )
        esum += sum[0][iy] + sum[1][iy];
      return esum;
    }

    /**
     * Number of equivalent entries,
     * i.e. <tt>SUM[ weight ] ^ 2 / SUM[ weight^2 ]</tt>
     * @return The number of equivalent entries.
     */
    double equivalentBinEntries() const {
      double sw = 0.0;
      double sw2 = 0.0;
      for ( int ix = 2; ix < xax->bins() + 2; ++ix )
        for ( int iy = 2; iy < yax->bins() + 2; ++iy ) {
          sw += sumw[ix][iy];
          sw2 += sumw2[ix][iy];
        }
      return sw2/(sw*sw);
    }

    /**
     * Sum of in-range bin heights in the IHistogram,
     * UNDERFLOW and OVERFLOW bins are excluded.
     * @return The sum of the in-range bins heights.
     *
     */
    double sumBinHeights() const {
      double sw = 0.0;
      for ( int ix = 2; ix < xax->bins() + 2; ++ix )
        for ( int iy = 2; iy < yax->bins() + 2; ++iy ) sw += sumw[ix][iy];
      return sw;
    }

    /**
     * Sum of the heights of all the IHistogram's bins,
     * i.e in-range bins, UNDERFLOW and OVERFLOW.
     * @return The sum of all the bins heights.
     */
    double sumAllBinHeights() const {
      return sumBinHeights() + sumExtraBinHeights();
    }

    /**
     * Sum of heights in the UNDERFLOW and OVERFLOW bins.
     * @return The sum of the heights of the out-of-range bins.
     */
    double sumExtraBinHeights() const {
      double esum = sumw[0][0] + sumw[1][0] + sumw[0][1] + sumw[1][1];
      for ( int ix = 2; ix < xax->bins() + 2; ++ix )
        esum += sumw[ix][0] + sumw[ix][1];
      for ( int iy = 2; iy < yax->bins() + 2; ++iy )
        esum += sumw[0][iy] + sumw[1][iy];
      return esum;
    }

    /**
     * Minimum height of the in-range bins,
     * i.e. not considering the UNDERFLOW and OVERFLOW bins.
     * @return The minimum height among the in-range bins.
     */
    double minBinHeight() const {
      double minw = sumw[2][2];
      for ( int ix = 2; ix < xax->bins() + 2; ++ix )
        for ( int iy = 2; iy < yax->bins() + 2; ++iy )
          minw = std::min(minw, sumw[ix][iy]);
      return minw;
    }

    /**
     * Maximum height of the in-range bins,
     * i.e. not considering the UNDERFLOW and OVERFLOW bins.
     * @return The maximum height among the in-range bins.
     */
    double maxBinHeight() const{
      double maxw = sumw[2][2];
      for ( int ix = 2; ix < xax->bins() + 2; ++ix )
        for ( int iy = 2; iy < yax->bins() + 2; ++iy )
          maxw = std::max(maxw, sumw[ix][iy]);
      return maxw;
    }

    /**
     * Fill the IHistogram1D with a value and the
     * corresponding weight.
     * @param x      The value to be filled in.
     * @param weight The corresponding weight (by default 1).
     * @return false If the weight is <0 or >1 (?).
     */
    bool fill(double x, double y, double weight = 1.) {
      int ix = xax->coordToIndex(x) + 2;
      int iy = yax->coordToIndex(y) + 2;
      ++sum[ix][iy];
      sumw[ix][iy] += weight;
      sumxw[ix][iy] += x*weight;
      sumx2w[ix][iy] += x*x*weight;
      sumyw[ix][iy] += y*weight;
      sumy2w[ix][iy] += y*y*weight;
      sumw2[ix][iy] += weight*weight;
      return weight >= 0 && weight <= 1;
    }

    /**
     * The weighted mean along the x-axis of a bin.
     * @param xindex The bin number (0...N-1) or OVERFLOW or UNDERFLOW.
     * @param yindex The bin number (0...N-1) or OVERFLOW or UNDERFLOW.
     * @return      The mean of the corresponding bin.
     */
    double binMeanX(int xindex, int yindex) const {
      int ix = xindex + 2;
      int iy = yindex + 2;
      return sumw[ix][iy] != 0.0? sumxw[ix][iy]/sumw[ix][iy]:
        ( xvax? xvax->binMidPoint(xindex): xfax->binMidPoint(xindex) );
    };

    /**
     * The weighted mean along the y-axis of a bin.
     * @param xindex The bin number (0...N-1) or OVERFLOW or UNDERFLOW.
     * @param yindex The bin number (0...N-1) or OVERFLOW or UNDERFLOW.
     * @return      The mean of the corresponding bin.
     */
    double binMeanY(int xindex, int yindex) const {
      int ix = xindex + 2;
      int iy = yindex + 2;
      return sumw[ix][iy] != 0.0? sumyw[ix][iy]/sumw[ix][iy]:
        ( yvax? yvax->binMidPoint(yindex): xfax->binMidPoint(yindex) );
    };

    /**
     * The weighted x-RMS of a bin.
     * @param xindex The bin number (0...N-1) or OVERFLOW or UNDERFLOW.
     * @param yindex The bin number (0...N-1) or OVERFLOW or UNDERFLOW.
     * @return      The RMS of the corresponding bin.
     */
    double binRmsX(int xindex, int yindex) const {
      int ix = xindex + 2;
      int iy = yindex + 2;
      return sumw[ix][iy] == 0.0 || sum[ix][iy] < 2? xax->binWidth(xindex):
        std::sqrt(std::max(sumw[ix][iy]*sumx2w[ix][iy] -
                           sumxw[ix][iy]*sumxw[ix][iy], 0.0))/sumw[ix][iy];
    };

    /**
     * The weighted y-RMS of a bin.
     * @param xindex The bin number (0...N-1) or OVERFLOW or UNDERFLOW.
     * @param yindex The bin number (0...N-1) or OVERFLOW or UNDERFLOW.
     * @return      The RMS of the corresponding bin.
     */
    double binRmsY(int xindex, int yindex) const {
      int ix = xindex + 2;
      int iy = yindex + 2;
      return sumw[ix][iy] == 0.0 || sum[ix][iy] < 2? yax->binWidth(yindex):
        std::sqrt(std::max(sumw[ix][iy]*sumy2w[ix][iy] -
                           sumyw[ix][iy]*sumyw[ix][iy], 0.0))/sumw[ix][iy];
    };

    /**
     * Number of entries in the corresponding bin (ie the number of
     * times fill was called for this bin).
     * @param index The bin number (0...N-1) or OVERFLOW or UNDERFLOW.
     * @return      The number of entries in the corresponding bin.
     */
    int binEntries(int xindex, int yindex) const {
      return sum[xindex + 2][yindex + 2];
    }

    /**
     * Sum of all the entries of the bins along a given x bin.
     * This is equivalent to <tt>projectionX().binEntries(index)</tt>.
     * @param index The x bin number (0...N-1) or OVERFLOW or UNDERFLOW.
     * @return      The number of entries in the corresponding set of bins.
     *
     */
    virtual int binEntriesX(int index) const {
      int ret = 0;
      for ( int iy = 2; iy < yax->bins() + 2; ++iy )
        ret += sum[index + 2][iy];
      return ret;
    }

    /**
     * Sum of all the entries of the bins along a given y bin.
     * This is equivalent to <tt>projectionY().binEntries(index)</tt>.
     * @param index The y bin number (0...N-1) or OVERFLOW or UNDERFLOW.
     * @return      The number of entries in the corresponding set of bins.
     *
     */
    virtual int binEntriesY(int index) const {
      int ret = 0;
      for ( int ix = 2; ix < xax->bins() + 2; ++ix )
        ret += sum[ix][index + 2];
      return ret;
    }

    /**
     * Total height of the corresponding bin (ie the sum of the weights
     * in this bin).
     * @param index The bin number (0...N-1) or OVERFLOW or UNDERFLOW.
     * @return      The height of the corresponding bin.
     */
    double binHeight(int xindex, int yindex) const {
      /// @todo While this is compatible with the reference AIDA
      /// implementation, it is not the bin height!
      return sumw[xindex + 2][yindex + 2];
    }

    /**
     * Sum of all the heights of the bins along a given x bin.
     * This is equivalent to <tt>projectionX().binHeight(index)</tt>.
     * @param index The x bin number (0...N-1) or OVERFLOW or UNDERFLOW.
     * @return      The sum of the heights in the corresponding set of bins.
     *
     */
    virtual double binHeightX(int index) const {
      double ret = 0;
      for ( int iy = 2; iy < yax->bins() + 2; ++iy )
        ret += sumw[index + 2][iy];
      return ret;
    }

    /**
     * Sum of all the heights of the bins along a given y bin.
     * This is equivalent to <tt>projectionY().binHeight(index)</tt>.
     * @param index The y bin number (0...N-1) or OVERFLOW or UNDERFLOW.
     * @return      The sum of the heights in the corresponding set of bins.
     *
     */
    virtual double binHeightY(int index) const {
      double ret = 0;
      for ( int ix = 2; ix < xax->bins() + 2; ++ix )
        ret += sumw[ix][index + 2];
      return ret;
    }

    /**
     * The error of a given bin.
     * @param index The bin number (0...N-1) or OVERFLOW or UNDERFLOW.
     * @return      The error on the corresponding bin.
     *
     */
    double binError(int xindex, int yindex) const {
      return std::sqrt(sumw2[xindex + 2][yindex + 2]);
    }

    /**
     * The mean of the IHistogram2D along the x axis.
     * @return The mean of the IHistogram2D along the x axis.
     *
     */
    double meanX() const {
      double s = 0.0;
      double sx = 0.0;
      for ( int ix = 2; ix < xax->bins() + 2; ++ix )
        for ( int iy = 2; iy < yax->bins() + 2; ++iy ) {
        s += sumw[ix][iy];
        sx += sumxw[ix][iy];
      }
      return s != 0.0? sx/s: 0.0;
    }

    /**
     * The mean of the IHistogram2D along the y axis.
     * @return The mean of the IHistogram2D along the y axis.
     *
     */
    double meanY() const {
      double s = 0.0;
      double sy = 0.0;
      for ( int ix = 2; ix < xax->bins() + 2; ++ix )
        for ( int iy = 2; iy < yax->bins() + 2; ++iy ) {
        s += sumw[ix][iy];
        sy += sumyw[ix][iy];
      }
      return s != 0.0? sy/s: 0.0;
    }

    /**
     * The RMS of the IHistogram2D along the x axis.
     * @return The RMS if the IHistogram2D along the x axis.
     *
     */
    double rmsX() const {
      double s = 0.0;
      double sx = 0.0;
      double sx2 = 0.0;
      for ( int ix = 2; ix < xax->bins() + 2; ++ix )
        for ( int iy = 2; iy < yax->bins() + 2; ++iy ) {
        s += sumw[ix][iy];
        sx += sumxw[ix][iy];
        sx2 += sumx2w[ix][iy];
      }
      return s != 0.0? std::sqrt(std::max(s*sx2 - sx*sx, 0.0))/s:
        xax->upperEdge() - xax->lowerEdge();
    }

    /**
     * The RMS of the IHistogram2D along the x axis.
     * @return The RMS if the IHistogram2D along the x axis.
     *
     */
    double rmsY() const {
      double s = 0.0;
      double sy = 0.0;
      double sy2 = 0.0;
      for ( int ix = 2; ix < xax->bins() + 2; ++ix )
        for ( int iy = 2; iy < yax->bins() + 2; ++iy ) {
        s += sumw[ix][iy];
        sy += sumyw[ix][iy];
        sy2 += sumy2w[ix][iy];
      }
      return s != 0.0? std::sqrt(std::max(s*sy2 - sy*sy, 0.0))/s:
        yax->upperEdge() - yax->lowerEdge();
    }

    /** The weights. */
    double getSumW(int xindex, int yindex) const {
        return sumw[xindex + 2][yindex + 2];
    }

    /** The squared weights. */
    double getSumW2(int xindex, int yindex) const {
        return sumw2[xindex + 2][yindex + 2];
    }

    /** The weighted x-values. */
    double getSumXW(int xindex, int yindex) const {
        return sumxw[xindex + 2][yindex + 2];
    }

    /** The weighted x-square-values. */
    double getSumX2W(int xindex, int yindex) const {
        return sumx2w[xindex + 2][yindex + 2];
    }

    /** The weighted x-values. */
    double getSumYW(int xindex, int yindex) const {
        return sumyw[xindex + 2][yindex + 2];
    }

    /** The weighted x-square-values. */
    double getSumY2W(int xindex, int yindex) const {
        return sumy2w[xindex + 2][yindex + 2];
    }

    /**
     * Get the x axis of the IHistogram2D.
     * @return The x coordinate IAxis.
     */
    const IAxis & xAxis() const {
      return *xax;
    }

    /**
     * Get the y axis of the IHistogram2D.
     * @return The y coordinate IAxis.
     */
    const IAxis & yAxis() const {
      return *yax;
    }

    /**
     * Get the bin number corresponding to a given coordinate along the
     * x axis.  This is a convenience method, equivalent to
     * <tt>axis().coordToIndex(coord)</tt>.
     * @param coord The coordinalte along the x axis.
     * @return      The corresponding bin number.
     */
    int coordToIndexX(double coord) const {
      return xax->coordToIndex(coord);
    }

    /**
     * Get the bin number corresponding to a given coordinate along the
     * y axis.  This is a convenience method, equivalent to
     * <tt>axis().coordToIndex(coord)</tt>.
     * @param coord The coordinalte along the y axis.
     * @return      The corresponding bin number.
     */
    int coordToIndexY(double coord) const {
      return yax->coordToIndex(coord);
    }

    /**
     * Add to this Histogram2D the contents of another IHistogram2D.
     * @param h The Histogram2D to be added to this IHistogram2D.
     * @return false If the IHistogram1Ds binnings are incompatible.
     */
    bool add(const Histogram2D & h) {
      if ( xax->upperEdge() != h.xax->upperEdge() ||
           xax->lowerEdge() != h.xax->lowerEdge() ||
           xax->bins() != h.xax->bins() ) return false;
      if ( yax->upperEdge() != h.yax->upperEdge() ||
           yax->lowerEdge() != h.yax->lowerEdge() ||
           yax->bins() != h.yax->bins() ) return false;
      for ( int ix = 0; ix < xax->bins() + 2; ++ix )
        for ( int iy = 0; iy < yax->bins() + 2; ++iy ) {
          sum[ix][iy] += h.sum[ix][iy];
          sumw[ix][iy] += h.sumw[ix][iy];
          sumxw[ix][iy] += h.sumxw[ix][iy];
          sumx2w[ix][iy] += h.sumx2w[ix][iy];
          sumyw[ix][iy] += h.sumyw[ix][iy];
          sumy2w[ix][iy] += h.sumy2w[ix][iy];
          sumw2[ix][iy] += h.sumw2[ix][iy];
        }
      return true;
    }

    /**
     * Add to this IHistogram1D the contents of another IHistogram1D.
     * @param hist The IHistogram1D to be added to this IHistogram1D.
     * @return false If the IHistogram1Ds binnings are incompatible.
     */
    bool add(const IHistogram2D & hist) {
      return add(dynamic_cast<const Histogram2D &>(hist));
    }

    /**
     * Scale the contents of this histogram with the given factor.
     * @param s the scaling factor to use.
     */
    bool scale(double s) {
      for ( int ix = 0; ix < xax->bins() + 2; ++ix )
        for ( int iy = 0; iy < yax->bins() + 2; ++iy ) {
          sumw[ix][iy] *= s;
          sumxw[ix][iy] *= s;
          sumx2w[ix][iy] *= s;
          sumyw[ix][iy] *= s;
          sumy2w[ix][iy] *= s;
          sumw2[ix][iy] *= s*s;
      }
      return true;
    }

    /**
     * Scale the given histogram so that the integral over all bins
     * (including overflow) gives \a intg. This function also corrects
     * for the bin-widths, which means that it should only be run once
     * for each histogram. Further rescaling must be done with the
     * scale(double) function.
     */
    void normalize(double intg) {
      double oldintg = sumAllBinHeights();
      if ( oldintg == 0.0 ) return;
      for ( int ix = 0; ix < xax->bins() + 2; ++ix )
        for ( int iy = 0; iy < yax->bins() + 2; ++iy ) {
          double fac = intg/oldintg;
          if ( ix >= 2 && iy >= 2 )
            fac /= (xax->binUpperEdge(ix - 2) - xax->binLowerEdge(ix - 2))*
              (yax->binUpperEdge(iy - 2) - yax->binLowerEdge(iy - 2));
        sumw[ix][iy] *= fac;
        sumxw[ix][iy] *= fac;
        sumx2w[ix][iy] *= fac;
        sumyw[ix][iy] *= fac;
        sumy2w[ix][iy] *= fac;
        sumw2[ix][iy] *= fac*fac;
      }
    }

    /**
     * Return the integral over the histogram bins assuming it has been
     * normalize()d.
     */
    // double integral() const {
    //   double intg = sumw[0] + sumw[1];
    //   for ( int i = 2; i < ax->bins() + 2; ++i )

    // is this right? Leave out bin width factor?

    //     intg += sumw[ix][iy]*(ax->binUpperEdge(i - 2) - ax->binLowerEdge(i - 2));
    //   return intg;
    // }

    /**
     * Not implemented in LWH.
     * @return null pointer always.
     */
    void * cast(const std::string &) const {
      return 0;
    }

    /**
     * Write out the histogram in the AIDA xml format.
     */
    bool writeXML(std::ostream & os, std::string path, std::string name) {
      //std::cout << "Writing out histogram " << name << " in AIDA file format!" << std::endl;
      os << "  <histogram2d name=\"" << encodeForXML(name)
         << "\"\n    title=\"" << encodeForXML(title())
         << "\" path=\"" << path
         << "\">\n    <axis max=\"" << xax->upperEdge()
         << "\" numberOfBins=\"" << xax->bins()
         << "\" min=\"" << xax->lowerEdge()
         << "\" direction=\"x\"";
      if ( xvax ) {
        os << ">\n";
        for ( int i = 0, N = xax->bins() - 1; i < N; ++i )
          os << "      <binBorder value=\"" << xax->binUpperEdge(i) << "\"/>\n";
        os << "    </axis>\n";
      } else {
        os << "/>\n";
      }
      os << "    <axis max=\"" << yax->upperEdge()
         << "\" numberOfBins=\"" << yax->bins()
         << "\" min=\"" << yax->lowerEdge()
         << "\" direction=\"y\"";
      if ( yvax ) {
        os << ">\n";
        for ( int i = 0, N = yax->bins() - 1; i < N; ++i )
          os << "      <binBorder value=\"" << yax->binUpperEdge(i) << "\"/>\n";
        os << "    </axis>\n";
      } else {
        os << "/>\n";
      }
      os << "    <statistics entries=\"" << entries()
         << "\">\n      <statistic mean=\"" << meanX()
         << "\" direction=\"x\"\n        rms=\"" << rmsX()
         << "\"/>\n    </statistics>\n"
         << "    <statistics entries=\"" << entries()
         << "\">\n      <statistic mean=\"" << meanY()
         << "\" direction=\"y\"\n        rms=\"" << rmsY()
         << "\"/>\n    </statistics>\n    <data2d>\n";
      for ( int ix = 0; ix < xax->bins() + 2; ++ix )
        for ( int iy = 0; iy < yax->bins() + 2; ++iy )
          if ( sum[ix][iy] ) {
            os << "      <bin2d binNumX=\"";
            if ( ix == 0 ) os << "UNDERFLOW";
            else if ( ix == 1 ) os << "OVERFLOW";
            else os << ix - 2;
            os << "\" binNumY=\"";
            if ( iy == 0 ) os << "UNDERFLOW";
            else if ( iy == 1 ) os << "OVERFLOW";
            else os << iy - 2;
            os << "\" entries=\"" << sum[ix][iy]
               << "\" height=\"" << sumw[ix][iy]
               << "\"\n        error=\"" << std::sqrt(sumw2[ix][iy])
               << "\" error2=\"" << sumw2[ix][iy]
               << "\"\n        weightedMeanX=\"" << binMeanX(ix - 2, iy - 2)
               << "\" weightedRmsX=\"" << binRmsX(ix - 2, iy - 2)
               << "\"\n        weightedMeanY=\"" << binMeanY(ix - 2, iy - 2)
               << "\" weightedRmsY=\"" << binRmsY(ix - 2, iy - 2)
               << "\"/>\n";
        }
      os << "    </data2d>\n  </histogram2d>" << std::endl;
      return true;
    }


    /**
     * Write out the histogram in a flat text file suitable for
     * eg. gnuplot to read. The coloums are layed out as 'x w w2 n'.
     */
    bool writeFLAT(std::ostream & os, std::string path, std::string name) {
      os << "#2D " << path << "/" << name << " " << xax->lowerEdge()
         << " " << xax->bins() << " " << xax->upperEdge() << " "
         << yax->lowerEdge() << " " << yax->bins() << " " << yax->upperEdge()
         << " \"" << title() << "\"" << std::endl;
      for ( int ix = 2; ix < xax->bins() + 2; ++ix ) {
        for ( int iy = 2; iy < yax->bins() + 2; ++iy )
          os << 0.5*(xax->binLowerEdge(ix - 2)+xax->binUpperEdge(ix - 2)) << " "
             << 0.5*(yax->binLowerEdge(iy - 2)+yax->binUpperEdge(iy - 2))
             << " " << sumw[ix][iy] << " " << sqrt(sumw2[ix][iy])
             << " " << sum[ix][iy] << std::endl;
        os << std::endl;
      }
      os << std::endl;
      return true;
    }



   #ifdef HAVE_ROOT
    /**
     * Write out the histogram in Root file format.
     */
    //bool writeROOT(std::ostream & os, std::string path, std::string name) {
    bool writeROOT(TFile* file, std::string path, std::string name) {

      //std::cout << "Writing out histogram " << name.c_str() << " in ROOT file format" << std::endl;

      TH1D* hist1d;
      int nbins;
      if (!vax || vax->isFixedBinning() ) {//equidistant binning (easier case)
        nbins = ax->bins();
        hist1d = new TH1D(name.c_str(), title().c_str(), nbins, ax->lowerEdge(), ax->upperEdge());
      }
      else {
        nbins = vax->bins();
        double* bins = new double[nbins+1];
        for (int i=0; i<nbins; ++i) {
      bins[ix][iy] = vax->binEdges(i).first;
        }
        bins[nbins] = vax->binEdges(nbins-1).second; //take last bin right border
        hist1d = new TH1D(name.c_str(), title().c_str(), nbins, bins);
        delete bins;
      }


      double entries = 0;
      for ( int i = 0; i < nbins + 2; ++i ) {
        if ( sum[ix][iy] ) {
          //i==0: underflow->RootBin(0), i==1: overflow->RootBin(NBins+1)
          entries = entries + sum[ix][iy];
          int j=i;
          if (i==0) j=0; //underflow
          else if (i==1) j=nbins+1; //overflow
          if (i>=2) j=i-1; //normal bin entries
          hist1d->SetBinContent(j, sumw[ix][iy]);
          hist1d->SetBinError(j, sqrt(sumw2[ix][iy]));
          //hist1d->Fill(binMean(i), sumw[ix][iy]);
        }
      }

      hist1d->Sumw2();
      hist1d->SetEntries(entries);

      std::string DirName; //remove preceding slash from directory name, else ROOT error
      for (unsigned int i=1; i<path.size(); ++i) DirName += path[i];
      if (!file->Get(DirName.c_str())) file->mkdir(DirName.c_str());
      file->cd(DirName.c_str());
      hist1d->Write();

      delete hist1d;

      return true;
    }

   #endif



  private:

    /** The title */
    // std::string theTitle;

    /** The axis. */
    IAxis * xax;

    /** Pointer (possibly null) to a axis with fixed bin width. */
    Axis * xfax;

    /** Pointer (possibly null) to a axis with fixed bin width. */
    VariAxis * xvax;

    /** The axis. */
    IAxis * yax;

    /** Pointer (possibly null) to a axis with fixed bin width. */
    Axis * yfax;

    /** Pointer (possibly null) to a axis with fixed bin width. */
    VariAxis * yvax;

    /** The counts. */
    std::vector< std::vector<int> > sum;

    /** The weights. */
    std::vector< std::vector<double> > sumw;

    /** The squared weights. */
    std::vector< std::vector<double> > sumw2;

    /** The weighted x-values. */
    std::vector< std::vector<double> > sumxw;

    /** The weighted x-square-values. */
    std::vector< std::vector<double> > sumx2w;

    /** The weighted y-values. */
    std::vector< std::vector<double> > sumyw;

    /** The weighted y-square-values. */
    std::vector< std::vector<double> > sumy2w;

    /** dummy pointer to non-existen annotation. */
    IAnnotation * anno;

  };

}

#endif /* LWH_Histogram1D_H */
