// -*- C++ -*-
#include "Rivet/Analysis.hh"
#include "Rivet/RivetAIDA.hh"
#include "Rivet/Tools/Logging.hh"
#include "Rivet/Projections/UnstableFinalState.hh"

namespace Rivet {

  class ALICE_2010_S8909580 : public Analysis {
  public:

    /// @name Constructors etc.
    //@{

    /// Constructor
    ALICE_2010_S8909580()
      : Analysis("ALICE_2010_S8909580")
    {
      setNeedsCrossSection(true);
    }

    //@}


  public:

    /// @name Analysis methods
    //@{

    /// Book histograms and initialise projections before the run
    void init() {

      /// @todo Initialise and register projections here
      const UnstableFinalState ufs(-5.0, 5.0, 0*MeV);
      addProjection(ufs, "UFS");

      /// @todo Book histograms here, e.g.:
      _hist_K0s = bookHistogram1D(1,1,1);
      _hist_lambda = bookHistogram1D(2,1,1);
      _hist_lambdabar = bookHistogram1D(3,1,1);
      _hist_xi = bookHistogram1D(4,1,1);
      _hist_phi = bookHistogram1D(5,1,1);
    }


    /// Perform the per-event analysis
    void analyze(const Event& event) {
      const double weight = event.weight();

      const UnstableFinalState& ufs = applyProjection<UnstableFinalState>(event, "UFS");

      foreach (const Particle& p, ufs.particles()) {
          const PdgId id = p.pdgId();
          const double pT = p.momentum().pT();
          switch (id) {
            case K0S:
              if (fabs(p.momentum().rapidity()) < 0.75) {
                _hist_K0s->fill(pT, weight); 
              }
              break;
            case LAMBDA:
              if (fabs(p.momentum().rapidity()) < 0.75) {
                _hist_lambda->fill(pT, weight); 
              }
              break;
            case LAMBDABAR:
              if (fabs(p.momentum().rapidity()) < 0.75) {
                _hist_lambdabar->fill(pT, weight); 
              }
              break;
            case XIMINUS:
              if (fabs(p.momentum().rapidity()) < 0.8) {
                _hist_xi->fill(pT, weight); 
              }
              break;
            case XIPLUS:
              if (fabs(p.momentum().rapidity()) < 0.8) {
                _hist_xi->fill(pT, weight); 
              }
              break;
            case 333:
              if (fabs(p.momentum().rapidity()) < 0.6) {
                _hist_phi->fill(pT, weight); 
              }
              break;
          }
        }
      }

    }


    /// Normalise histograms etc., after the run
    void finalize() {

      /// @todo Normalise, scale and otherwise manipulate histograms here
      // scale(_h_YYYY, crossSection()/sumOfWeights()); # norm to cross section

      normalize(_hist_K0s);
      normalize(_hist_lambda);
      normalize(_hist_lambdabar);
      normalize(_hist_xi);
      normalize(_hist_phi);
    }

    //@}


  private:
    // Data members like post-cuts event weight counters go here

  private:
    /// @name Histograms
    AIDA::IHistogram1D *_hist_K0s, *_hist_lambda, *_hist_lambdabar, *_hist_xi, *_hist_phi;

  };

  // This global object acts as a hook for the plugin system
  AnalysisBuilder<ALICE_2010_S8909580> plugin_ALICE_2010_S8909580;


}
