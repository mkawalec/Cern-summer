// -*- C++ -*-
#include "Rivet/Analysis.hh"
#include "Rivet/RivetAIDA.hh"
#include "Rivet/Tools/Logging.hh"
#include "Rivet/Projections/FinalState.hh"
#include <cstdlib>
/// @todo Include more projections as required, e.g. ChargedFinalState, FastJets, ZFinder...

namespace Rivet {


  class MY_TEST : public Analysis {
  public:

    /// @name Constructors etc.
    //@{

    /// Constructor
    MY_TEST()
      : Analysis("MY_TEST")
    {
      /// @todo Set whether your finalize method needs the generator cross section
      setNeedsCrossSection(true);
    }

    //@}


  public:

    /// @name Analysis methods
    //@{

    /// Book histograms and initialise projections before the run
    void init() {

      /// @todo Initialise and register projections here

      /// @todo Book histograms here, e.g.:
      // _h_XXXX = bookProfile1D(1, 1, 1);
      // _h_YYYY = bookHistogram1D(2, 1, 1);
   	const FinalState fs(-5.0, 5.0);
    	addProjection(fs, "FS");
	
	_h_one = bookHistogram1D("flatOne", 50, 0, 100);
    }


    /// Perform the per-event analysis
    void analyze(const Event& event) {
      const double weight = event.weight();

      /// @todo Do the event by event analysis here

      _h_one->fill(rand()%100,1);

    }


    /// Normalise histograms etc., after the run
    void finalize() {

      /// @todo Normalise, scale and otherwise manipulate histograms here

      // scale(_h_YYYY, crossSection()/sumOfWeights()); # norm to cross section
      // normalize(_h_YYYY); # normalize to unity

    }

    //@}


  private:

    // Data members like post-cuts event weight counters go here


  private:

    /// @name Histograms
    //@{

    AIDA::IProfile1D *_h_XXXX;
    AIDA::IHistogram1D *_h_YYYY;
    AIDA::IHistogram1D *_h_one;
    //@}


  };



  // This global object acts as a hook for the plugin system
  AnalysisBuilder<MY_TEST> plugin_MY_TEST;


}
