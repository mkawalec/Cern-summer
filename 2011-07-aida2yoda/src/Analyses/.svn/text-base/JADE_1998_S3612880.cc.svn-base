// -*- C++ -*-
#include "Rivet/Analysis.hh"
#include "Rivet/RivetAIDA.hh"
#include "Rivet/Tools/Logging.hh"
#include "Rivet/Projections/Thrust.hh"
#include "Rivet/Projections/FastJets.hh"
#include "Rivet/Projections/Hemispheres.hh"
#include "Rivet/Projections/ChargedFinalState.hh"
/// @todo Include more projections as required, e.g. ChargedFinalState, FastJets, ZFinder...

namespace Rivet {


  class JADE_1998_S3612880 : public Analysis {
  public:

    /// @name Constructors etc.
    //@{

    /// Constructor
    JADE_1998_S3612880()
      : Analysis("JADE_1998_S3612880")
    {
      /// @todo Set whether your finalize method needs the generator cross section
      setBeams(ELECTRON, POSITRON);
    }



    /// Book histograms and initialise projections before the run
    void init() {
      const ChargedFinalState cfs(-MAXRAPIDITY, MAXRAPIDITY, 0.1/GeV);
      addProjection(cfs, "CFS");
      addProjection(FastJets(cfs, FastJets::DURHAM, 0.7), "DurhamJets");
      
      // Thrust
      const Thrust thrust(cfs);
      addProjection(thrust, "Thrust");
      addProjection(Hemispheres(thrust), "Hemispheres");

      // Histos
      int offset = 0;
      switch (int(sqrtS()/GeV)) {

        case 44:
          offset = 0;
          _h_thrust  = bookHistogram1D( 2+offset, 1, 1);
          _h_MH = bookHistogram1D( 3 + offset, 1, 1);
          _h_BT = bookHistogram1D( 4 + offset, 1, 1);
          _h_BW = bookHistogram1D( 5 + offset, 1, 1);
          _h_y23 = bookHistogram1D(10, 1, 1);
          break;
        case 35:
          offset = 4;
          _h_thrust  = bookHistogram1D( 2+offset, 1, 1);
          _h_MH = bookHistogram1D( 3 + offset, 1, 1);
          _h_BT = bookHistogram1D( 4 + offset, 1, 1);
          _h_BW = bookHistogram1D( 5 + offset, 1, 1);
          _h_y23 = bookHistogram1D(11, 1, 1);
          break;
        case 22:
          _h_y23 = bookHistogram1D(12, 1, 1);
          break;
      }
    }


    /// Perform the per-event analysis
    void analyze(const Event& event) {
      const double weight = event.weight();
      const ChargedFinalState& cfs = applyProjection<ChargedFinalState>(event, "CFS");

      // JADE hadronic event selection TODO: move this into a trigger definition
      if (cfs.particles().size() < 3 ) {
        vetoEvent;
      }
      const Thrust& thrust = applyProjection<Thrust>(event, "Thrust");
      const Vector3 & thrustAxis = thrust.thrustAxis ();
      double theta = thrustAxis.theta();
      if ( fabs(cos(theta)) >= 0.8 ) {
        getLog() << Log::DEBUG << "Failed thrust angle cut: " << fabs(cos(theta)) << endl;
        vetoEvent;
      }
      // TODO Evis, pmiss, pbal

      const Hemispheres& hemi = applyProjection<Hemispheres>(event, "Hemispheres");
      const FastJets& durjet = applyProjection<FastJets>(event, "DurhamJets");

      double y23 = durjet.clusterSeq()->exclusive_ymerge_max(2);
      
      // Make sure we don't run into a segfault by trying to fill non-existing histos
      int s = int(sqrtS()/GeV);
      if (s == 44 || s == 35) {
        _h_thrust->fill(1. - thrust.thrust(), weight);
        _h_MH->fill(sqrt(hemi.scaledM2high()), weight);
        _h_BT->fill(hemi.Bsum(), weight);
        _h_BW->fill(hemi.Bmax(), weight);
      }
      _h_y23->fill(y23, weight);
    }

    /// Normalise histograms etc., after the run
    void finalize() {
      // Make sure we don't try to normalise non-existing histos
      int s = int(sqrtS()/GeV);
      if (s == 44 || s == 35) {
        normalize(_h_thrust);
        normalize(_h_MH);
        normalize(_h_BT);
        normalize(_h_BW);
      }
      normalize(_h_y23);


    }

    //@}


  private:

    AIDA::IHistogram1D *_h_thrust;
    AIDA::IHistogram1D *_h_MH;
    AIDA::IHistogram1D *_h_BT;
    AIDA::IHistogram1D *_h_BW;
    AIDA::IHistogram1D *_h_y23;


  };



  // This global object acts as a hook for the plugin system
  AnalysisBuilder<JADE_1998_S3612880> plugin_JADE_1998_S3612880;


}
