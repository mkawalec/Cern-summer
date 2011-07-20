// -*- C++ -*-
#include "Rivet/Analysis.hh"
#include "Rivet/RivetYODA.hh"
#include "Rivet/Tools/Logging.hh"
#include "Rivet/Projections/FinalState.hh"
#include "Rivet/Projections/IdentifiedFinalState.hh"
#include "Rivet/Tools/BinnedHistogram.hh"

namespace Rivet {

  typedef std::pair<double, double> doublepair;


  /// @brief D0 direct photon pair production
  class D0_2010_S8570965 : public Analysis {
  public:

    D0_2010_S8570965()
      : Analysis("D0_2010_S8570965")
    {
      setBeams(PROTON, ANTIPROTON);
      setNeedsCrossSection(true);
    }


  public:

    void init() {
      FinalState fs;
      addProjection(fs, "FS");

      IdentifiedFinalState ifs(-0.9, 0.9, 20.0*GeV);
      ifs.acceptId(PHOTON);
      addProjection(ifs, "IFS");

      _h_M = bookHisto1D(1, 1, 1);
      _h_pT = bookHisto1D(2, 1, 1);
      _h_dPhi = bookHisto1D(3, 1, 1);
      _h_costheta = bookHisto1D(4, 1, 1);

      std::pair<double, double> M_ranges[] = { std::make_pair(30.0, 50.0),
                                               std::make_pair(50.0, 80.0),
                                               std::make_pair(80.0, 350.0) };

      for (size_t i=0; i<3; ++i) {
        _h_pT_M.addHistogram(M_ranges[i].first, M_ranges[i].second, bookHisto1D(5+3*i, 1, 1));
        _h_dPhi_M.addHistogram(M_ranges[i].first, M_ranges[i].second, bookHisto1D(6+3*i, 1, 1));
        _h_costheta_M.addHistogram(M_ranges[i].first, M_ranges[i].second, bookHisto1D(7+3*i, 1, 1));
      }
    }


    /// Perform the per-event analysis
    void analyze(const Event& event) {
      const double weight = event.weight();

      ParticleVector photons = applyProjection<IdentifiedFinalState>(event, "IFS").particlesByPt();
      if (photons.size() < 2 ||
          (photons[0].momentum().pT() < 21.0*GeV)) {
        vetoEvent;
      }

      // Isolate photons with ET_sum in cone
      ParticleVector isolated_photons;
      ParticleVector fs = applyProjection<FinalState>(event, "FS").particles();
      foreach (const Particle& photon, photons) {
        double eta_P = photon.momentum().eta();
        double phi_P = photon.momentum().phi();
        double Etsum=0.0;
        foreach (const Particle& p, fs) {
          if (p.genParticle().barcode()!=photon.genParticle().barcode() &&
              deltaR(eta_P, phi_P, p.momentum().eta(), p.momentum().phi()) < 0.4) {
            Etsum += p.momentum().Et();
          }
        }
        if (Etsum<2.5*GeV) {
          isolated_photons.push_back(photon);
        }
      }

      if (isolated_photons.size() != 2) {
        vetoEvent;
      }
      std::sort(isolated_photons.begin(), isolated_photons.end(), cmpParticleByPt);

      FourMomentum y1=isolated_photons[0].momentum();
      FourMomentum y2=isolated_photons[1].momentum();
      if (deltaR(y1, y2)<0.4) {
        vetoEvent;
      }

      FourMomentum yy=y1+y2;
      double Myy = yy.mass()/GeV;
      if (Myy<30.0 || Myy>350.0) {
        vetoEvent;
      }

      double pTyy = yy.pT()/GeV;
      if (Myy<pTyy) {
        vetoEvent;
      }

      double dPhiyy = mapAngle0ToPi(y1.phi()-y2.phi());
      if (dPhiyy<0.5*M_PI) {
        vetoEvent;
      }

      double costhetayy = fabs(tanh((y1.eta()-y2.eta())/2.0));

      _h_M->fill(Myy, weight);
      _h_pT->fill(pTyy, weight);
      _h_dPhi->fill(dPhiyy, weight);
      _h_costheta->fill(costhetayy, weight);

      _h_pT_M.fill(Myy, pTyy, weight);
      _h_dPhi_M.fill(Myy, dPhiyy, weight);
      _h_costheta_M.fill(Myy, costhetayy, weight);
    }


    void finalize() {

      scale(_h_M, crossSection()/sumOfWeights());
      scale(_h_pT, crossSection()/sumOfWeights());
      scale(_h_dPhi, crossSection()/sumOfWeights());
      scale(_h_costheta, crossSection()/sumOfWeights());

      _h_pT_M.scale(crossSection()/sumOfWeights(), this);
      _h_dPhi_M.scale(crossSection()/sumOfWeights(), this);
      _h_costheta_M.scale(crossSection()/sumOfWeights(), this);

    }


  private:

    Histo1DPtr _h_M;
    Histo1DPtr _h_pT;
    Histo1DPtr _h_dPhi;
    Histo1DPtr _h_costheta;
    BinnedHistogram<double> _h_pT_M;
    BinnedHistogram<double> _h_dPhi_M;
    BinnedHistogram<double> _h_costheta_M;

  };



  // This global object acts as a hook for the plugin system
  AnalysisBuilder<D0_2010_S8570965> plugin_D0_2010_S8570965;


}
