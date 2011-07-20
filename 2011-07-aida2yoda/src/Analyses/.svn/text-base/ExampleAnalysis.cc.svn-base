// -*- C++ -*-
#include "Rivet/Analysis.hh"
#include "Rivet/Tools/Logging.hh"
#include "Rivet/RivetYODA.hh"
#include "Rivet/Projections/FinalState.hh"
#include "Rivet/Projections/ChargedFinalState.hh"
#include "Rivet/Projections/FastJets.hh"
#include "Rivet/Projections/Multiplicity.hh"
#include "Rivet/Projections/Thrust.hh"
#include "Rivet/Projections/Sphericity.hh"

namespace Rivet {


  /// @brief Just measures a few random things as an example.
  class ExampleAnalysis : public Analysis {
  public:

    /// Constructor
    ExampleAnalysis()
      : Analysis("EXAMPLE")
    {
      // No counters etc. to initialise, hence nothing to do here!
    }


    /// @name Analysis methods
    //@{

    /// Set up projections and book histograms
    void init() {
      // Projections
      const FinalState cnfs(-4, 4, 2*GeV);
      const ChargedFinalState cfs(-4, 4, 2*GeV);
      addProjection(cnfs, "FS");
      addProjection(cfs, "CFS");
      addProjection(FastJets(cnfs, FastJets::KT, 0.7), "Jets");
      addProjection(Multiplicity(cfs), "CMult");
      addProjection(Multiplicity(cnfs), "CNMult");
      addProjection(Thrust(cfs), "Thrust");
      addProjection(Sphericity(cfs), "Sphericity");

      // Histograms
      _histTot         = bookHisto1D("TotalMult", 100, -0.5, 99.5);
      _histChTot       = bookHisto1D("TotalChMult", 50, -1.0, 99.0);
      _histHadrTot     = bookHisto1D("HadrTotalMult", 100, -0.5, 99.5);
      _histHadrChTot   = bookHisto1D("HadrTotalChMult", 50, -1.0, 99.0);
      _histMajor       = bookHisto1D("Major", 10, 0.0, 0.6);
      _histSphericity  = bookHisto1D("Sphericity", 10, 0.0, 0.8);
      _histAplanarity  = bookHisto1D("Aplanarity", 10, 0.0, 0.3);

      // Non-uniform binning example:
      double edges[11] = { 0.5, 0.6, 0.7, 0.80, 0.85, 0.9, 0.92, 0.94, 0.96, 0.98, 1.0 };
      vector<double> vedges(edges, edges+11);
      _histThrust = bookHisto1D("Thrust", vedges);
    }


    /// Do the analysis
    void analyze(const Event& event) {
      // Make sure to always include the event weight in histogram fills!
      const double weight = event.weight();

      const Multiplicity& cnm = applyProjection<Multiplicity>(event, "CNMult");
      MSG_DEBUG("Total multiplicity = " << cnm.totalMultiplicity());
      _histTot->fill(cnm.totalMultiplicity(), weight);
      MSG_DEBUG("Hadron multiplicity = " << cnm.hadronMultiplicity());
      _histHadrTot->fill(cnm.hadronMultiplicity(), weight);

      const Multiplicity& cm = applyProjection<Multiplicity>(event, "CMult");
      MSG_DEBUG("Total charged multiplicity = " << cm.totalMultiplicity());
      _histChTot->fill(cm.totalMultiplicity(), weight);
      MSG_DEBUG("Hadron charged multiplicity = " << cm.hadronMultiplicity());
      _histHadrChTot->fill(cm.hadronMultiplicity(), weight);

      const Thrust& t = applyProjection<Thrust>(event, "Thrust");
      MSG_DEBUG("Thrust = " << t.thrust());
      _histThrust->fill(t.thrust(), weight);
      _histMajor->fill(t.thrustMajor(), weight);

      const Sphericity& s = applyProjection<Sphericity>(event, "Sphericity");
      MSG_DEBUG("Sphericity = " << s.sphericity());
      _histSphericity->fill(s.sphericity(), weight);
      MSG_DEBUG("Aplanarity = " << s.aplanarity());
      _histAplanarity->fill(s.aplanarity(), weight);

      unsigned int num_b_jets = 0;
      const Jets jets = applyProjection<FastJets>(event, "Jets").jets(5*GeV);
      foreach (const Jet& j, jets) {
        if (j.containsBottom()) num_b_jets += 1;
      }
      MSG_DEBUG("Num B-jets with pT > 5 GeV = " << num_b_jets);
    }


    /// Finalize
    void finalize() {
      normalize(_histTot);
      normalize(_histChTot);
      normalize(_histHadrTot);
      normalize(_histHadrChTot);
      normalize(_histThrust);
      normalize(_histMajor);
      normalize(_histSphericity);
      normalize(_histAplanarity);
    }

    //@}


  private:

    //@{
    /// Histograms
    Histo1DPtr _histTot;
    Histo1DPtr _histChTot;
    Histo1DPtr _histHadrTot;
    Histo1DPtr _histHadrChTot;
    Histo1DPtr _histThrust;
    Histo1DPtr _histMajor;
    Histo1DPtr _histSphericity;
    Histo1DPtr _histAplanarity;
    //@}

  };



  // This global object acts as a hook for the plugin system
  AnalysisBuilder<ExampleAnalysis> plugin_ExampleAnalysis;

}
