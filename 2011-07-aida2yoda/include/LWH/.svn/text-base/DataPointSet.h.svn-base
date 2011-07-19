// -*- C++ -*-
#ifndef LWH_DataPointSet_H
#define LWH_DataPointSet_H
//
// This is the declaration of the DataPointSet class representing
//


#include <vector>
#include <limits>
#include <cmath>
#include <algorithm>
#include "AIDataPointSet.h"
#include "ManagedObject.h"
#include "DataPoint.h"

#ifdef HAVE_ROOT
  #include "TGraphAsymmErrors.h"
#endif

namespace LWH {

using namespace AIDA;

using namespace std;

/**
 * An DataPointSet represents a binned histogram axis. A 1D Histogram would have
 * one DataPointSet representing the X axis, while a 2D Histogram would have two
 * axes representing the X and Y DataPointSet.
 */
  class DataPointSet: public IDataPointSet, public ManagedObject {

public:

  /**
   * Standard constructor takes the dimension, \a D, of the data
   * points as argument.
   */
  DataPointSet(int D): dim(D) {}

  /**
   * Destructor.
   */
  virtual ~DataPointSet() {}

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
   * Get the data set's title.
   * @return The data set's title.
   */
  // std::string title() const {
  //   return theTitle;
  // }

  /**
   * Get the data set's title.
   * @return The data set's title.
   */
  std::string name() const {
    return theTitle;
  }

  /**
   * Set the data set's title.
   * @param title The title.
   * @return false If title cannot be changed.
   */
  // bool setTitle(const std::string & title) {
  //   theTitle = title;
  //   return true;
  // }

  /**
   * Get the dimension of the IDataPoints that can be stored in the set.
   * @return The dimension of the IDataPoints storable in the set.
   *
   */
  int dimension() const {
    return dim;
  }

  /**
   * Remove all the IDataPoints in the set.
   * After this the IDataPointSet is as just created.
   */
  void clear() {
    dset.clear();
  }

  /**
   * Get the current size of the IDataPointSet, i.e. the number
   * of IDataPoints contained in the set.
   * @return The size of the IDataPointSet.
   */
  int size() const {
    return dset.size();
  }

  /**
   * Get the IDataPoint at a give index in the set.
   * @param index The IDataPoint index.
   * @return      The corresponding IDataPoint.
   */
  IDataPoint * point(int index) {
    return &(dset[index]);
  }

  /**
   * Set the values and errors of a given coordinate all at once.  If
   * this method is called on an empty IDataPointSet, a number of
   * points equal to the size of the arrays provided is created; if
   * the IDataPointSet is not empty the dimension of the array must
   * match with the size of the IDataPointSet.
   * @param coord The coordinate's index
   * @param val   The array of the values for the given coordinate
   * @param err   The array with the symmetric errors.
   * @return false if an illegal coordinate is provided or if there is
   *      a mismatch between the size of the array and the size of the
   *      IDataPointSet.
   */
  bool setCoordinate(int coord,
		     const std::vector<double>  & val,
		     const std::vector<double>  & err) {
    return setCoordinate(coord, val, err, err);
  }

  /**
   * Set the values and errors of a given coordinate all at once.  If
   * this method is called on an empty IDataPointSet, a number of
   * points equal to the size of the arrays provided is created; if
   * the IDataPointSet is not empty the dimension of the array must
   * match with the size of the IDataPointSet.
   * @param coord The coordinate's index
   * @param val   The array of the values for the given coordinate
   * @param errp  The array with the plus errors.
   * @param errm  The array with the minus errors.
   * @return false if an illegal coordinate is provided or if there is
   *     a mismatch between the size of the array and the size of the
   *     IDataPointSet.
   *
   */
  bool setCoordinate(int coord,
		     const std::vector<double>  & val,
		     const std::vector<double>  & errp,
		     const std::vector<double>  & errm) {
    if ( coord < 0 || coord >= dimension() ) return false;
    if ( dset.empty() ) dset.resize(val.size(), DataPoint(dimension()));
    if ( val.size() != dset.size() || errp.size() != dset.size() ||
	 errm.size() != dset.size() ) return false;
    for ( int i = 0, N = val.size(); i < N; ++i ) {
      dset[i].coordinate(coord)->setValue(val[i]);
      dset[i].coordinate(coord)->setErrorPlus(errp[i]);
      dset[i].coordinate(coord)->setErrorMinus(errm[i]);
    }
    return true;
  }

  /**
   * Return the data point at the given index.
   * @return 0 if index is out of range.
   */
  const IDataPoint * point(int index) const {
    if ( index < 0 || unsigned(index) >= dset.size() ) return 0;
    return &(dset[index]);
  }

