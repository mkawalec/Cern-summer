// -*- C++ -*-
#include "Rivet/Analysis.hh"
#include "Rivet/Projections/FinalState.hh"
#include "Rivet/Projections/IdentifiedFinalState.hh"
#include "Rivet/RivetAIDA.hh"
#include "Rivet/Tools/Logging.hh"

namespace Rivet {


  /// @brief CDF diff cross-sections for prompt di-photon production
  class CDF_2005_S6080774 : public Analysis {
  public:

    /// Constructor
    CDF_2005_S6080774() : Analysis("CDF_2005_S6080774") {
      setBeams(PROTON, ANTIPROTON);
      setNeedsCrossSection(true);
    }


    /// @name Analysis methods
    //@{

    void init() {
      FinalState fs;
      addProjection(fs, "FS");

      IdentifiedFinalState ifs(-0.9, 0.9, 13.0*GeV);
      ifs.acceptId(PHOTON);
      addProjection(ifs, "IFS");

      for (size_t yAxisId=1; yAxisId<5; ++yAxisId) {
        _h_m_PP.push_back(bookHistogram1D(1, 1, yAxisId));
        _h_pT_PP.push_back(bookHistogram1D(2, 1, yAxisId));
        _h_dphi_PP.push_back(bookHistogram1D(3, 1, yAxisId));
      }
    }


    void analyze(const Event& event) {
      const double weight = event.weight();

      ParticleVector photons = applyProjection<IdentifiedFinalState>(event, "IFS").particlesByPt();
      if (photons.size() < 2 ||
          (photons[0].momentum().pT() < 14.0*GeV)) {
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
      for (size_t i=0; i<4; ++i) {
        _h_m_PP[i]->fill(mom_PP.mass(), weight);
        _h_pT_PP[i]->fill(mom_PP.pT(), weight);
        _h_dphi_PP[i]->fill(mapAngle0ToPi(isolated_photons[0].momentum().phi()-
                                          isolated_photons[1].momentum().phi())/M_PI, weight);
      }
    }


    void finalize() {
      for (size_t i=0; i<4; ++i) {
        scale(_h_m_PP[i], crossSection()/sumOfWeights());
        scale(_h_pT_PP[i], crossSection()/sumOfWeights());
        scale(_h_dphi_PP[i], crossSection()/M_PI/sumOfWeights());
      }
    }

    //@}


  private:

    /// @name Histograms
    //@{
    std::vector<AIDA::IHistogram1D*> _h_m_PP;
    std::vector<AIDA::IHistogram1D*> _h_pT_PP;
    std::vector<AIDA::IHistogram1D*> _h_dphi_PP;
    //@}


  };



  // This global object acts as a hook for the plugin system
  AnalysisBuilder<CDF_2005_S6080774> plugin_CDF_2005_S6080774;

}
