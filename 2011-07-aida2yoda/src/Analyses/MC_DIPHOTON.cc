// -*- C++ -*-
#include "Rivet/Analysis.hh"
#include "Rivet/RivetAIDA.hh"
#include "Rivet/Projections/FinalState.hh"
#include "Rivet/Projections/IdentifiedFinalState.hh"
#include "Rivet/Tools/Logging.hh"

namespace Rivet {


  /// @brief MC validation analysis for isolated di-photon events
  class MC_DIPHOTON : public Analysis {
  public:

    /// Constructor
    MC_DIPHOTON() : Analysis("MC_DIPHOTON") {
      setNeedsCrossSection(true);
    }


    /// @name Analysis methods
    //@{

    void init() {
      FinalState fs;
      addProjection(fs, "FS");

      IdentifiedFinalState ifs(-2.0, 2.0, 20.0*GeV);
      ifs.acceptId(PHOTON);
      addProjection(ifs, "IFS");

      _h_m_PP = bookHistogram1D("m_PP", logBinEdges(50, 1.0, 0.25*sqrtS()));
      _h_pT_PP = bookHistogram1D("pT_PP", logBinEdges(50, 1.0, 0.25*sqrtS()));
      _h_dphi_PP = bookHistogram1D("dphi_PP", 20, 0.0, M_PI);
    }


    void analyze(const Event& event) {
      const double weight = event.weight();

      ParticleVector photons = applyProjection<IdentifiedFinalState>(event, "IFS").particles();

      if (photons.size() < 2) {
        vetoEvent;
      }

      // Isolate photons with ET_sum in cone
      ParticleVector isolated_photons;
      ParticleVector fs = applyProjection<FinalState>(event, "FS").particles();
      foreach (const Particle& photon, photons) {
        FourMomentum mom_in_cone;
        double eta_P = photon.momentum().eta();
        double phi_P = photon.momentum().phi();
        foreach (const Particle& p, fs) {
          if (deltaR(eta_P, phi_P, p.momentum().eta(), p.momentum().phi()) < 0.4) {
            mom_in_cone += p.momentum();
          }
        }
        if (mom_in_cone.Et()-photon.momentum().Et() < 1.0*GeV) {
          isolated_photons.push_back(photon);
        }
      }

      if (isolated_photons.size() != 2) {
        vetoEvent;
      }

      FourMomentum mom_PP = isolated_photons[0].momentum() + isolated_photons[1].momentum();
      _h_m_PP->fill(mom_PP.mass(), weight);
      _h_pT_PP->fill(mom_PP.pT(), weight);
      _h_dphi_PP->fill(mapAngle0ToPi(isolated_photons[0].momentum().phi()-
                                     isolated_photons[1].momentum().phi())/M_PI, weight);
    }


    void finalize() {
      scale(_h_m_PP, crossSection()/sumOfWeights());
      scale(_h_pT_PP, crossSection()/sumOfWeights());
      scale(_h_dphi_PP, crossSection()/sumOfWeights());
    }

    //@}


  private:

    /// @name Histograms
    //@{
    AIDA::IHistogram1D* _h_m_PP;
    AIDA::IHistogram1D* _h_pT_PP;
    AIDA::IHistogram1D* _h_dphi_PP;
    //@}


  };



  // This global object acts as a hook for the plugin system
  AnalysisBuilder<MC_DIPHOTON> plugin_MC_DIPHOTON;

}