  /**
   * Add a new empty IDataPoint at the end of the set.
   * @return The newly added point.
   */
  IDataPoint * addPoint() {
    dset.push_back(DataPoint(dimension()));
    return &(dset.back());
  }

  /**
   * Add a copy of an IDataPoint at the end of the set.
   * @param point The IDataPoint to be added.
   * @return false If the point has the wrong dimension or
   *                                       if the point cannot be added.
   */
  bool addPoint(const IDataPoint & point) {
    if ( dimension() && dimension() != point.dimension() ) return false;
    dset.push_back(DataPoint(point));
    return true;
  }

  /**
   * Remove the IDataPoint at a given index.
   * @param index The index of the IDataPoint to be removed.
   * @return false If the index is < 0 or >= size().
   */
  bool removePoint(int index) {
    if ( index < 0 || unsigned(index) >= dset.size() ) return false;
    dset.erase(dset.begin() + index);
    return true;
  }

  /**
   * Get the lower value for a give axis.
   * @param coord The coordinate of the axis.
   * @return      The lower edge of the corresponding axis.
   *              If coord < 0 or coord >= dimension(), or if the
   *              set is empty NaN is returned.
   */
  double lowerExtent(int coord) const {
    if ( dset.empty() ) return std::numeric_limits<double>::quiet_NaN();
    if ( coord < 0 || coord >= dimension() )
      return std::numeric_limits<double>::quiet_NaN();
    double low = dset[0].coordinate(coord)->value();
    for ( int i = 1, N = dset.size(); i < N; ++i )
      low = std::min(low, dset[i].coordinate(coord)->value());
    return low;
  }

  /**
   * Get the upper value for a give axis.
   * @param coord The coordinate of the axis.
   * @return      The upper edge of the corresponding axis.
   *              If coord < 0 or coord >= dimension(), or if the set
   *              is empty NaN is returned.
   */
  double upperExtent(int coord) const {
    if ( dset.empty() ) return std::numeric_limits<double>::quiet_NaN();
    if ( coord < 0 || coord >= dimension() )
      return std::numeric_limits<double>::quiet_NaN();
    double upp = dset[0].coordinate(coord)->value();
    for ( int i = 1, N = dset.size(); i < N; ++i )
      upp = std::max(upp, dset[i].coordinate(coord)->value());
    return upp;
  }

  /**
   * Scales the values and the errors of all the measurements
   * of each point by a given factor.
   * @param scale The scale factor.
   * @return false If an illegal scaleFactor is provided.
   */
  bool scale(double scale) {
    for ( int i = 0, N = dset.size(); i < N; ++i )
      for ( int j = 0, M = dset[i].dimension(); j < M; ++j ) {
	IMeasurement * m = dset[i].coordinate(j);
	m->setValue(m->value()*scale);
	m->setErrorPlus(m->errorPlus()*scale);
	m->setErrorMinus(m->errorPlus()*scale);
      }
    return true;
  }

  /**
   * Scales the values and the errors of the measurements in a given
   * coordinate of each point by a given factor.
   * @param scale The scale factor.
   * @param coord The coordinate
   * @return false If an illegal scaleFactor is provided.
   */
  bool scale(double scale, int coord) {
    for ( int i = 0, N = dset.size(); i < N; ++i ) {
      if ( coord >= dset[i].dimension() ) {
        throw std::runtime_error("Trying to scale non-existent dimension.");
      }
      IMeasurement * m = dset[i].coordinate(coord);
      m->setValue(m->value()*scale);
      m->setErrorPlus(m->errorPlus()*scale);
      m->setErrorMinus(m->errorPlus()*scale);
    }
    return true;
  }
	
  /**
   * Scales the values of all the measurements
   * of each point by a given factor.
   * @param scale The scale factor.
   * @return false If an illegal scaleFactor is provided.
   */
  bool scaleValues(double scale) {
    for ( int i = 0, N = dset.size(); i < N; ++i )
      for ( int j = 0, M = dset[i].dimension(); j < M; ++j ) {
	IMeasurement * m = dset[i].coordinate(j);
	m->setValue(m->value()*scale);
      }
    return true;
  }

