// -*- C++ -*-
#include "Rivet/Analysis.hh"
#include "Rivet/RivetYODA.hh"
#include "Rivet/Tools/Logging.hh"
#include "HepMC/HepMCDefs.h"

namespace Rivet {


  /// @brief Analysis for the generated cross section
  class MC_XS : public Analysis {
  public:

    /// @name Constructors etc.
    //@{

    /// Constructor
    MC_XS()
      : Analysis("MC_XS")
    {
      setNeedsCrossSection(true);
    }

    //@}


  public:

    /// @name Analysis methods
    //@{

    /// Book histograms and initialise projections before the run
    void init() {
      _h_XS = bookScatter2D("XS", 1, 0.0, 1.0);
      _mc_xs=_mc_error=0.;
    }


    /// Perform the per-event analysis
    void analyze(const Event& event) {
#ifdef HEPMC_HAS_CROSS_SECTION
      _mc_xs    = event.genEvent().cross_section()->cross_section();
      _mc_error = event.genEvent().cross_section()->cross_section_error();
#endif
    }


    /// Normalise histograms etc., after the run
    void finalize() {
#ifndef HEPMC_HAS_CROSS_SECTION
      _mc_xs=crossSection();
      _mc_error=0.0;
#endif
      _h_XS->addPoint(0,_mc_xs,
		      0,_mc_error);
    }

    //@}


  private:

    /// @name Histograms
    //@{
    Scatter2DPtr  _h_XS;
    double _mc_xs, _mc_error;
    //@}


  };



  // This global object acts as a hook for the plugin system
  AnalysisBuilder<MC_XS> plugin_MC_XS;


}
