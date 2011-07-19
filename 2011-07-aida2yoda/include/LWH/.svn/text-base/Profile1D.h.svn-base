// -*- C++ -*-
#ifndef LWH_Profile1D_H
#define LWH_Profile1D_H
//
// This is the declaration of the Profile1D class.
//

#include "AIProfile1D.h"
#include "ManagedObject.h"
#include "Axis.h"
#include "VariAxis.h"
#include <vector>
#include <stdexcept>
#include <cassert>

#include <iostream>
#ifdef HAVE_ROOT
  #include "TProfile.h"
#endif



namespace LWH {

using namespace AIDA;

/**
 * User level interface to 1D Profile.
 */
class Profile1D: public IProfile1D, public ManagedObject {

public:

  /** HistFactory is a friend. */
  friend class HistogramFactory;

public:

  /**
   * Standard constructor.
   */
  Profile1D(int n, double lo, double up)
    : fax(new Axis(n, lo, up)), vax(0),
      sum(n + 2), sumw(n + 2), sumw2(n + 2), sumxw(n + 2), sumx2w(n + 2), sumyw(n + 2), sumy2w(n + 2), sumy2w2(n + 2) {
    ax = fax;
  }


  /**
   * Standard constructor for variable bin width.
   */
  Profile1D(const std::vector<double> & edges)
    : fax(0), vax(new VariAxis(edges)),
      sum(edges.size() + 1), sumw(edges.size() + 1), sumw2(edges.size() + 1),
      sumxw(edges.size() + 1), sumx2w(edges.size() + 1), sumyw(edges.size() + 1),
      sumy2w(edges.size() + 1), sumy2w2(edges.size() + 1) {
    ax = vax;
  }


  /**
   * Copy constructor.
   */
  Profile1D(const Profile1D & h)
    : IBaseHistogram(h), IProfile(h), IProfile1D(h), ManagedObject(h),
      fax(0), vax(0), sum(h.sum), sumw(h.sumw), sumw2(h.sumw2),
      sumxw(h.sumxw), sumx2w(h.sumx2w), sumyw(h.sumyw), sumy2w(h.sumy2w),
      sumy2w2(h.sumy2w2) {
    const VariAxis * hvax = dynamic_cast<const VariAxis *>(h.ax);
    if ( hvax ) ax = vax = new VariAxis(*hvax);
    else ax = fax = new Axis(dynamic_cast<const Axis &>(*h.ax));
  }


  /// Destructor.
  virtual ~Profile1D() {
    delete ax;
  }

  /**
   * Get the Profile's title.
   * @return The Profile's title.
   */
  // std::string title() const {
  //   return theTitle;
  // }

  /**
   * Get the Profile's name.
   * @return The Profile's name
   */
  std::string name() const {
    return theTitle;
  }

  /**
   * Set the profile title.
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
   * Get the Profile's dimension.
   * @return The Profile's dimension.
   */
  int dimension() const {
    return 1;
  }



  /**
   * Reset the Histogram; as if just created.
   * @return false If something goes wrong.
   */
  bool reset() {
    sum = std::vector<int>(ax->bins() + 2);
    sumw = std::vector<double>(ax->bins() + 2);
    sumxw = std::vector<double>(ax->bins() + 2);
    sumx2w = std::vector<double>(ax->bins() + 2);
    sumyw = std::vector<double>(ax->bins() + 2);
    sumy2w = std::vector<double>(ax->bins() + 2);
    sumy2w2 = std::vector<double>(ax->bins() + 2);
    sumw2 = std::vector<double>(ax->bins() + 2);
    return true;
  }

  /**
   * Get the number of in-range entries in the Histogram.
   * @return The number of in-range entries.
   *
   */
  int entries() const {
    int si = 0;
    for ( int i = 2; i < ax->bins() + 2; ++i ) si += sum[i];
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
    return sum[0] + sum[1];
  }

