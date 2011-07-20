// -*- C++ -*-
#include "Rivet/Analyses/MC_JetAnalysis.hh"
#include "Rivet/Projections/FinalState.hh"
#include "Rivet/Projections/FastJets.hh"
#include "Rivet/Tools/Logging.hh"
#include "Rivet/RivetYODA.hh"

namespace Rivet {


  /// @brief MC validation analysis for jet events
  class MC_JETS : public MC_JetAnalysis {
  public:

    MC_JETS() : MC_JetAnalysis("MC_JETS", 4, "Jets")
    {
      setNeedsCrossSection(true);
    }


  public:

    void init() {
      FinalState fs;
      FastJets jetpro(fs, FastJets::KT, 0.7);
      addProjection(jetpro, "Jets");

      MC_JetAnalysis::init();
    }


    void analyze(const Event& event) {
      MC_JetAnalysis::analyze(event);
    }


    void finalize() {
      MC_JetAnalysis::finalize();
    }

  };

  AnalysisBuilder<MC_JETS> plugin_MC_JETS;

}
