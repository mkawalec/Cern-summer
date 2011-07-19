// -*- C++ -*-
#include "Rivet/Analysis.hh"
#include "Rivet/Projections/ChargedFinalState.hh"
#include "Rivet/Projections/Multiplicity.hh"
#include "Rivet/Tools/Logging.hh"
#include "Rivet/RivetAIDA.hh"

namespace Rivet {


  /// @brief ALEPH LEP1 charged multiplicity in hadronic Z decay
  /// @author Andy Buckley
  class ALEPH_1991_S2435284 : public Analysis {
  public:

    /// Constructor.
    ALEPH_1991_S2435284()
      : Analysis("ALEPH_1991_S2435284")
    {
      setBeams(ELECTRON, POSITRON);
    }


    /// @name Analysis methods
    //@{

    /// Book projections and histogram
    void init() {
      const ChargedFinalState cfs;
      addProjection(cfs, "FS");
      addProjection(Multiplicity(cfs), "Mult");

      _histChTot = bookHistogram1D(1, 1, 1);
    }


    /// Do the analysis
    void analyze(const Event& event) {
      const Multiplicity& m = applyProjection<Multiplicity>(event, "Mult");
      getLog() << Log::DEBUG << "Total charged multiplicity = " << m.totalMultiplicity() << endl;
      _histChTot->fill(m.totalMultiplicity(), event.weight());
    }


    /// Normalize the histogram
    void finalize() {
      scale(_histChTot, 2.0/sumOfWeights()); // same as in ALEPH 1996
    }

    //@}


  private:

    /// @name Histograms
    //@{
    AIDA::IHistogram1D* _histChTot;
    //@}

  };


  // This global object acts as a hook for the plugin system
  AnalysisBuilder<ALEPH_1991_S2435284> plugin_ALEPH_1991_S2435284;

}
