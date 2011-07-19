// -*- C++ -*-
#include "Rivet/Rivet.hh"
#include "Rivet/Tools/Logging.hh"
#include "Rivet/Projections/Beam.hh"
#include "Rivet/Projections/ChargedFinalState.hh"
#include "Rivet/Projections/TriggerCDFRun2.hh"

namespace Rivet {


  void TriggerCDFRun2::project(const Event& evt) {
    // Start with the assumption that the trigger fails
    _decision_mb = false;

    // Run 2 Minimum Bias trigger requirements: 
    int n_trig_1 = 0;
    int n_trig_2 = 0;
    const ChargedFinalState& cfs = applyProjection<ChargedFinalState>(evt, "CFS");
    foreach (const Particle& p, cfs.particles()) {
      const double eta = p.momentum().pseudorapidity();
      if (inRange(eta, -4.7, -3.7)) n_trig_1++;
      else if (inRange(eta, 3.7, 4.7)) n_trig_2++;
    }
    
    // Require at least one charged particle in both -4.7 < eta < -3.7 and 3.7 < eta < 4.7
    if (n_trig_1 == 0 || n_trig_2 == 0) return;
    getLog() << Log::DEBUG << "Trigger 1: " << n_trig_1 << " Trigger 2: " << n_trig_2 << endl;
 
    // Trigger success:
    _decision_mb = true;
  }


}
