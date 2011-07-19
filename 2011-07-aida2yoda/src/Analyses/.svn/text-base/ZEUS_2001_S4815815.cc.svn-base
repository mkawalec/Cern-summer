// -*- C++ -*-
#include "Rivet/Analysis.hh"
#include "Rivet/RivetAIDA.hh"
#include "Rivet/Tools/Logging.hh"
#include "Rivet/Projections/FastJets.hh"

namespace Rivet {


  /// @brief ZEUS dijet photoproduction study used in the ZEUS Jets PDF fit
  ///
  /// This class is a reproduction of the HZTool routine for the ZEUS
  /// dijet photoproduction paper which was used in the ZEUS Jets PDF fit.
  ///
  /// @author Jon Butterworth
  class ZEUS_2001_S4815815 : public Analysis {
  public:

    /// Constructor
    ZEUS_2001_S4815815() : Analysis("ZEUS_2001_S4815815")
    {
      setBeams(POSITRON, PROTON);
    }


    /// @name Analysis methods
    //@{

    // Book projections and histograms
    void init() {
      FinalState fs;
      addProjection(fs, "FS");
      /// @todo This is the *wrong* jet def: correct it!
      addProjection(FastJets(fs, FastJets::KT, 0.7), "Jets");
      getLog() << Log::WARN << "This analysis uses the wrong jet definition: the "
               << "paper just says 'a cone algorithm was applied to the CAL cells and jets "
               << "were reconstructed using the energies and positions of these cells'" << endl;

      /// @todo This doesn't seem to correspond to the plots in the paper (SPIRES 4730372)
      _histJetEt1 = bookHistogram1D("JetET1", 11, 14.0, 75.0);
    }


    // Do the analysis
    void analyze(const Event& event) {
      const double weight = event.weight();
      const JetAlg& jets = applyProjection<FastJets>(event, "Jets");
      getLog() << Log::INFO << "Jet multiplicity = " << jets.size() << endl;
      foreach (const Jet& j, jets.jets()) {
        _histJetEt1->fill(j.momentum().pT(), weight);
      }
    }
 
 
    // Finalize
    void finalize() {
      //
    }

    //@}

  private:

    /// @name Histograms
    //@{
    AIDA::IHistogram1D* _histJetEt1;
    //@}


  };

 
 
  // This global object acts as a hook for the plugin system
  AnalysisBuilder<ZEUS_2001_S4815815> plugin_ZEUS_2001_S4815815;

}
