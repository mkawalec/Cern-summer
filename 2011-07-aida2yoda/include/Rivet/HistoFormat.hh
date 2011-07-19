// -*- C++ -*-
#ifndef RIVET_HistoFormat_HH
#define RIVET_HistoFormat_HH

#include "Rivet/Rivet.hh"

namespace Rivet {


  /// Enumeration of available histogram output formats.
  enum HistoFormat { AIDAML, FLAT, ROOT };

  /// Typedef for a map of histogram format enums to strings.
  typedef std::map<HistoFormat, std::string> HistoFormatMap;


  /// Typedef for a map of histogram format name strings to enums.
  typedef std::map<std::string, HistoFormat> HistoFormatMapR;


  /// Function which returns a map from histogram format enums to the corresponding name strings.
  inline HistoFormatMap getKnownHistoFormats() {
    HistoFormatMap hfmap;
    hfmap[AIDAML] = "AIDA";
    hfmap[FLAT] = "FLAT";
#ifdef HAVE_ROOT
    hfmap[ROOT] = "ROOT";
#endif
    return hfmap;
  }

  /// Function which returns a map from histogram format name strings to the corresponding enums.
  inline HistoFormatMapR getKnownHistoFormatsR() {
    HistoFormatMap hfmap = getKnownHistoFormats();
    HistoFormatMapR hfmapr;
    for (HistoFormatMap::const_iterator hf = hfmap.begin(); hf != hfmap.end(); ++hf) {
      hfmapr[hf->second] = hf->first;
    }
    return hfmapr;
  }


  /// Typedef for a collection of histogram format name enums.
  typedef std::vector<HistoFormat> HistoFormatList;


  /// Function which returns a vector of all the histogram format
  /// values in the HistoFormat enum.
  inline HistoFormatList getKnownHistoFormatEnums() {
    HistoFormatList names;
    HistoFormatMap hfmap = getKnownHistoFormats();
    for (HistoFormatMap::const_iterator hf = hfmap.begin(); hf != hfmap.end(); ++hf) {
      names.push_back(hf->first);
    }
    return names;
  }


  /// Function which returns a vector of all the histogram format name strings.
  inline std::vector<std::string> getKnownHistoFormatNames() {
    vector<string> names;
    HistoFormatMap hfmap = getKnownHistoFormats();
    for (HistoFormatMap::const_iterator hf = hfmap.begin(); hf != hfmap.end(); ++hf) {
      names.push_back(hf->second);
    }
    return names;
  }


}

#endif
