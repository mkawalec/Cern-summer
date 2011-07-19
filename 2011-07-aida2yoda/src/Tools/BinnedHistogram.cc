// -*- C++ -*-
#include "Rivet/Tools/BinnedHistogram.hh"
#include "Rivet/RivetBoost.hh"
#include "Rivet/RivetAIDA.hh"
#include "Rivet/Analysis.hh"

namespace Rivet {


  template<typename T>
  const BinnedHistogram<T>& BinnedHistogram<T>::addHistogram(const T& binMin, 
                                                             const T& binMax, 
                                                             AIDA::IHistogram1D *histo){
    if (binMin > binMax) {
      throw Error
        ("Cannot add a binned histogram where the lower bin edge is above the upper edge");
    } 
    _histosByUpperBound[binMax] = histo;
    _histosByLowerBound[binMin] = histo;
    bool found = false;
    foreach (AIDA::IHistogram1D* hist, _histos) {
      if (hist == histo) {
        found = true;
        break;
      }
    }
    
    if (!found){
      _histos.push_back(histo);
      _binWidths[histo]=binMax-binMin;
    }
    
    return *this;
  }



  template<typename T>
  AIDA::IHistogram1D* BinnedHistogram<T>::fill(const T& bin,
                                                     const T& val,
                                                     double weight) {

    typename map<T, AIDA::IHistogram1D*>::iterator histIt =
      _histosByUpperBound.upper_bound(bin);
    //check that the bin is not out of range
    if (histIt == _histosByUpperBound.end()) {
      return 0;
    }
 
    AIDA::IHistogram1D* histo = histIt->second;
    histIt = _histosByLowerBound.lower_bound(bin);

    // No need to check going beyond the upper bound if we already passed above
    // (given that upper bound > lower bound is checked)
    // Check it is not before the start of the map
    if (histIt == _histosByLowerBound.begin()) {
      return 0;
    }
    // By-lower-bound actually gives us the iterator one above the nearest element,
    // so decrement it. This is safe because we already checked we're not at the start!
    --histIt;
 
    if (histo != histIt->second) {
      return 0;
    }
    
    histo->fill(val, weight);
    
    return histo;
  }
  
  
  template<typename T>
  void BinnedHistogram<T>::scale(const T& scale, Analysis* ana) {
    foreach (AIDA::IHistogram1D* hist, getHistograms()) {
      ana->scale(hist, scale/_binWidths[hist]);
    }
  }



  // Template declarations for the compiler.
  template class BinnedHistogram<double>;
  template class BinnedHistogram<int>;
  template class BinnedHistogram<float>;


}
