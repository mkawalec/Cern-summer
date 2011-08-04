// -*- C++ -*-
//
// This file is part of YODA -- Yet more Objects for Data Analysis
// Copyright (C) 2008-2011 The YODA collaboration (see AUTHORS for details)
//
#ifndef YODA_Histo2D_h
#define YODA_Histo2D_h

#include "YODA/AnalysisObject.h"
#include "YODA/HistoBin2D.h"
#include "YODA/Scatter3D.h"
#include "YODA/Axis2D.h"
#include "YODA/Exceptions.h"
#include "YODA/Histo1D.h"
#include <vector>
#include <string>
#include <map>

namespace YODA {


  /// Convenience typedef
  typedef Axis2D<HistoBin2D> Histo2DAxis;


  /// A  one-dimensional histogram.
  class Histo2D : public AnalysisObject {

  public:

    /// Convenience typedefs
    typedef Histo2DAxis Axis;
    typedef Axis::Bins Bins;


    /// @name Constructors
    //@{

    /// Constructor giving range and number of bins.
    /// @todo Remove binning enum stuff
    Histo2D(size_t nbinsX, double lowerX, double upperX,
            size_t nbinsY, double lowerY, double upperY,
            const std::string& path="", const std::string& title="")
      : AnalysisObject("Histo2D", path, title),
        _axis(nbinsX, lowerX, upperX,
              nbinsY, lowerY, upperY)
    { }
    /* A default constructor. One needs to provide two points 
     * (top-right and bottom-left) for each rectangular bin that 
     * is created. It is assumed that the binedges vector is nonempty (why btw?).
     */
    Histo2D(const std::vector<std::pair<std::pair<double,double>, pair<double,double> > >& binedges, 
            const std::string& path="", 
            const std::string& title="") 
      : AnalysisObject("Histo2D", path, title),
      _axis(binedges)
    { }

    /// Copy constructor with optional new path
    Histo2D(const Histo2D& h, const std::string& path="");

    /// Constructor from a Scatter3D's binning, with optional new path
    Histo2D(const Scatter3D& s, const std::string& path="");


    //@}


  public:

    /// @name Persistency hooks
    //@{

    /// Get name of the analysis object type, for persisting
    std::string _aotype() const { return "Histo2D"; }

    /// Set the state of the histo object, for unpersisting
    /// @todo Need to set annotations (do that on AO), all-histo Dbns, and dbns for every bin. Delegate!
    // void _setstate() = 0;

    //@}


    /// @name Modifiers
    //@{

    /// Fill histo by value and weight
    int fill(double x, double y, double weight=1.0);

    /// @brief Reset the histogram.
    /// Keep the binning but set all bin contents and related quantities to zero
    virtual void reset() {
      _axis.reset();
    }

    ///Check if is a grid:
    int isGriddy() {
        return _axis.isGriddy();
    }
    
    /// Rescale as if all fill weights had been different by factor @a scalefactor.
    void scaleW(double scalefactor) {
      _axis.scaleW(scalefactor);
    }
    
    /// Scale the dimensions
    void scale(double scaleX = 1.0, double scaleY = 1.0) {
      _axis.scale(scaleX, scaleY);
    }

    
    //Adding bins
    void addBin(const vector<pair<pair<double,double>, pair<double,double> > > coords) {
        _axis.addBin(coords);
    }

    /// Adding bins which is not so eloquent
    void addBin(double lowX, double lowY, double highX, double highY)   {
        _axis.addBin(lowX, lowY, highX, highY);
    }

    //@}
  public:

    /// @name Bin accessors
    //@{

    /// Low edges of this histo's axis
    double lowEdgeX() const {
      return _axis.lowEdgeX();
    }

    double lowEdgeY() const {
        return _axis.lowEdgeY();
    }

    /// High edges of this histo's axis
    double highEdgeX() const {
      return _axis.highEdgeX();
    }

    double highEdgeY() const {
        return _axis.highEdgeY();
    }

    /// Access the bin vector
    /// @todo Actually, it's a Histo
    std::vector<YODA::HistoBin2D>& bins() {
      return _axis.bins();
    }

    /// Access the bin vector (const version)
    const std::vector<YODA::HistoBin2D>& bins() const {
      return _axis.bins();
    }

    /// Access a bin by index (non-const version)
    HistoBin2D& bin(size_t index) {
      return _axis.bins()[index];
    }

    /// Access a bin by index (const version)
    const HistoBin2D& bin(size_t index) const {
      return _axis.bins()[index];
    }

    /// Access a bin by coordinate (non-const version)
    HistoBin2D& binByCoord(double x, double y) {
      return _axis.binByCoord(x, y);
    }

    /// Access a bin by coordinate (const version)
    const HistoBin2D& binByCoord(double x, double y) const {
      return _axis.binByCoord(x, y);
    }

    /// Return bin index (non-const version)
    int findBinIndex(double coordX, double coordY) {
      return _axis.findBinIndex(coordX, coordY);
    }

