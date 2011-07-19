// -*- C++ -*-
#include "Rivet/Analysis.hh"
#include "Rivet/RivetAIDA.hh"
#include "Rivet/Projections/ChargedFinalState.hh"
#include "Rivet/Projections/FastJets.hh"
#include "Rivet/Tools/Logging.hh"
#include "LWH/Histogram1D.h"

namespace Rivet {

  class ATLAS_2010_CONF_2010_049 : public Analysis {
  public:

    ATLAS_2010_CONF_2010_049() : Analysis("ATLAS_2010_CONF_2010_049") {
      setNeedsCrossSection(true);
    }


    void init() {
      ChargedFinalState cfs(-1.5, 1.5, 0.5*GeV);
      addProjection(cfs, "CFS");

      FastJets jetsproj6(cfs, FastJets::ANTIKT, 0.6);
      addProjection(jetsproj6, "Jets6");

      FastJets jetsproj4(cfs, FastJets::ANTIKT, 0.4);
      addProjection(jetsproj4, "Jets4");

      for (size_t i=0 ; i<2 ; i++) {
        _h_xsec[i]       = bookHistogram1D(1+i, 1, 1);
        _h_frag_04_06[i] = bookHistogram1D(3+i, 1, 1);
        _h_frag_06_10[i] = bookHistogram1D(3+i, 2, 1);
        _h_frag_10_15[i] = bookHistogram1D(3+i, 3, 1);
        _h_frag_15_24[i] = bookHistogram1D(3+i, 4, 1);
        _njets_04_06[i] = 0.0;
        _njets_06_10[i] = 0.0;
        _njets_10_15[i] = 0.0;
        _njets_15_24[i] = 0.0;
      }
    }


    void analyze(const Event& event) {
      const double weight = event.weight();

      const FastJets & jetsproj6 = applyProjection<FastJets>(event, "Jets6");
      const FastJets & jetsproj4 = applyProjection<FastJets>(event, "Jets4");
      Jets alljets[2];
      alljets[0] = jetsproj6.jetsByPt(4.0*GeV);
      alljets[1] = jetsproj4.jetsByPt(4.0*GeV);

      for (size_t i=0 ; i<2 ; i++) {
        Jets jets;

        // First we want to make sure that we only use jets within |eta|<0.57
        foreach (const Jet& jet, alljets[i]) {
          if (fabs(jet.momentum().eta())<0.57) {
            jets.push_back(jet);
          }
        }
        foreach (const Jet& jet, jets) {
          const double pTjet = jet.momentum().pT();
          const double pjet = jet.momentum().p().mod();
          _h_xsec[i]->fill(pTjet, weight);
          if (pTjet > 24*GeV) continue;
          foreach (const Particle& p, jet.particles()) {
            const double z=p.momentum().p().mod()/pjet;
            if (pTjet > 15*GeV) {
              _h_frag_15_24[i]->fill(z, weight);
            }
            else if (pTjet > 10*GeV) {
              _h_frag_10_15[i]->fill(z, weight);
            }
            else if (pTjet > 6*GeV) {
              _h_frag_06_10[i]->fill(z, weight);
            }
            else {
              _h_frag_04_06[i]->fill(z, weight);
            }
          }
          if (pTjet > 15*GeV) {
            _njets_15_24[i] += weight;
          }
          else if (pTjet > 10*GeV) {
            _njets_10_15[i] += weight;
          }
          else if (pTjet > 6*GeV) {
            _njets_06_10[i] += weight;
          }
          else {
            _njets_04_06[i] += weight;
          }
        }
      }
    }

    void finalize() {
      for (size_t i=0 ; i<2 ; i++) {
        // deta = 2*0.57
        scale(_h_xsec[i], crossSection()/microbarn/sumOfWeights()/(2*0.57));
        scale(_h_frag_04_06[i], 1./_njets_04_06[i]);
        scale(_h_frag_06_10[i], 1./_njets_06_10[i]);
        scale(_h_frag_10_15[i], 1./_njets_10_15[i]);
        scale(_h_frag_15_24[i], 1./_njets_15_24[i]);
      }
    }


  private:

    AIDA::IHistogram1D* _h_xsec[2];
    AIDA::IHistogram1D* _h_frag_04_06[2];
    AIDA::IHistogram1D* _h_frag_06_10[2];
    AIDA::IHistogram1D* _h_frag_10_15[2];
    AIDA::IHistogram1D* _h_frag_15_24[2];
    double _njets_04_06[2];
    double _njets_06_10[2];
    double _njets_10_15[2];
    double _njets_15_24[2];
  };

  // This global object acts as a hook for the plugin system
  AnalysisBuilder<ATLAS_2010_CONF_2010_049> plugin_ATLAS_2010_CONF_2010_049;

}