  /**
   * Number of equivalent entries,
   * i.e. <tt>SUM[ weight ] ^ 2 / SUM[ weight^2 ]</tt>
   * @return The number of equivalent entries.
   */
  double equivalentBinEntries() const {
    double sw = 0.0;
    double sw2 = 0.0;
    for ( int i = 2; i < ax->bins() + 2; ++i ) {
      sw += sumw[i];
      sw2 += sumw2[i];
    }
    return sw2/(sw*sw);
  }

  /**
   * Sum of weighted in-range bin profile heights in the IProfile,
   * UNDERFLOW and OVERFLOW bins are excluded.
   * @return The sum of the in-range bins heights.
   *
   */
  double sumBinHeights() const {
    double sw = 0.;
    double syw = 0.;
    for ( int i = 2; i < ax->bins() + 2; ++i ) {
      syw += sumyw[i];
      sw += sumw[i];
    }
    double sBH = 0.;
    if (sw > 0.) sBH = syw/sw;
    return sBH;
  }

  /**
   * Sum of the heights of all the IHistogram's bins,
   * i.e in-range bins, UNDERFLOW and OVERFLOW.
   * @return The sum of all the bins heights.
   */
  double sumAllBinHeights() const {
    double sw = 0.;
    double syw = 0.;
    for ( int i = 0; i < ax->bins() + 2; ++i ) {
      syw += sumyw[i];
      sw += sumw[i];
    }
    double sABH = 0.;
    if (sw > 0.) sABH = syw/sw;
    return sABH;
  }

  /**
   * Sum of heights in the UNDERFLOW and OVERFLOW bins.
   * @return The sum of the heights of the out-of-range bins.
   */
  double sumExtraBinHeights() const {
    double sw = sumw[0] + sumw[1];
    double syw = sumyw[0] + sumyw[1];
    double sEBH = 0.;
    if (sw > 0.) sEBH = syw/sw;
    return sEBH;
  }

  /**
   * Minimum height of the in-range bins,
   * i.e. not considering the UNDERFLOW and OVERFLOW bins.
   * @return The minimum height among the in-range bins.
   */
  double minBinHeight() const {
    double minw = 0.;
    bool first = true;
    for ( int i = 3; i < ax->bins() + 2; ++i ) {
      if (sumw[i] > 0.) {
        double yw = sumyw[i]/sumw[i];
        if (first) {
          minw = yw;
          first = false;
        }
        else if (yw < minw) minw = yw;
      }
    }
    return minw;
  }

  /**
   * Maximum height of the in-range bins,
   * i.e. not considering the UNDERFLOW and OVERFLOW bins.
   * @return The maximum height among the in-range bins.
   */
  double maxBinHeight() const{
    double maxw = 0.;
    bool first = true;
    for ( int i = 3; i < ax->bins() + 2; ++i ) {
      if (sumw[i] > 0.) {
        double yw = sumyw[i]/sumw[i];
        if (first) {
          maxw = yw;
          first = false;
        }
        else if (yw > maxw) maxw = yw;
      }
    }
    return maxw;
  }

  /**
   * Fill the IProfile1D with a value and the
   * corresponding weight.
   * @param x      The x value to be filled in.
   * @param y      The y value to be filled in.
   * @param weight The corresponding weight (by default 1).
   * @return false If the weight is <0 or >1 (?).
   */
  bool fill(double x, double y, double weight = 1.) {
    int i = ax->coordToIndex(x) + 2;
    ++sum[i];
    sumw[i] += weight;
    sumxw[i] += x*weight;
    sumx2w[i] += x*x*weight;
    sumyw[i] += y*weight;
    sumy2w[i] += y*y*weight;
    sumy2w2[i] += y*y*weight*weight;
    sumw2[i] += weight*weight;
    return weight >= 0 && weight <= 1;
  }

  /**
   * The weighted mean of a bin.
   * @param index The bin number (0...N-1) or OVERFLOW or UNDERFLOW.
   * @return      The mean in x of the corresponding bin.
   */
  double binMean(int index) const {
    int i = index + 2;
    return sumw[i] != 0.0? sumxw[i]/sumw[i]:
      ( vax? vax->binMidPoint(index): fax->binMidPoint(index) );
  };