    /// Return bin index (const version)
    const int findBinIndex(double coordX, double coordY) const {
      return _axis.findBinIndex(coordX, coordY);
    }

    /// Underflow (const version)
    const Dbn2D& underflow() const {
        return _axis.underflow();
    }
    
    /// Return underflow (non-const version)
    Dbn2D& underflow() {
        return _axis.underflow();
    }

    /// Return overflow (const version)
    const Dbn2D& overflow() const {
        return _axis.overflow();
    }

    /// Return overflow (non-const version)
    Dbn2D& overflow() {
        return _axis.overflow();
    }
   
    /// Return a total number of bins in Histo(non-const version)
    unsigned int numBinsTotal() {
        return _axis.numBinsTotal();
    }

    const unsigned int numBinsTotal() const {
        return _axis.numBinsTotal();
    }

    /// Hash returner (non-const version)
    std::pair<Utils::cachedvector<pair<double,std::vector<pair<size_t, pair<double,double> > > > >,
              Utils::cachedvector<pair<double,std::vector<pair<size_t, pair<double,double> > > > > > getHash() {
        return _axis.getHash();
    }
    
    /// Hash returner (const version)
    const std::pair<Utils::cachedvector<pair<double,std::vector<pair<size_t, pair<double,double> > > > >,
                    Utils::cachedvector<pair<double,std::vector<pair<size_t, pair<double,double> > > > > > getHash() const {
        return _axis.getHash();
    }
    //@}
  public:

    /// @name Whole histo data
    //@{

    /// Get the total volume of the histogram
    //TODO: This does not work!!
    double integral(bool includeoverflows=true) const {
      return sumW(includeoverflows);
    }

    /// Get sum of weights in histo
    double sumW(bool includeoverflows=true) const;

    /// Get sum of squared weights in histo
    double sumW2(bool includeoverflows=true) const;

    /// Get the mean
    double xMean(bool includeoverflows=true) const;
    double yMean(bool includeoverflows=true) const;

    /// Get the variance
    double xVariance(bool includeoverflows=true) const;
    double yVariance(bool includeoverflows=true) const;

    /// Get the standard deviation
    double xStdDev(bool includeoverflows=true) const {
      return std::sqrt(xVariance(includeoverflows));
    }
    double yStdDev(bool includeoverflows=true) const {
      return std::sqrt(yVariance(includeoverflows));
    }

    //@}


  public:

    /// @name Adding and subtracting histograms
    //@{

    /// Add another histogram to this one
    Histo2D& operator += (const Histo2D& toAdd) {
      _axis += toAdd._axis;
      return *this;
    }
    
    /// Subtract another histogram from this one
    Histo2D& operator -= (const Histo2D& toSubtract) {
      _axis -= toSubtract._axis;
      return *this;
    }

    //@}

    ///Creates a Histo1D from Histo2D 
    /** This function cuts Histo2D parallely to the X axis 
      * at the specified Y coordinate:
      */
    Histo1D cutterX(double atY) {
        if(isGriddy() != 0) throw GridError("This is not a gird!");
        if(atY < lowEdgeY() || atY > highEdgeY()) throw RangeError("Y is outside the grid");
        HistoBin2D first = binByCoord(lowEdgeX(), atY);
        vector<HistoBin1D> temp;
        temp.push_back(first.transformX());

        for(double i = first.xMax() + first.widthX()/2; i < highEdgeX(); i+=first.widthX()){
            temp.push_back(binByCoord(i,atY).transformX());
        }

        Histo1D ret(temp);
        return ret;
    }
    
    Histo1D cutterY(double atX) {
        if(isGriddy() != 0) throw GridError("This is not a gird!");
        if(atX < lowEdgeX() || atX > highEdgeX()) throw RangeError("X is outside the grid");
        HistoBin2D first = binByCoord(lowEdgeX(), atX);
        vector<HistoBin1D> temp;
        temp.push_back(first.transformY());

        for(double i = first.yMax() + first.widthY()/2; i < highEdgeY(); i+=first.widthY()){
            temp.push_back(binByCoord(atX,i).transformY());
        }

        Histo1D ret(temp);
        return ret;
    }

  private:

    /// @name Bin data
    //@{

    /// Definition of bin edges and contents
    Axis2D<HistoBin2D> _axis;

    //@}

  };


  /// @name Combining histos: global operators
  //@{

  /// Add two histograms
  inline Histo2D operator + (const Histo2D& first, const Histo2D& second) {
    Histo2D tmp = first;
    tmp += second;
    return tmp;
  }

  /// Subtract two histograms
  inline Histo2D operator - (const Histo2D& first, const Histo2D& second) {
    Histo2D tmp = first;
    tmp -= second;
    return tmp;
  }

  //Scatter3D operator / (const Histo2D& numer, const Histo2D& denom);

  //@}


}

#endif
