// -*- C++ -*-
#include "Rivet/Analysis.hh"
#include "Rivet/RivetAIDA.hh"
#include "Rivet/Tools/Logging.hh"
#include "Rivet/Math/MathUtils.hh"
#include "Rivet/Projections/UnstableFinalState.hh"
#include "LWH/Histogram1D.h"
/// @todo Include more projections as required, e.g. ChargedFinalState, FastJets, ZFinder...

namespace Rivet {


  class CMS_2011_S8978280 : public Analysis {
  public:

    /// @name Constructors etc.
    //@{

    /// Constructor
    CMS_2011_S8978280()
      : Analysis("CMS_2011_S8978280")
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

//	const FinalState fs(-5.0, 5.0);
//	addProjection(fs, "FS");

	const UnstableFinalState ufs(-2.0, 2.0);
	addProjection(ufs, "UFS");

	//7TeV case:
	if(fuzzyEquals(sqrtS(), 7*TeV)){
		//Pt (right) ones:
		_h_kaonPt = bookHistogram1D(2,1,2);
		_h_lambdaPt = bookHistogram1D(4,1,2);
		_h_XiPt = bookHistogram1D(6,1,2);

		//Rapidity (left) ones:
		_h_kaonRap = bookHistogram1D(1,1,2);
		_h_lambdaRap = bookHistogram1D(3,1,2);
		_h_XiRap = bookHistogram1D(5,1,2);

		//Temprorary histos needed to generate the 'division' tables:
		_temp_h_kaon.reset(new LWH::Histogram1D(binEdges(7,1,2)));
		_temp_h_lambda.reset(new LWH::Histogram1D(binEdges(7,1,2)));

		_temp_h_Xi.reset(new LWH::Histogram1D(binEdges(8,1,2)));
		_temp_h_lambda2.reset(new LWH::Histogram1D(binEdges(8,1,2)));

		_temp_h_lambda3.reset(new LWH::Histogram1D(binEdges(9,1,2)));
		_temp_h_kaon2.reset(new LWH::Histogram1D(binEdges(9,1,2)));

		_temp_h_Xi2.reset(new LWH::Histogram1D(binEdges(10,1,2)));
		_temp_h_lambda4.reset(new LWH::Histogram1D(binEdges(10,1,2)));
	}
	//900GeV case:
	else if(fuzzyEquals(sqrtS(), 900*GeV)){
		//Pt (right) ones:
		_h_kaonPt = bookHistogram1D(2,1,1);
		_h_lambdaPt = bookHistogram1D(4,1,1);
		_h_XiPt = bookHistogram1D(6,1,1);

		//Rapidity (left) ones:
		_h_kaonRap = bookHistogram1D(1,1,1);
		_h_lambdaRap = bookHistogram1D(3,1,1);
		_h_XiRap = bookHistogram1D(5,1,1);

		//Temprorary histos needed to generate the 'division' tables:
		_temp_h_kaon.reset(new LWH::Histogram1D(binEdges(7,1,1)));
		_temp_h_lambda.reset(new LWH::Histogram1D(binEdges(7,1,1)));

		_temp_h_Xi.reset(new LWH::Histogram1D(binEdges(8,1,1)));
		_temp_h_lambda2.reset(new LWH::Histogram1D(binEdges(8,1,1)));
		
		_temp_h_lambda3.reset(new LWH::Histogram1D(binEdges(9,1,1)));
		_temp_h_kaon2.reset(new LWH::Histogram1D(binEdges(9,1,1)));

		_temp_h_Xi2.reset(new LWH::Histogram1D(binEdges(10,1,1)));
		_temp_h_lambda4.reset(new LWH::Histogram1D(binEdges(10,1,1)));
	}
    }


