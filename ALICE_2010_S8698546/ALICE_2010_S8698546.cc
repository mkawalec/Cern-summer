// -*- C++ -*-
#include "Rivet/Analysis.hh"
#include "Rivet/RivetAIDA.hh"
#include "Rivet/Tools/Logging.hh"
#include "Rivet/Projections/FinalState.hh"
/// @todo Include more projections as required, e.g. ChargedFinalState, FastJets, ZFinder...

namespace Rivet {


  class ALICE_2010_S8698546 : public Analysis {
  public:

    /// @name Constructors etc.
    //@{

    /// Constructor
    ALICE_2010_S8698546()
      : Analysis("ALICE_2010_S8698546")
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

	_h_one = bookProfile1D(1, 1, 1);
    }


    /// Perform the per-event analysis
    void analyze(const Event& event) {
      const double weight = event.weight();
	int protons = 0; int aprotons = 0;
	double protonsPt = 0.0; double aprotonsPt = 0.0;

	const FinalState& cfs = applyProjection<FinalState> (event, "FS");

      /// @todo Do the event by event analysis here
	foreach (const Particle& p, cfs.particles()) {
		if(2212 == p.pdgId()) {
			protons++;
			protonsPt += p.momentum().pT();
		}
		else if(-2212 == p.pdgId()) {
			aprotons++;
			aprotonsPt += p.momentum().pT();
		}
	}
	if(protons && aprotons){
		int ratio = (int)(aprotons/protons);
		double avgPt = ((protonsPt/protons) + (aprotonsPt/aprotons))/2;
//		avgPt /= 1000000000;
	//	_h_one->fill(ratio, avgPt, weight);
		_h_one->fill(avgPt, ratio, weight);
	}
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
    AIDA::IProfile1D *_h_one;
    //@}


  };



  // This global object acts as a hook for the plugin system
  AnalysisBuilder<ALICE_2010_S8698546> plugin_ALICE_2010_S8698546;


}
