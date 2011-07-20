// -*- C++ -*-
#include "Rivet/Analysis.hh"
#include "Rivet/RivetYODA.hh"
#include "Rivet/Projections/ChargedFinalState.hh"
#include "Rivet/Tools/ParticleIdUtils.hh"

namespace Rivet {


  class CMS_2010_S8547297 : public Analysis {
  public:

    CMS_2010_S8547297() : Analysis("CMS_2010_S8547297") {}

    void init() {
      ChargedFinalState cfs(-2.5, 2.5, 0.0*GeV);
      addProjection(cfs, "CFS");

      if(fuzzyEquals(sqrtS()/GeV, 900)){
        for (int d=1; d<=3; d++) {
          for (int y=1; y<=4; y++) {
            _h_dNch_dpT.push_back(bookHisto1D(d, 1, y));
          }
        }
        _h_dNch_dpT_all = bookHisto1D(7, 1, 1);
        _h_dNch_dEta = bookHisto1D(8, 1, 1);
      } else if (fuzzyEquals(sqrtS()/GeV, 2360)){
        for (int d=4; d<=6; d++) {
          for (int y=1; y<=4; y++) {
            _h_dNch_dpT.push_back(bookHisto1D(d, 1, y));
          }
        }
        _h_dNch_dpT_all = bookHisto1D(7, 1, 2);
        _h_dNch_dEta = bookHisto1D(8, 1, 2);
      }
    }


    void analyze(const Event& event) {
      const double weight = event.weight();

      //charged particles
      const ChargedFinalState& charged = applyProjection<ChargedFinalState>(event, "CFS");

      foreach (const Particle& p, charged.particles()) {
        //selecting only charged hadrons
        if(! PID::isHadron(p.pdgId())) continue;

        const double pT = p.momentum().pT();
        const double eta = p.momentum().eta();

        // The data is actually a duplicated folded distribution.  This should mimic it.
        _h_dNch_dEta->fill(eta, 0.5*weight);
        _h_dNch_dEta->fill(-eta, 0.5*weight);
        if (fabs(eta)<2.4 && pT>0.1) {
          if (pT<4.0) {
            _h_dNch_dpT_all->fill(pT, weight/pT);
            if (pT<2.0) {
              int ietabin = fabs(eta)/0.2;
              _h_dNch_dpT[ietabin]->fill(pT, weight);
            }
          }
        }
      }
    }

    void finalize() {
      const double normfac = 1.0/sumOfWeights(); // Normalizing to unit eta is automatic
      // The pT distributions in bins of eta must be normalized to unit eta.  This is a factor of 2
      // for the |eta| times 0.2 (eta range).
      // The pT distributions over all eta are normalized to unit eta (2.0*2.4) and by 1/2*pi*pT.
      // The 1/pT part is taken care of in the filling.  The 1/2pi is taken care of here.
      const double normpT = normfac/(2.0*0.2);
      const double normpTall = normfac/(2.0*M_PI*2.0*2.4);

      for (size_t ietabin=0; ietabin < _h_dNch_dpT.size(); ietabin++){
        scale(_h_dNch_dpT[ietabin], normpT);
      }
      scale(_h_dNch_dpT_all, normpTall);
      scale(_h_dNch_dEta, normfac);
    }


  private:
    std::vector<Histo1DPtr> _h_dNch_dpT;
    Histo1DPtr _h_dNch_dpT_all;
    Histo1DPtr _h_dNch_dEta;
   };

  // This global object acts as a hook for the plugin system
  AnalysisBuilder<CMS_2010_S8547297> plugin_CMS_2010_S8547297;
}

