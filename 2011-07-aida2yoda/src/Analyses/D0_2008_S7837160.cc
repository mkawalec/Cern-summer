// -*- C++ -*-
#include "Rivet/Analysis.hh"
#include "Rivet/Tools/Logging.hh"
#include "Rivet/Tools/ParticleIdUtils.hh"
#include "Rivet/Projections/FinalState.hh"
#include "Rivet/Projections/WFinder.hh"
#include "Rivet/Projections/LeadingParticlesFinalState.hh"
#include "Rivet/Projections/IdentifiedFinalState.hh"
#include "Rivet/RivetYODA.hh"

namespace Rivet {


  /// @brief D0 Run II measurement of W charge asymmetry
  /// @author Andy Buckley
  /// @author Gavin Hesketh
  class D0_2008_S7837160 : public Analysis {

  public:

    /// Default constructor.
    D0_2008_S7837160()
      : Analysis("D0_2008_S7837160")
    {
      // Run II W charge asymmetry
      setBeams(PROTON, ANTIPROTON);
    }


    /// @name Analysis methods
    //@{

    // Book histograms and set up projections
    void init() {
      // Projections
      /// @todo Use separate pT and ETmiss cuts in WFinder
      const WFinder wfe(-5, 5, 25.0*GeV, ELECTRON, 60.0*GeV, 100.0*GeV, 25.0*GeV, 0.2);
      addProjection(wfe, "WFe");

      // Cross-section histograms
      const BinEdges& edges = binEdges(1,1,1);
      _h_dsigplus_deta_25_35  = bookHisto1D("/dsigplus_deta_25_35", edges);
      _h_dsigminus_deta_25_35 = bookHisto1D("/dsigminus_deta_25_35", edges);
      _h_dsigplus_deta_35     = bookHisto1D("/dsigplus_deta_35", edges);
      _h_dsigminus_deta_35    = bookHisto1D("/dsigminus_deta_35", edges);
      _h_dsigplus_deta_25     = bookHisto1D("/dsigplus_deta_25", edges);
      _h_dsigminus_deta_25    = bookHisto1D("/dsigminus_deta_25", edges);
    }


    /// Do the analysis
    void analyze(const Event & event) {
      const WFinder& wf = applyProjection<WFinder>(event, "WFe");
      if (wf.size() == 0) {
        getLog() << Log::DEBUG << "No W candidates found: vetoing" << endl;
        vetoEvent;
      }

      // Require that leptons have Et >= 25 GeV
      /// @todo Use pT cut in WFinder
      /// @todo Any ETmiss cut?
      FourMomentum p_e=wf.constituentLepton().momentum();
      int chg_e = PID::threeCharge(wf.constituentLepton().pdgId());
      if (p_e.eta() < 0) chg_e *= -1;
      assert(chg_e != 0);

      const double weight = event.weight();
      const double eta_e = fabs(p_e.eta());
      const double et_e = p_e.Et();
      if (et_e < 35*GeV) {
        // 25 <= ET < 35
        if (chg_e < 0) {
          _h_dsigminus_deta_25_35->fill(eta_e, weight);
        } else {
          _h_dsigplus_deta_25_35->fill(eta_e, weight);
        }
      } else {
        // ET >= 35
        if (chg_e < 0) {
          _h_dsigminus_deta_35->fill(eta_e, weight);
        } else {
          _h_dsigplus_deta_35->fill(eta_e, weight);
        }
      }
      // Inclusive: ET >= 25
      if (chg_e < 0) {
        _h_dsigminus_deta_25->fill(eta_e, weight);
      } else {
        _h_dsigplus_deta_25->fill(eta_e, weight);
      }
    }


    /// Finalize
    void finalize() {
      // \todo YODA divide
      // Construct asymmetry: (dsig+/deta - dsig-/deta) / (dsig+/deta + dsig-/deta) for each Et region
      // IHistogram1D* num25_35 = hf.subtract("/num25_35", *_h_dsigplus_deta_25_35, *_h_dsigminus_deta_25_35);
      // num25_35->scale(100.);
      // IHistogram1D* denom25_35 = hf.add("/denom25_35", *_h_dsigplus_deta_25_35, *_h_dsigminus_deta_25_35);
      // assert(num25_35 && denom25_35);
      // hf.divide(histoDir() + "/d01-x01-y01", *num25_35, *denom25_35);
      // hf.destroy(num25_35);
      // hf.destroy(denom25_35);
      // //
      // IHistogram1D* num35 = hf.subtract("/num35", *_h_dsigplus_deta_35, *_h_dsigminus_deta_35);
      // num35->scale(100.);
      // IHistogram1D* denom35 = hf.add("/denom35", *_h_dsigplus_deta_35, *_h_dsigminus_deta_35);
      // assert(num35 && denom35);
      // hf.divide(histoDir() + "/d01-x01-y02", *num35, *denom35);
      // hf.destroy(num35);
      // hf.destroy(denom35);
      // //
      // IHistogram1D* num25 = hf.subtract("/num25", *_h_dsigplus_deta_25, *_h_dsigminus_deta_25);
      // num25->scale(100.);
      // IHistogram1D* denom25 = hf.add("/denom25", *_h_dsigplus_deta_25, *_h_dsigminus_deta_25);
      // assert(num25 && denom25);
      // hf.divide(histoDir() + "/d01-x01-y03", *num25, *denom25);
      // hf.destroy(num25);
      // hf.destroy(denom25);

      // // Delete raw histos
      // hf.destroy(_h_dsigplus_deta_25_35);
      // hf.destroy(_h_dsigminus_deta_25_35);
      // hf.destroy(_h_dsigplus_deta_35);
      // hf.destroy(_h_dsigminus_deta_35);
      // hf.destroy(_h_dsigplus_deta_25);
      // hf.destroy(_h_dsigminus_deta_25);
    }

    //@}


  private:

    /// @name Histograms
    //@{
    Histo1DPtr _h_dsigplus_deta_25_35, _h_dsigminus_deta_25_35;
    Histo1DPtr _h_dsigplus_deta_35, _h_dsigminus_deta_35;
    Histo1DPtr _h_dsigplus_deta_25, _h_dsigminus_deta_25;
    //@}

  };


  // This global object acts as a hook for the plugin system
  AnalysisBuilder<D0_2008_S7837160> plugin_D0_2008_S7837160;

}
