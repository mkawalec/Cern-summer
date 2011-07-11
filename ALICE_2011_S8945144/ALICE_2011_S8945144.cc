// -*- C++ -*-
#include "Rivet/Analysis.hh"
#include "Rivet/RivetAIDA.hh"
#include "Rivet/Tools/Logging.hh"
#include "Rivet/Projections/FinalState.hh"

namespace Rivet {

  class ALICE_2011_S8945144 : public Analysis {
  public:

    /// @name Constructors etc.
    //@{

    /// Constructor
    ALICE_2011_S8945144()
      : Analysis("ALICE_2011_S8945144")
    {
      // setNeedsCrossSection(true);
    }

    //@}


  public:

    /// @name Analysis methods
    //@{

    /// Book histograms and initialise projections before the run
    void init() {

      /// @todo Initialise and register projections here
      const FinalState cnfs(-5.0, 5.0, 0*MeV);
      addProjection(cnfs, "FS");

      /// @todo Book histograms here, e.g.:
      // _h_XXXX = bookProfile1D(1, 1, 1);
      // _h_YYYY = bookHistogram1D(2, 1, 1);
      _hist_pi_plus = bookHistogram1D(1,1,1);
      _hist_pi_minus = bookHistogram1D(1,1,2);
      _hist_K_plus = bookHistogram1D(2,1,1);
      _hist_K_minus = bookHistogram1D(2,1,2);
      _hist_p_plus = bookHistogram1D(3,1,1);
      _hist_p_minus = bookHistogram1D(3,1,2);
    }


    /// Perform the per-event analysis
    void analyze(const Event& event) {
      const double weight = event.weight();

      /// @todo Do the event by event analysis here
      const FinalState& cnfs = applyProjection<FinalState>(event, "FS");

      foreach (const Particle& p, cnfs.particles()) {
        if (fabs(p.momentum().rapidity()) < 0.5) {
          const PdgId id = p.pdgId();
          const double pT = p.momentum().pT();
          switch (id) {
            case 2212:
              _hist_p_plus->fill(pT, weight); 
              break;
            case -2212:
              _hist_p_minus->fill(pT, weight); 
              break;
            case 211:
              _hist_pi_plus->fill(pT, weight); 
              break;
            case -211:
              _hist_pi_minus->fill(pT, weight); 
              break;
            case 321:
              _hist_K_plus->fill(pT, weight); 
              break;
            case -321:
              _hist_K_minus->fill(pT, weight); 
              break;
          }
        }
      }

    }

    /// Normalise histograms etc., after the run
    void finalize() {

      /// @todo Normalise, scale and otherwise manipulate histograms here

      // scale(_h_YYYY, crossSection()/sumOfWeights()); # norm to cross section
      // normalize(_h_YYYY); # normalize to unity
      normalize(_hist_p_plus);
      normalize(_hist_p_minus);
      normalize(_hist_pi_plus);
      normalize(_hist_pi_minus);
      normalize(_hist_K_plus);
      normalize(_hist_K_minus);

    }

    //@}


  private:

    // Data members like post-cuts event weight counters go here


  private:

    /// @name Histograms
    //@{

    AIDA::IProfile1D *_h_XXXX;
    AIDA::IHistogram1D *_h_YYYY;
    //@}
    AIDA::IHistogram1D *_hist_p_plus, *_hist_p_minus, *_hist_K_minus, *_hist_K_plus, *_hist_pi_plus, *_hist_pi_minus;

  };



  // This global object acts as a hook for the plugin system
  AnalysisBuilder<ALICE_2011_S8945144> plugin_ALICE_2011_S8945144;


}