  /**
   * Scales the errors of all the measurements
   * of each point by a given factor.
   * @param scale The scale factor.
   * @return false If an illegal scaleFactor is provided.
   */
  bool scaleErrors(double scale) {
    for ( int i = 0, N = dset.size(); i < N; ++i )
      for ( int j = 0, M = dset[i].dimension(); j < M; ++j ) {
	IMeasurement * m = dset[i].coordinate(j);
	m->setErrorPlus(m->errorPlus()*scale);
	m->setErrorMinus(m->errorPlus()*scale);
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
   * Write out the data set in the AIDA XML format.
   */
  bool writeXML(std::ostream & os, std::string path, std::string name) {
    //std::cout << "Writing out data point set " << name << " in AIDA file format!" << std::endl;
    os << scientific << setprecision(8);
    os << "  <dataPointSet name=\"" << encodeForXML(name)
       << "\"\n    title=\"" << encodeForXML(title())
       << "\" path=\"" << path
       << "\" dimension=\"" << dimension() << "\">\n";
    for ( int d = 0; d < dimension(); ++d )
      os << "    <dimension dim=\"" << d << "\" title=\""
	 << encodeForXML(title(d)) << "\" />\n";
    for ( int i = 0, N = size(); i < N; ++i ) {
      os << "    <dataPoint>\n";
      for ( int j = 0, M = dimension(); j < M; ++j )
	os << "      <measurement value=\""
	   << point(i)->coordinate(j)->value()
	   << "\" errorPlus=\""
	   << point(i)->coordinate(j)->errorPlus()
	   << "\" errorMinus=\""
	   << point(i)->coordinate(j)->errorMinus()
	   << "\"/>\n";
      os << "    </dataPoint>\n";
    }
    os << "  </dataPointSet>" << std::endl;
    return true;
  }

  /**
   * Write out the data set in a flat text file suitable for
   * eg. gnuplot to read. The coloums are layed out as 'x1 x2 ... xn
   * dx1+ dx2+ ... dxn+ dx1- dx2- ... dxn-'.
   */
  bool writeFLAT(std::ostream & os, std::string path, std::string name) {
    os << "# " << path << "/" << name << " " << size()
       << " \"" << title() << " \" dimension " << dimension() << std::endl;
    for ( int i = 0, N = size(); i < N; ++i ) {
      for ( int j = 0, M = dimension(); j < M; ++j )
	os << point(i)->coordinate(j)->value() << " ";
      for ( int j = 0, M = dimension(); j < M; ++j )
	os << point(i)->coordinate(j)->errorPlus() << " ";
      for ( int j = 0, M = dimension(); j < M; ++j )
	os << point(i)->coordinate(j)->errorMinus() << " ";
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

    if (dimension()!=2) {
      cerr << "DataPointSet.h: writeROOT: dimension != 2, can't write TGraph, "
           << "choose different file format!" << endl;
      return false;
    }
    
    //Replace "-" by "_" because cint interprets - as a minus.
    
    for(std::string::iterator c = name.begin();
        c != name.end(); ++c){
      if(*c == *"-"){
        std::string::iterator cEnd=c;
        ++cEnd;
        name.replace(c, cEnd, "_");
      }
    }
    
    //cout << "Writing out TGraph " << name.c_str() << " in ROOT file format" << endl;
      
    int N = size();
    
    vector<double> x, y, exl, exh, eyl, eyh;

    for ( int i = 0; i < N; ++i ) {
      x.push_back(point(i)->coordinate(0)->value());
      exl.push_back(point(i)->coordinate(0)->errorMinus());
      exh.push_back(point(i)->coordinate(0)->errorPlus());
      y.push_back(point(i)->coordinate(1)->value());
      eyl.push_back(point(i)->coordinate(1)->errorMinus());
      eyh.push_back(point(i)->coordinate(1)->errorPlus());
    }
        
    TGraphAsymmErrors* graph = new TGraphAsymmErrors(N, &(x[0]), &(y[0]),
                                                     &(exl[0]), &(exh[0]),
                                                     &(eyl[0]), &(eyh[0]) );
        
    graph->SetTitle(title().c_str());
    graph->SetName(name.c_str());
        
    std::string DirName; //remove preceding slash from directory name, else ROOT error
    for (unsigned int i=1; i<path.size(); ++i) DirName += path[i];
    if (!file->Get(DirName.c_str())) file->mkdir(DirName.c_str());
    file->cd(DirName.c_str());
        
    graph->Write();
    delete graph;
    
    return true;
  }

 #endif




private:

  /** The title */
  // std::string theTitle;

  /**
   * The included data points.
   */
  std::vector<DataPoint> dset;

  /**
   * The dimension of the points in this set.
   */
  unsigned int dim;

  /** dummy pointer to non-existen annotation. */
  IAnnotation * anno;

};

}

#endif /* LWH_DataPointSet_H */
