// -*- C++ -*-
#include "Rivet/Analysis.hh"
#include "Rivet/RivetYODA.hh"
#include "Rivet/Tools/Logging.hh"
#include "Rivet/Projections/ChargedFinalState.hh"

namespace Rivet {


  /// @brief MC validation analysis for Z + jets events
  /// @todo More! This analysis just checks the \f$ \eta \f$ distribution at the moment.
  class MC_TTBAR : public Analysis {
  public:

    /// @name Constructors etc.
    //@{

    /// Constructor
    MC_TTBAR()
      : Analysis("MC_TTBAR")
    {
      //setNeedsCrossSection(false);
    }

    //@}


  public:

    /// @name Analysis methods
    //@{

    /// Book histograms and initialise projections before the run
    void init() {

      const ChargedFinalState cfs(-5.0, 5.0);
      addProjection(cfs, "CFS");

      /// @todo Book histograms here, e.g.:
      _hist_nch_eta = bookHisto1D("nch-eta", 20, -5.0, 5.0);
      _hist_nch_pt  = bookHisto1D("nch-pt", 100, 0.0, 200.0);
      _hist_nch_phi = bookHisto1D("nch-phi", 100, 0.0, TWOPI);

    }


    /// Perform the per-event analysis
    void analyze(const Event& event) {
      const double weight = event.weight();
      const ChargedFinalState& cfs = applyProjection<ChargedFinalState>(event, "CFS");

      foreach (const Particle& p, cfs.particles()) {
        double eta = p.momentum().pseudorapidity();
        double pT = p.momentum().perp();
        double phi = p.momentum().phi();
        _hist_nch_eta->fill(eta, weight);
        _hist_nch_pt->fill(pT, weight);
        _hist_nch_phi->fill(phi, weight);
      }

    }


    /// Normalise histograms etc., after the run
    void finalize() {
      scale(_hist_nch_eta, 1.0/sumOfWeights());
      scale(_hist_nch_pt,  1.0/sumOfWeights());
      scale(_hist_nch_phi, 1.0/sumOfWeights());
    }


  private:

    /// @name Histograms
    //@{
    Histo1DPtr _hist_nch_eta;
    Histo1DPtr _hist_nch_pt;
    Histo1DPtr _hist_nch_phi;
    //@}

  };



  // This global object acts as a hook for the plugin system
  AnalysisBuilder<MC_TTBAR> plugin_MC_TTBAR;


}