  /**
   * The weighted RMS of a bin.
   * @param index The bin number (0...N-1) or OVERFLOW or UNDERFLOW.
   * @return      The RMS in x of the corresponding bin.
   */
  double binRms(int index) const {
    int i = index + 2;
    return sumw[i] == 0.0 || sum[i] < 2? ax->binWidth(index):
      std::sqrt(std::max(sumw[i]*sumx2w[i] - sumxw[i]*sumxw[i], 0.0))/sumw[i];
  };

  /**
   * Number of entries in the corresponding bin (ie the number of
   * times fill was called for this bin).
   * @param index The bin number (0...N-1) or OVERFLOW or UNDERFLOW.
   * @return      The number of entries in the corresponding bin.
   */
  int binEntries(int index) const {
    return sum[index + 2];
  }

  /**
   * Total height of the corresponding bin (ie sumyw/sumw = mean in y
   * in this bin).
   * @param index The bin number (0...N-1) or OVERFLOW or UNDERFLOW.
   * @return      The weight of the corresponding bin.
   */
  double binHeight(int index) const {
    double bH = 0.;
    if (sumw[index+2] != 0. && sumyw[index+2] != 0.)
      bH = sumyw[index+2]/sumw[index+2];
    return bH;
  }

  /**
   * The correctly weighted error of a given bin.
   * @param index The bin number (0...N-1) or OVERFLOW or UNDERFLOW.
   * @return      The error on the corresponding bin.
   *
   */
  double binError(int index) const {
    const size_t i = index + 2;
    if (sumw[i] > 0.0) {
      const double n_eff = sumw[i]*sumw[i] / sumw2[i];
      if (n_eff <= 1.0) {
        return sumyw[i]/n_eff;
      }
      const double denom = sumw[i]*sumw[i] - sumw2[i];
      const double numer = sumy2w[i]*sumw[i] - sumyw[i]*sumyw[i];
      assert(denom > 0);
      const double variance = numer/denom;
      /// @todo Is this biasing again? I.e. do we actually need a 1 / (n_eff - 1)?
      const double std_var = variance / n_eff;
      if (std_var > 0.0) {
        const double std_err = sqrt(std_var);
        // std::cout << "@@ " << index << " " << std_err << " " << sumyw[i]/sumw[i] << std::endl;
        return std_err;
      }
    }
    return 0.0;
  }

  /**
   * The mean in x of the whole IProfile1D.
   * @return The mean in x of the IProfile1D.
   */
  double mean() const {
    double s = 0.0;
    double sx = 0.0;
    for ( int i = 2; i < ax->bins() + 2; ++i ) {
      s += sumw[i];
      sx += sumxw[i];
    }
    return s != 0.0? sx/s: 0.0;
  }

  /**
   * The RMS in x of the whole IProfile1D.
   * @return The RMS in x if the IProfile1D.
   */
  double rms() const {
    double s = 0.0;
    double sx = 0.0;
    double sx2 = 0.0;
    for ( int i = 2; i < ax->bins() + 2; ++i ) {
      s += sumw[i];
      sx += sumxw[i];
      sx2 += sumx2w[i];
    }
    return s != 0.0? std::sqrt(std::max(s*sx2 - sx*sx, 0.0))/s:
      ax->upperEdge() - ax->lowerEdge();
  }


  /** The weights. */
  double getSumW(int index) const {
      return sumw[index + 2];
  }

  /** The squared weights. */
  double getSumW2(int index) const {
      return sumw2[index + 2];
  }

  /** The weighted x-values. */
  double getSumXW(int index) const {
      return sumxw[index + 2];
  }

  /** The weighted x-square-values. */
  double getSumX2W(int index) const {
      return sumx2w[index + 2];
  }

  /** The weighted y-values. */
  double getSumYW(int index) const {
      return sumyw[index + 2];
  }

