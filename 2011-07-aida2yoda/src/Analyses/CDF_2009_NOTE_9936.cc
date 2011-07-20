// -*- C++ -*-
#include "Rivet/Analysis.hh"
#include "Rivet/RivetYODA.hh"
#include "Rivet/Tools/Logging.hh"
#include "Rivet/Projections/ChargedFinalState.hh"
#include "Rivet/Projections/TriggerCDFRun2.hh"

namespace Rivet {


  class CDF_2009_NOTE_9936 : public Analysis {
  public:

    /// @name Constructors etc.
    //@{

    /// Constructor
    CDF_2009_NOTE_9936()
      : Analysis("CDF_2009_NOTE_9936") 
        //_sumWPassed(0.0)
    {
      /// @todo Set approriate for your analysis
      setBeams(PROTON, ANTIPROTON);
      
      /// @todo Set whether your finalize method needs the generator cross section
      setNeedsCrossSection(false);
    }

    //@}


  public:

    /// @name Analysis methods
    //@{

    /// Book histograms and initialise projections before the run
    void init() {

      addProjection(TriggerCDFRun2(), "Trigger");
      
      addProjection(ChargedFinalState(-1.0, 1.0, 0.4*GeV), "CFS");

      _hist_nch = bookHisto1D(1, 1, 1);
    }


    /// Perform the per-event analysis
    void analyze(const Event& event) {
      // MinBias Trigger
      const bool trigger = applyProjection<TriggerCDFRun2>(event, "Trigger").minBiasDecision();
      if (!trigger) vetoEvent;
      //_sumWPassed += event.weight();
      const double weight = event.weight();

      // Get events charged multiplicity and fill histogram
      const ChargedFinalState& cfs = applyProjection<ChargedFinalState>(event, "CFS");
      _hist_nch->fill(cfs.size(), weight);

    }


    /// Normalise histograms etc., after the run
    void finalize() {
      normalize(_hist_nch);
    }

    //@}

  private:

    Histo1DPtr _hist_nch;

  };



  // This global object acts as a hook for the plugin system
  AnalysisBuilder<CDF_2009_NOTE_9936> plugin_CDF_2009_NOTE_9936;


}
