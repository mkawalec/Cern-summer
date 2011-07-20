#include "Rivet/Analysis.hh"
#include "Rivet/RivetYODA.hh"
#include "Rivet/Tools/Logging.hh"
#include "Rivet/Projections/FinalState.hh"
#include "Rivet/Projections/FastJets.hh"

namespace Rivet {


  /// @brief CDF in-jet kT distribution analysis
  /// @todo Finish!
  class CDF_2009_S8057893 : public Analysis {
  public:

    /// Constructor
    CDF_2009_S8057893::CDF_2009_S8057893()
      : Analysis("CDF_2009_S8057893")
    {
      setBeams(PROTON, ANTIPROTON);
    }


    /// @name Analysis methods
    //@{

    void CDF_2009_S8057893::init() {
      const FinalState fsj(-4.0, 4.0, 0.0*GeV);
      addProjection(fsj, "FSJ");
      addProjection(FastJets(fsj, FastJets::CDFMIDPOINT, 1.0), "Jets");
    }


    void CDF_2009_S8057893::analyze(const Event& event) {
      const FastJets& jetpro = applyProjection<FastJets>(e, "MidpointJets");
      const Jets& jets = jetpro.jetsByPt();
      getLog() << Log::DEBUG << "Jet multiplicity = " << jets.size() << endl;
      if (jets.size() < 1) {
        getLog() << Log::DEBUG << "Failed jet multiplicity cut" << endl;
        vetoEvent;
      }

      // Email sent to authors:
      // Okay, so here are the questions:

      //  * What |eta| and pT_min acceptance cuts were used?
      //  * Is the "cone algorithm" JETCLU or MIDPOINT? You refer to the old 1992 paper that defines
      //    JETCLU, but I thought Run II analyses were using the more IRC-safe midpoint algorithm.
      //  * Effective min j1, j2 Et values?
      //  * Definition of "require the two leading jets to be well-balanced in Et"?
      //  * Definition of the complementary cones: per-jet for j1, j2? Otherwise, what is defn of
      //    "dijet axis" (since the two jet axes will not exactly match due to ISR and extra jets.)
      //    Complementary cones are same eta as jet, but phi +- 90 degrees? Radius of compl. cones
      //    = 1.0? Or defined in theta_c (not Lorentz invariant)?
      //  * kT of tracks rel to jet axis for all jets, j1 & j2, or just j1?

      // Herwig missing from plots!
      // Data tables? More dijet mass bins (only 3 are shown, but 8 are mentioned)


      // Only use tracks with kT > 0.3 GeV

      // Low histo limit: kT_jet > 0.5 GeV

      // Opening cone theta_c = 0.5 rad (in dijet rest frame)

      //  95 < Mjj < 132 GeV
      // 243 < Mjj < 323 GeV
      // 428 < Mjj < 563 GeV
      // < Mjj < GeV
      // < Mjj < GeV
      // < Mjj < GeV
      // < Mjj < GeV
      // < Mjj < GeV
    }


    void CDF_2009_S8057893::finalize() {

    }

    //@}

  };


  // This global object acts as a hook for the plugin system
  AnalysisBuilder<CDF_2009_S8057893> plugin_CDF_2009_S8057893;

}