  /** The weighted y-square-values. */
  double getSumY2W(int index) const {
      return sumy2w[index + 2];
  }

  /** The squared weighted y-square-values. */
  double getSumY2W2(int index) const {
      return sumy2w2[index + 2];
  }

  /**
   * Get the x axis of the IHistogram1D.
   * @return The x coordinate IAxis.
   */
  const IAxis & axis() const {
    return *ax;
  }

  /**
   * Get the bin number corresponding to a given coordinate along the
   * x axis.  This is a convenience method, equivalent to
   * <tt>axis().coordToIndex(coord)</tt>.
   * @param coord The coordinalte along the x axis.
   * @return      The corresponding bin number.
   */
  int coordToIndex(double coord) const {
    return ax->coordToIndex(coord);
  }

  /**
   * Add to this Profile1D the contents of another IProfile1D.
   * @param h The Profile1D to be added to this IProfile1D.
   * @return false If the IProfile1Ds binnings are incompatible.
   */
  bool add(const Profile1D & h) {
    if ( ax->upperEdge() != h.ax->upperEdge() ||
         ax->lowerEdge() != h.ax->lowerEdge() ||
         ax->bins() != h.ax->bins() ) return false;
    for ( int i = 0; i < ax->bins() + 2; ++i ) {
      sum[i] += h.sum[i];
      sumw[i] += h.sumw[i];
      sumxw[i] += h.sumxw[i];
      sumx2w[i] += h.sumx2w[i];
      sumyw[i] += h.sumxw[i];
      sumy2w[i] += h.sumx2w[i];
      sumy2w2[i] += h.sumxw[i];
      sumw2[i] += h.sumw2[i];
    }
    return true;
  }

  /**
   * Add to this IProfile1D the contents of another IProfile1D.
   * @param hist The IProfile1D to be added to this IProfile1D.
   * @return false If the IProfile1Ds binnings are incompatible.
   */
  bool add(const IProfile1D & hist) {
    return add(dynamic_cast<const Profile1D &>(hist));
  }

  /**
   * Scale the contents of this profile histogram with the given factor.
   * @param s the scaling factor to use.
   */
  bool scale(double s) {
    for ( int i = 0; i < ax->bins() + 2; ++i ) {
      sumw[i] *= s;
      sumxw[i] *= s;
      sumx2w[i] *= s;
      sumyw[i] *= s;
      sumy2w[i] *= s;
      sumy2w2[i] *= s*s;
      sumw2[i] *= s*s;
    }
    return true;
  }

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
    //std::cout << "Writing out profile histogram " << name << " in AIDA file format!" <<std::endl;
    os << "  <profile1d name=\"" << encodeForXML(name)
       << "\"\n    title=\"" << encodeForXML(title())
       << "\" path=\"" << path
       << "\">\n    <axis max=\"" << ax->upperEdge()
       << "\" numberOfBins=\"" << ax->bins()
       << "\" min=\"" << ax->lowerEdge()
       << "\" direction=\"x\"";
    if ( vax ) {
      os << ">\n";
      for ( int i = 0, N = ax->bins() - 1; i < N; ++i )
        os << "      <binBorder value=\"" << ax->binUpperEdge(i) << "\"/>\n";
      os << "    </axis>\n";
    } else {
      os << "/>\n";
    }
    os << "    <statistics entries=\"" << entries()
       << "\">\n      <statistic mean=\"" << mean()
       << "\" direction=\"x\"\n        rms=\"" << rms()
       << "\"/>\n    </statistics>\n    <data1d>\n";
    for ( int i = 0; i < ax->bins() + 2; ++i )
      if ( sum[i] && binError(i)>0.) {
        os << "      <bin1d binNum=\"";
        if ( i == 0 ) os << "UNDERFLOW";
        else if ( i == 1 ) os << "OVERFLOW";
        else os << i - 2;
        os << "\" entries=\"" << sum[i]
           << "\" height=\"" << binHeight(i)
           << "\"\n        error=\"" << binError(i)
           << "\" error2=\"" << binError(i)*binError(i)
           << "\"\n        weightedMean=\"" << binMean(i - 2)
           << "\" weightedRms=\"" << binRms(i - 2)
           << "\"/>\n";
      }
    os << "    </data1d>\n  </profile1d>" << std::endl;
    return true;
  }


