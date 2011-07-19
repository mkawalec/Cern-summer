// -*- C++ -*-
#include "Rivet/Analysis.hh"
#include "Rivet/RivetAIDA.hh"
#include "Rivet/Tools/Logging.hh"
#include "Rivet/Projections/FinalState.hh"
#include "Rivet/Projections/FastJets.hh"

namespace Rivet {


  /// @brief CDF Inclusive jet cross-section differential in \f$ p_\perp \f$
  class CDF_2006_S6450792 : public Analysis {
  public:

    /// Constructor
    CDF_2006_S6450792() : Analysis("CDF_2006_S6450792") {
      setBeams(PROTON, ANTIPROTON);
      setNeedsCrossSection(true);
    }


    /// @name Analysis methods
    //@{

    void init() {
      FinalState fs;
      addProjection(FastJets(fs, FastJets::CDFMIDPOINT, 0.7), "ConeFinder");

      _h_jet_pt = bookHistogram1D(1, 1, 1);
    }


    void analyze(const Event& event) {
      const Jets& jets = applyProjection<JetAlg>(event, "ConeFinder").jets(61.0*GeV);
      foreach (const Jet& jet, jets) {
        double y = fabs(jet.momentum().rapidity());
        if (inRange(y, 0.1, 0.7)) {
          _h_jet_pt->fill(jet.momentum().pT()/GeV, event.weight());
        }
      }
    }


    void finalize() {
      const double delta_y = 1.2;
      scale(_h_jet_pt, crossSection()/nanobarn/sumOfWeights()/delta_y);
    }

    //@}


  private:

    /// @name Histograms
    //@{

    AIDA::IHistogram1D *_h_jet_pt;
    //@}

  };


  // This global object acts as a hook for the plugin system
  AnalysisBuilder<CDF_2006_S6450792> plugin_CDF_2006_S6450792;

}
