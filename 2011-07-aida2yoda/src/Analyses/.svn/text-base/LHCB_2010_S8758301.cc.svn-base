// -*- C++ -*-
#include "Rivet/Analysis.hh"
#include "Rivet/RivetYODA.hh"
#include "Rivet/Tools/Logging.hh"
#include "Rivet/Projections/UnstableFinalState.hh"
#include "Rivet/Tools/ParticleIdUtils.hh"

namespace Rivet {


  class LHCB_2010_S8758301 : public Analysis {
  public:

    /// @name Constructors etc.
    //@{

    /// Constructor
    LHCB_2010_S8758301()
      : Analysis("LHCB_2010_S8758301"),
      sumKs0_30(0.0), sumKs0_35(0.0), sumKs0_40(0.0)

    {
      /// @todo Set whether your finalize method needs the generator cross section
      setNeedsCrossSection(false);
      setBeams(PROTON, PROTON);
    }

    //@}


  public:

    /// @name Analysis methods
    //@{

    /// Book histograms and initialise projections before the run
    void init() {

      addProjection(UnstableFinalState(), "UFS");

      _h_K0s_pt_y_30 = bookHisto1D(1,1,1);
      _h_K0s_pt_y_35 = bookHisto1D(1,1,2);
      _h_K0s_pt_y_40 = bookHisto1D(1,1,3);

    }


    /// Perform the per-event analysis
    void analyze(const Event& event) {
      const double weight = event.weight();
      const UnstableFinalState& ufs = applyProjection<UnstableFinalState>(event, "UFS");

      foreach (const Particle& p, ufs.particles()) {
        const PdgId id = abs(p.pdgId());

        if (id == 310) {
          double y  = p.momentum().rapidity();
          double pT = p.momentum().perp();
          if (y > 2.5 && y < 3.0) {
            //_h_K0s_pt_y_30->fill(pT, weight/(0.5*0.2));
            _h_K0s_pt_y_30->fill(pT, weight);
            sumKs0_30 += weight;
          }
          else if (y > 3.0 && y < 3.5) {
            //_h_K0s_pt_y_35->fill(pT, weight/(0.5*0.2));
            _h_K0s_pt_y_35->fill(pT, weight);
            sumKs0_35 += weight;
          }
          else if (y > 3.5 && y < 4.0) {
            //_h_K0s_pt_y_40->fill(pT, weight/(0.5*0.2));
            _h_K0s_pt_y_40->fill(pT, weight);
            sumKs0_40 += weight;
          }
        }
      }
      

    }


    /// Normalise histograms etc., after the run
    void finalize() {


      // here we normalise to reference data... 
      scale(_h_K0s_pt_y_30, 4.880000e+02/sumKs0_30);
      scale(_h_K0s_pt_y_35, 4.442000e+02/sumKs0_35);
      scale(_h_K0s_pt_y_40, 3.868000e+02/sumKs0_40);



    }

    //@}


  private:

    // Data members like post-cuts event weight counters go here


  private:

    /// @name Histograms
    //@{


    Histo1DPtr _h_K0s_pt_y_30;
    Histo1DPtr _h_K0s_pt_y_35;
    Histo1DPtr _h_K0s_pt_y_40;

    double sumKs0_30;
    double sumKs0_35;
    double sumKs0_40;

    //@}


  };



  // This global object acts as a hook for the plugin system
  AnalysisBuilder<LHCB_2010_S8758301> plugin_LHCB_2010_S8758301;


}
