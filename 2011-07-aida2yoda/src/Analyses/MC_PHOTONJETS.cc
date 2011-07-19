// -*- C++ -*-
#include "Rivet/Analyses/MC_JetAnalysis.hh"
#include "Rivet/Projections/LeadingParticlesFinalState.hh"
#include "Rivet/Projections/FastJets.hh"
#include "Rivet/Tools/Logging.hh"
#include "Rivet/RivetAIDA.hh"

namespace Rivet {


  /// @brief MC validation analysis for photon + jets events
  class MC_PHOTONJETS : public MC_JetAnalysis {
  public:

    /// Default constructor
    MC_PHOTONJETS()
      : MC_JetAnalysis("MC_PHOTONJETS", 4, "Jets")
    {
      setNeedsCrossSection(true);
    }


    /// @name Analysis methods
    //@{

    /// Book histograms
    void init() {
      // General FS
      FinalState fs(-5.0, 5.0);
      addProjection(fs, "FS");

      // Get leading photon
      LeadingParticlesFinalState photonfs(FinalState(-1.0, 1.0, 30.0*GeV));
      photonfs.addParticleId(PHOTON);
      addProjection(photonfs, "LeadingPhoton");

      // FS for jets excludes the leading photon
      VetoedFinalState vfs(fs);
      vfs.addVetoOnThisFinalState(photonfs);
      addProjection(vfs, "JetFS");
      FastJets jetpro(vfs, FastJets::KT, 0.7);
      addProjection(jetpro, "Jets");

      _h_photon_pT = bookHistogram1D("photon_pT", logBinEdges(50, 30.0, 0.5*sqrtS()));
      _h_photon_y = bookHistogram1D("photon_y", 50, -5.0, 5.0);
      _h_photon_jet1_deta = bookHistogram1D("photon_jet1_deta", 50, -5.0, 5.0);
      _h_photon_jet1_dphi = bookHistogram1D("photon_jet1_dphi", 20, 0.0, M_PI);
      _h_photon_jet1_dR = bookHistogram1D("photon_jet1_dR", 25, 0.5, 7.0);

      MC_JetAnalysis::init();
    }


    /// Do the analysis
    void analyze(const Event& e) {
      // Get the photon
      const ParticleVector photons = applyProjection<FinalState>(e, "LeadingPhoton").particles();
      if (photons.size() != 1) {
        vetoEvent;
      }
      const FourMomentum photon = photons.front().momentum();

      // Get all charged particles
      const FinalState& fs = applyProjection<FinalState>(e, "JetFS");
      if (fs.empty()) {
        vetoEvent;
      }

      // Passed cuts, so get the weight
      const double weight = e.weight();

      // Isolate photon by ensuring that a 0.4 cone around it contains less than 7% of the photon's energy
      const double egamma = photon.E();
      double econe = 0.0;
      foreach (const Particle& p, fs.particles()) {
        if (deltaR(photon, p.momentum()) < 0.4) {
          econe += p.momentum().E();
          // Veto as soon as E_cone gets larger
          if (econe/egamma > 0.07) {
            vetoEvent;
          }
        }
      }

      _h_photon_pT->fill(photon.pT(),weight);
      _h_photon_y->fill(photon.rapidity(),weight);

      const FastJets& jetpro = applyProjection<FastJets>(e, "Jets");
      const Jets& jets = jetpro.jetsByPt(20.0*GeV);
      if (jets.size()>0) {
        _h_photon_jet1_deta->fill(photon.eta()-jets[0].momentum().eta(), weight);
        _h_photon_jet1_dphi->fill(mapAngle0ToPi(photon.phi()-jets[0].momentum().phi()), weight);
        _h_photon_jet1_dR->fill(deltaR(photon, jets[0].momentum()), weight);
      }

      MC_JetAnalysis::analyze(e);
    }


    // Finalize
    void finalize() {
      scale(_h_photon_pT, crossSectionPerEvent());
      scale(_h_photon_y, crossSectionPerEvent());
      scale(_h_photon_jet1_deta, crossSectionPerEvent());
      scale(_h_photon_jet1_dphi, crossSectionPerEvent());
      scale(_h_photon_jet1_dR, crossSectionPerEvent());

      MC_JetAnalysis::finalize();
    }

    //@}


  private:

    /// @name Histograms
    //@{
    AIDA::IHistogram1D * _h_photon_pT;
    AIDA::IHistogram1D * _h_photon_y;
    AIDA::IHistogram1D * _h_photon_jet1_deta;
    AIDA::IHistogram1D * _h_photon_jet1_dphi;
    AIDA::IHistogram1D * _h_photon_jet1_dR;
    //@}

  };



  // This global object acts as a hook for the plugin system
  AnalysisBuilder<MC_PHOTONJETS> plugin_MC_PHOTONJETS;

}
