// -*- C++ -*-

#include "Rivet/Analysis.hh"
#include "Rivet/RivetYODA.hh"
#include "Rivet/Projections/FinalState.hh"
#include "Rivet/Projections/FastJets.hh"
#include "Rivet/Projections/Thrust.hh"
#include "Rivet/Tools/Logging.hh"

namespace Rivet {

  /// Rivet analysis class for CMS_2011_S8957746 dataset
  class CMS_2011_S8957746 : public Analysis {
  public:

    /// Default constructor
    CMS_2011_S8957746() : Analysis("CMS_2011_S8957746") {
      setBeams(PROTON, PROTON);
    }

    /// Initialization, called once before running
    void init() {
      // Projections
      const FastJets jets(FinalState(-5.0, 5.0, 0.0*GeV), FastJets::ANTIKT, 0.5);
      addProjection(jets, "Jets");

      // Book histograms
      _hist_T_90  = bookHisto1D(1, 1, 1);
      _hist_m_90  = bookHisto1D(2, 1, 1);
      _hist_T_125 = bookHisto1D(1, 2, 1);
      _hist_m_125 = bookHisto1D(2, 2, 1);
      _hist_T_200 = bookHisto1D(1, 3, 1);
      _hist_m_200 = bookHisto1D(2, 3, 1);
    }

    void analyze(const Event& event) {
      const double weight = event.weight();
      const Jets& jets = applyProjection<FastJets>(event, "Jets").jetsByPt(30.0*GeV);
      if (jets.size() < 2 ||
          fabs(jets[0].momentum().eta())>=1.3 ||
          fabs(jets[1].momentum().eta())>=1.3 ||
          jets[0].momentum().pT()<90) {
        vetoEvent;
      }
      std::vector<Vector3> momenta;
      foreach (Jet j, jets) {
        if (fabs(j.momentum().eta())<1.3) {
          Vector3 mom = j.momentum().vector3();
          mom.setZ(0.0);
          momenta.push_back(mom);
        }
      }
      if (momenta.size()==2) {
        // We need to use a ghost so that Thrust.calc() doesn't return 1.
        momenta.push_back(Vector3(1e-10*MeV, 0., 0.));
      }
      Thrust thrust;
      thrust.calc(momenta);

      // The lowest bin also includes the underflow:
      const double T=max(log(1-thrust.thrust()), -12.0);
      const double M=max(log(thrust.thrustMajor()), -6.0);
      if (jets[0].momentum().pT()>200) {
        _hist_T_200->fill(T, weight);
        _hist_m_200->fill(M, weight);
      } else if (jets[0].momentum().pT()>125) {
        _hist_T_125->fill(T, weight);
        _hist_m_125->fill(M, weight);
      } else if (jets[0].momentum().pT()>90) {
        _hist_T_90->fill(T, weight);
        _hist_m_90->fill(M, weight);
      }
    }

    void finalize() {
      normalize(_hist_T_90);
      normalize(_hist_m_90);
      normalize(_hist_T_125);
      normalize(_hist_m_125);
      normalize(_hist_T_200);
      normalize(_hist_m_200);
    }

  private:

    Histo1DPtr _hist_T_90;
    Histo1DPtr _hist_m_90;
    Histo1DPtr _hist_T_125;
    Histo1DPtr _hist_m_125;
    Histo1DPtr _hist_T_200;
    Histo1DPtr _hist_m_200;
  };

  // This global object acts as a hook for the plugin system
  AnalysisBuilder<CMS_2011_S8957746> plugin_CMS_2011_S8957746;
}
