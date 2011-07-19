// -*- C++ -*-
#include "Rivet/Analysis.hh"
#include "Rivet/RivetAIDA.hh"
#include "Rivet/Tools/Logging.hh"
#include "Rivet/Projections/FinalState.hh"
#include "Rivet/Projections/ZFinder.hh"


namespace Rivet {


  /// @brief Measurement of Z(->muon muon) pT differential cross-section
  /// @author Flavia Dias
  class D0_2010_S8671338 : public Analysis {
  public:

    /// @name Construction
    //@{

    /// Constructor
    D0_2010_S8671338() : Analysis("D0_2010_S8671338")
    {
      setBeams(PROTON, ANTIPROTON);
      setNeedsCrossSection(true);
    }

    //@}


    ///@name Analysis methods
    //@{

    /// Add projections and book histograms
    void init() {
      ZFinder zfinder(-1.7, 1.7, 15.0*GeV, MUON, 65.0*GeV, 115.0*GeV, 0.2, false, true);
      addProjection(zfinder, "ZFinder");

      _h_Z_pT_normalised = bookHistogram1D(1, 1, 1);
      _h_Z_pT_xs = bookHistogram1D(2, 1, 1);
    }


    // Do the analysis
    void analyze(const Event& e) {
      const double weight = e.weight();
      const ZFinder& zfinder = applyProjection<ZFinder>(e, "ZFinder");
      if (zfinder.particles().size()==1) {
        double ZpT = zfinder.particles()[0].momentum().pT()/GeV;
        _h_Z_pT_normalised->fill(ZpT, weight);
        _h_Z_pT_xs->fill(ZpT, weight);
      }
    }


    /// Finalize
    void finalize() {
      normalize(_h_Z_pT_normalised, 1.0);
      scale(_h_Z_pT_xs, crossSectionPerEvent());
    }

    //@}


  private:

    /// @name Histogram
    AIDA::IHistogram1D * _h_Z_pT_normalised;
    AIDA::IHistogram1D * _h_Z_pT_xs;

  };


  // This global object acts as a hook for the plugin system
  AnalysisBuilder<D0_2010_S8671338> plugin_D0_2010_S8671338;


}