  /**
   * Write out the histogram in a flat text file suitable for
   * eg. gnuplot to read. The coloums are layed out as 'x w w2 n'.
   */
  bool writeFLAT(std::ostream & os, std::string path, std::string name) {
    os << "# " << path << "/" << name << " " << ax->lowerEdge()
       << " " << ax->bins() << " " << ax->upperEdge()
       << " \"" << title() << " \"" << std::endl;
    for ( int i = 2; i < ax->bins() + 2; ++i )
      if ( sum[i] && binError(i)>0.)
        os << binMean(i - 2) << " "
           << binHeight(i) << " " << binError(i) << " " << sum[i] << std::endl;
    os << std::endl;
    return true;
  }



#ifdef HAVE_ROOT
  /**
   * Write out the histogram in Root file format.
   */
  //bool writeROOT(std::ostream & os, std::string path, std::string name) {
  bool writeROOT(TFile* file, std::string path, std::string name) {

    //std::cout << "Writing out profile histogram " << name.c_str() << " in ROOT file format" << std::endl;

    TProfile* prof1d;
    int nbins;
    if (!vax || vax->isFixedBinning() ) {//equidistant binning (easier case)
      nbins = ax->bins();
      prof1d = new TProfile(name.c_str(), title().c_str(), nbins, ax->lowerEdge(), ax->upperEdge());
    }
    else {
      nbins = vax->bins();
      double* bins = new double[nbins+1];
      for (int i=0; i<nbins; ++i) {
        bins[i] = vax->binEdges(i).first;
      }
      bins[nbins] = vax->binEdges(nbins-1).second; //take last bin right border
      prof1d = new TProfile(name.c_str(), title().c_str(), nbins, bins);
      delete bins;
    }


    double entries = 0;
    for ( int i = 0; i < nbins + 2; ++i ) {
      if ( sum[i] && binError(i)>0.) {
        //i==0: underflow->RootBin(0), i==1: overflow->RootBin(NBins+1)
        entries = entries + sum[i];
        int j=i;
        if (i==0) j=0; //underflow
        else if (i==1) j=nbins+1; //overflow
        if (i>=2) j=i-1; //normal bin entries
        prof1d->SetBinContent(j, binHeight(i));
        prof1d->SetBinError(j, binError(i));
      }
    }

    prof1d->Sumw2();
    prof1d->SetEntries(entries);

    std::string DirName; //remove preceding slash from directory name, else ROOT error
    for (unsigned int i=1; i<path.size(); ++i) DirName += path[i];
    if (!file->Get(DirName.c_str())) file->mkdir(DirName.c_str());
    file->cd(DirName.c_str());
    prof1d->Write();

    delete prof1d;

    return true;
  }

#endif



private:

  /** The title */
  // std::string theTitle;

  /** The axis. */
  IAxis * ax;

  /** Pointer (possibly null) to a axis with fixed bin width. */
  Axis * fax;

  /** Pointer (possibly null) to a axis with fixed bin width. */
  VariAxis * vax;

  /** The counts. */
  std::vector<int> sum;

  /** The weights. */
  std::vector<double> sumw;

  /** The squared weights. */
  std::vector<double> sumw2;

  /** The weighted x-values. */
  std::vector<double> sumxw;

  /** The weighted x-square-values. */
  std::vector<double> sumx2w;

  /** The weighted y-values. */
  std::vector<double> sumyw;

  /** The weighted y-square-values. */
  std::vector<double> sumy2w;

  /** The squared weighted y-square-values. */
  std::vector<double> sumy2w2;

  /** dummy pointer to non-existen annotation. */
  IAnnotation * anno;


};

}

#endif /* LWH_Profile1D_H */