    /// Perform the per-event analysis
    void analyze(const Event& event) {
      	const double weight = event.weight();
//	const FinalState cfs = applyProjection<FinalState>(event, "FS");
	const UnstableFinalState cufs = applyProjection<UnstableFinalState>(event, "UFS");


	foreach(const Particle& p, cufs.particles()){
		if(p.pdgId() == K0S){
			_h_kaonPt-> fill(p.momentum().pT(), weight);
			_temp_h_kaon-> fill(p.momentum().pT(), weight);
			_temp_h_kaon2-> fill(p.momentum().pT(), weight);
			_h_kaonRap-> fill(abs(p.momentum().rapidity()), weight);
		}
		else if (p.pdgId() == LAMBDA){
			_h_lambdaPt-> fill(p.momentum().pT(), weight);
			_temp_h_lambda-> fill(p.momentum().pT(), weight);
			_temp_h_lambda2-> fill(p.momentum().pT(), weight);
			_temp_h_lambda3-> fill(p.momentum().pT(), weight);
			_temp_h_lambda4-> fill(p.momentum().pT(), weight);
			_h_lambdaRap-> fill(abs(p.momentum().rapidity()), weight);

		}
		else if (p.pdgId() == XIMINUS){
			_h_XiPt-> fill(p.momentum().pT(), weight);
			_temp_h_Xi-> fill(p.momentum().pT(), weight);
			_temp_h_Xi2-> fill(p.momentum().pT(), weight);
		//	std::cout << abs(p.momentum().rapidity()) << endl;
			_h_XiRap-> fill(abs(p.momentum().rapidity()), weight);
		}
	}	

    }

LICE_2010_S8698546
    /// Normalise histograms etc., after the run
    void finalize() {

      /// @todo Normalise, scale and otherwise manipulate histograms here

      // scale(_h_YYYY, crossSection()/sumOfWeights()); # norm to cross section
     	normalize(_h_kaonPt);
     	normalize(_h_lambdaPt);
	normalize(_h_XiPt);

	normalize(_h_kaonRap);
	normalize(_h_lambdaRap);
	normalize(_h_XiRap);

	//Printing out the graphs that consist of two divided ones.
	//Notice two different cases for different energies:
	if(fuzzyEquals(sqrtS(), 7*TeV)){
		histogramFactory().divide(histoPath("d07-x01-y02"), *_temp_h_lambda, *_temp_h_kaon);
		histogramFactory().divide(histoPath("d08-x01-y02"), *_temp_h_Xi, *_temp_h_lambda2);
		histogramFactory().divide(histoPath("d09-x01-y02"), *_temp_h_lambda3, *_temp_h_kaon2);
		histogramFactory().divide(histoPath("d10-x01-y02"), *_temp_h_Xi2, *_temp_h_lambda4);
	}
	else if(fuzzyEquals(sqrtS(), 900*GeV)){
		histogramFactory().divide(histoPath("d07-x01-y01"), *_temp_h_lambda, *_temp_h_kaon);
		histogramFactory().divide(histoPath("d08-x01-y01"), *_temp_h_Xi, *_temp_h_lambda2);
		histogramFactory().divide(histoPath("d09-x01-y01"), *_temp_h_lambda3, *_temp_h_kaon2);
		histogramFactory().divide(histoPath("d10-x01-y01"), *_temp_h_Xi2, *_temp_h_lambda4);
	}
    }

    //@}


  private:

    // Data members like post-cuts event weight counters go here


  private:

    /// @name Histograms
    //@{

	AIDA::IHistogram1D *_h_kaonPt;
	AIDA::IHistogram1D *_h_lambdaPt;
	AIDA::IHistogram1D *_h_XiPt;

	AIDA::IHistogram1D *_h_kaonRap;
	AIDA::IHistogram1D *_h_lambdaRap;
	AIDA::IHistogram1D *_h_XiRap;

	//Temprorary ones:
	shared_ptr<LWH::Histogram1D> _temp_h_lambda, _temp_h_kaon;
	shared_ptr<LWH::Histogram1D> _temp_h_Xi, _temp_h_lambda2;
	shared_ptr<LWH::Histogram1D> _temp_h_lambda3, _temp_h_kaon2;
	shared_ptr<LWH::Histogram1D> _temp_h_Xi2, _temp_h_lambda4;
    //@}


  };



  // This global object acts as a hook for the plugin system
  AnalysisBuilder<CMS_2011_S8978280> plugin_CMS_2011_S8978280;


}
