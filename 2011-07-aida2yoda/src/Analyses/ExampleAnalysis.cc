// -*- C++ -*-
#include "Rivet/Analysis.hh"
#include "Rivet/Tools/Logging.hh"
#include "Rivet/RivetAIDA.hh"
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
      _histTot         = bookHistogram1D("TotalMult", 100, -0.5, 99.5);
      _histChTot       = bookHistogram1D("TotalChMult", 50, -1.0, 99.0);
      _histHadrTot     = bookHistogram1D("HadrTotalMult", 100, -0.5, 99.5);
      _histHadrChTot   = bookHistogram1D("HadrTotalChMult", 50, -1.0, 99.0);
      _histMajor       = bookHistogram1D("Major", 10, 0.0, 0.6);
      _histSphericity  = bookHistogram1D("Sphericity", 10, 0.0, 0.8);
      _histAplanarity  = bookHistogram1D("Aplanarity", 10, 0.0, 0.3);

      // Non-uniform binning example:
      double edges[11] = { 0.5, 0.6, 0.7, 0.80, 0.85, 0.9, 0.92, 0.94, 0.96, 0.98, 1.0 };
      vector<double> vedges(edges, edges+11);
      _histThrust = bookHistogram1D("Thrust", vedges);
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
    AIDA::IHistogram1D* _histTot;
    AIDA::IHistogram1D* _histChTot;
    AIDA::IHistogram1D* _histHadrTot;
    AIDA::IHistogram1D* _histHadrChTot;
    AIDA::IHistogram1D* _histThrust;
    AIDA::IHistogram1D* _histMajor;
    AIDA::IHistogram1D* _histSphericity;
    AIDA::IHistogram1D* _histAplanarity;
    //@}

  };



  // This global object acts as a hook for the plugin system
  AnalysisBuilder<ExampleAnalysis> plugin_ExampleAnalysis;

}
