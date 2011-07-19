// -*- C++ -*-
#include "Rivet/Analysis.hh"
#include "Rivet/RivetAIDA.hh"
#include "Rivet/Tools/Logging.hh"
#include "Rivet/Projections/TriggerUA5.hh"
#include "Rivet/Projections/ChargedFinalState.hh"

namespace Rivet {


  class UA5_1987_S1640666 : public Analysis {
  public:

    /// Constructor
    UA5_1987_S1640666()
      : Analysis("UA5_1987_S1640666") 
    {
      setBeams(PROTON, ANTIPROTON);
      _sumWPassed = 0;
      
    }

    /// Book histograms and initialise projections before the run
    void init() {
      addProjection(TriggerUA5(), "Trigger");
      addProjection(ChargedFinalState(-5.0, 5.0), "CFS");

      _hist_mean_nch = bookHistogram1D(1, 1, 1);
      _hist_nch      = bookHistogram1D(3, 1, 1);

    }


    /// Perform the per-event analysis
    void analyze(const Event& event) {
      // Trigger
      const TriggerUA5& trigger = applyProjection<TriggerUA5>(event, "Trigger");
      if (!trigger.nsdDecision()) vetoEvent;

      const double weight = event.weight();
      _sumWPassed += weight;

      // Count final state particles in several eta regions
      const int Nch = applyProjection<ChargedFinalState>(event, "CFS").size();

      // Fill histograms
      _hist_nch->fill(Nch, weight);
      _hist_mean_nch->fill(_hist_mean_nch->binMean(0), Nch);

    }


    /// Normalise histograms etc., after the run
    void finalize() {
      
      scale(_hist_nch, 1.0/_sumWPassed);
      scale(_hist_mean_nch, 1.0/_sumWPassed);
      
    }

  private:
    
    double _sumWPassed;

    AIDA::IHistogram1D *_hist_mean_nch;
    AIDA::IHistogram1D *_hist_nch;

  };



  // This global object acts as a hook for the plugin system
  AnalysisBuilder<UA5_1987_S1640666> plugin_UA5_1987_S1640666;


}
