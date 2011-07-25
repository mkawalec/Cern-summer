#ifndef RIVET_RIVETYODA_HH
#define RIVET_RIVETYODA_HH

/// @author Andy Buckley
/// @date   2009-01-30
/// @author David Grellscheid
/// @date   2011-07-18

// Include files
#include "Rivet/Rivet.hh"
#include "Rivet/RivetYODA.fhh"
#include "YODA/AnalysisObject.h"
#include "YODA/WriterYODA.h"
#include "YODA/Histo1D.h"
#include "YODA/Profile1D.h"
#include "YODA/Scatter2D.h"
#include "YODA/Point2D.h"
#include "YODA/ReaderAIDA.h"

// Yoda ones:
#include "YODA/AnalysisObject.h"
#include "YODA/Axis1D.h"
#include "YODA/Bin1D.h"
#include "YODA/Bin.h"
#include "YODA/Dbn1D.h"
#include "YODA/Exceptions.h"
#include "YODA/Histo1D.h"
#include "YODA/HistoBin1D.h"
#include "YODA/Point2D.h"
#include "YODA/Profile1D.h"
#include "YODA/ProfileBin1D.h"
#include "YODA/ReaderAIDA.h"
#include "YODA/Reader.h"
#include "YODA/ReaderYODA.h"
#include "YODA/Scatter2D.h"
#include "YODA/WriterAIDA.h"
#include "YODA/Writer.h"
#include "YODA/WriterYODA.h"

//And second dimension goes here:
#include "YODA/Axis2D.h"
#include "YODA/Bin2D.h"
#include "YODA/Dbn2D.h"
#include "YODA/Histo2D.h"
#include "YODA/HistoBin2D.h"
#include "YODA/Point3D.h"
#include "YODA/Scatter3D.h"


namespace Rivet {

  /// Function to get a map of all the bin edge vectors in a paper with the
  /// given @a papername.
  map<string, BinEdges> getBinEdges(string papername);

  map<string, BinEdges> getBinEdges(const map<string, vector<DPSXPoint> >& xpoints);

  map<string, vector<DPSXPoint> > getDPSXValsErrs(string papername);

  map<string, vector<DPSXYPoint> > getDPSXYValsErrs(string papername);

  /// Get the file system path to the AIDA reference file for this paper.
  string getDatafilePath(string papername);

  /// Return the integral over the histogram bins
  inline double integral(Histo1DPtr histo) {
    double intg = 0.0;
    for ( size_t i = 0; i < histo->numBins(); ++i ) {
      intg += histo->bin(i).area();
    }
    return intg;
  }

  using YODA::WriterYODA;
  using YODA::ReaderAIDA;
  using YODA::Histo1D;
  using YODA::Profile1D;
  using YODA::Scatter2D;
  using YODA::Point2D;
}

#endif
