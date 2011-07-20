// -*- C++ -*-
#include "Rivet/Analyses/MC_JetAnalysis.hh"
#include "Rivet/Projections/FastJets.hh"
#include "Rivet/Tools/Logging.hh"
#include "Rivet/RivetYODA.hh"

namespace Rivet {


  MC_JetAnalysis::MC_JetAnalysis(const string& name,
                                 size_t njet,
                                 const string& jetpro_name,
                                 double jetptcut)
    : Analysis(name), m_njet(njet), m_jetpro_name(jetpro_name), m_jetptcut(jetptcut),
      _h_log10_d(njet), _h_log10_R(njet+1), _h_pT_jet(njet),
      _h_eta_jet(njet), _h_eta_jet_plus(njet), _h_eta_jet_minus(njet),
      _h_rap_jet(njet), _h_rap_jet_plus(njet), _h_rap_jet_minus(njet),
     _h_mass_jet(njet)
  {
    setNeedsCrossSection(true);
  }



  // Book histograms
  void MC_JetAnalysis::init() {

    for (size_t i=0; i < m_njet; ++i) {
      stringstream dname;
      dname << "log10_d_" << i << i+1;

      _h_log10_d[i] = bookHisto1D(dname.str(), 50, 0.2, log10(0.5*sqrtS()));

      stringstream Rname;
      Rname << "log10_R_" << i;
      _h_log10_R[i] = bookScatter2D(Rname.str(), 50, 0.2, log10(0.5*sqrtS()));

      stringstream pTname;
      pTname << "jet_pT_" << i+1;
      double pTmax = 1.0/(double(i)+2.0) * sqrtS()/GeV/2.0;
      int nbins_pT = 100/(i+1);
      _h_pT_jet[i] = bookHisto1D(pTname.str(), logBinEdges(nbins_pT, 10.0, pTmax));

      stringstream massname;
      massname << "jet_mass_" << i+1;
      double mmax = 100.0;
      int nbins_m = 100/(i+1);
      _h_mass_jet[i] = bookHisto1D(massname.str(), logBinEdges(nbins_m, 1.0, mmax));

      stringstream etaname;
      etaname << "jet_eta_" << i+1;
      _h_eta_jet[i] = bookHisto1D(etaname.str(), i > 1 ? 25 : 50, -5.0, 5.0);
      _h_eta_jet_plus[i].reset(new Histo1D(i > 1 ? 15 : 25, 0, 5));
      _h_eta_jet_minus[i].reset(new Histo1D(i > 1 ? 15 : 25, 0, 5));

      stringstream rapname;
      rapname << "jet_y_" << i+1;
      _h_rap_jet[i] = bookHisto1D(rapname.str(), i>1 ? 25 : 50, -5.0, 5.0);
      _h_rap_jet_plus[i].reset(new Histo1D(i > 1 ? 15 : 25, 0, 5));
      _h_rap_jet_minus[i].reset(new Histo1D(i > 1 ? 15 : 25, 0, 5));

      for (size_t j = i+1; j < m_njet; ++j) {
        std::pair<size_t, size_t> ij = std::make_pair(i, j);

        stringstream detaname;
        detaname << "jets_deta_" << i+1 << j+1;
        _h_deta_jets.insert(make_pair(ij, bookHisto1D(detaname.str(), 25, -5.0, 5.0)));

        stringstream dRname;
        dRname << "jets_dR_" << i+1 << j+1;
        _h_dR_jets.insert(make_pair(ij, bookHisto1D(dRname.str(), 25, 0.0, 5.0)));
      }
    }
    stringstream Rname;
    Rname << "log10_R_" << m_njet;
    _h_log10_R[m_njet] = bookScatter2D(Rname.str(), 50, 0.2, log10(0.5*sqrtS()));

    _h_jet_multi_exclusive = bookHisto1D("jet_multi_exclusive", m_njet+3, -0.5, m_njet+3-0.5);
    _h_jet_multi_inclusive = bookHisto1D("jet_multi_inclusive", m_njet+3, -0.5, m_njet+3-0.5);
    _h_jet_multi_ratio = bookScatter2D("jet_multi_ratio", m_njet+2, 0.5, m_njet+3-0.5);
    _h_jet_HT = bookHisto1D("jet_HT", logBinEdges(50, m_jetptcut, sqrtS()/GeV/2.0));
  }



  // Do the analysis
  void MC_JetAnalysis::analyze(const Event & e) {
    const double weight = e.weight();

    const FastJets& jetpro = applyProjection<FastJets>(e, m_jetpro_name);

    // Jet resolutions and integrated jet rates
    const fastjet::ClusterSequence* seq = jetpro.clusterSeq();
    if (seq != NULL) {
      double previous_dij = 10.0;
      for (size_t i = 0; i < m_njet; ++i) {
        // Jet resolution i -> j
        double d_ij = log10(sqrt(seq->exclusive_dmerge_max(i)));

        // Fill differential jet resolution
        _h_log10_d[i]->fill(d_ij, weight);

        // Fill integrated jet resolution
        for (size_t ibin = 0; ibin < _h_log10_R[i]->numPoints(); ++ibin) {
          Point2D & dp = _h_log10_R[i]->point(ibin);
          double dcut = dp.x();
          if (d_ij < dcut && previous_dij > dcut) {
            dp.setY(dp.y() + weight);
          }
        }
        previous_dij = d_ij;
      }
      // One remaining integrated jet resolution
      for (size_t ibin = 0; ibin<_h_log10_R[m_njet]->numPoints(); ++ibin) {
        Point2D & dp = _h_log10_R[m_njet]->point(ibin);
        double dcut = dp.x();
        if (previous_dij > dcut) {
          dp.setY(dp.y() + weight);
        }
      }
    }

    const Jets& jets = jetpro.jetsByPt(m_jetptcut);

    // The remaining direct jet observables
    for (size_t i = 0; i < m_njet; ++i) {
      if (jets.size() < i+1) continue;
      _h_pT_jet[i]->fill(jets[i].momentum().pT()/GeV, weight);
      // Check for numerical precision issues with jet masses
      double m2_i = jets[i].momentum().mass2();
      if (m2_i < 0) {
        if (m2_i < -1e-4) {
          getLog() << Log::WARNING << "Jet mass2 is negative: " << m2_i << " GeV^2. "
                   << "Truncating to 0.0, assuming numerical precision is to blame." << endl;
        }
        m2_i = 0.0;
      }

      // Jet mass
      _h_mass_jet[i]->fill(sqrt(m2_i)/GeV, weight);

      // Jet eta
      const double eta_i = jets[i].momentum().eta();
      _h_eta_jet[i]->fill(eta_i, weight);
      if (eta_i > 0.0) {
        _h_eta_jet_plus[i]->fill(eta_i, weight);
      } else {
        _h_eta_jet_minus[i]->fill(fabs(eta_i), weight);
      }

      // Jet rapidity
      const double rap_i = jets[i].momentum().rapidity();
      _h_rap_jet[i]->fill(rap_i, weight);
      if (rap_i > 0.0) {
        _h_rap_jet_plus[i]->fill(rap_i, weight);
      } else {
        _h_rap_jet_minus[i]->fill(fabs(rap_i), weight);
      }

      // Inter-jet properties
      for (size_t j = i+1; j < m_njet; ++j) {
        if (jets.size() < j+1) continue;
        std::pair<size_t, size_t> ij = std::make_pair(i, j);
        double deta = jets[i].momentum().eta()-jets[j].momentum().eta();
        double dR = deltaR(jets[i].momentum(), jets[j].momentum());
        _h_deta_jets[ij]->fill(deta, weight);
        _h_dR_jets[ij]->fill(dR, weight);
      }
    }
    _h_jet_multi_exclusive->fill(jets.size(), weight);

    for (size_t i = 0; i < m_njet+2; ++i) {
      if (jets.size() >= i) {
        _h_jet_multi_inclusive->fill(i, weight);
      }
    }

    double HT=0.0;
    foreach (const Jet& jet, jets) {
      HT += jet.momentum().pT();
    }
    _h_jet_HT->fill(HT, weight);
  }


  // Finalize
  void MC_JetAnalysis::finalize() {
    for (size_t i = 0; i < m_njet; ++i) {
      scale(_h_log10_d[i], crossSection()/sumOfWeights());
      for (size_t ibin = 0; ibin<_h_log10_R[i]->numPoints(); ++ibin) {
        Point2D & dp = _h_log10_R[i]->point(ibin);
        dp.setY(dp.y()*crossSection()/sumOfWeights());
      }

      scale(_h_pT_jet[i], crossSection()/sumOfWeights());
      scale(_h_mass_jet[i], crossSection()/sumOfWeights());
      scale(_h_eta_jet[i], crossSection()/sumOfWeights());
      scale(_h_rap_jet[i], crossSection()/sumOfWeights());

      // Create eta/rapidity ratio plots
      stringstream etaname;
      etaname << "jet_eta_pmratio_" << i+1;
      // \todo YODA divide
      // histogramFactory().divide(histoPath(etaname.str()), *_h_eta_jet_plus[i], *_h_eta_jet_minus[i]);
      stringstream rapname;
      rapname << "jet_y_pmratio_" << i+1;
      // histogramFactory().divide(histoPath(rapname.str()), *_h_rap_jet_plus[i], *_h_rap_jet_minus[i]);
    }

    for (size_t ibin = 0; ibin < _h_log10_R[m_njet]->numPoints(); ++ibin) {
      Point2D & dp =_h_log10_R[m_njet]->point(ibin);
      dp.setY(dp.y()*crossSection()/sumOfWeights());
    }

    // Scale the d{eta,R} histograms
    map<pair<size_t, size_t>, Histo1DPtr>::iterator it;
    for (it = _h_deta_jets.begin(); it != _h_deta_jets.end(); ++it) {
      scale(it->second, crossSection()/sumOfWeights());
    }
    for (it = _h_dR_jets.begin(); it != _h_dR_jets.end(); ++it) {
      scale(it->second, crossSection()/sumOfWeights());
    }

    // Fill inclusive jet multi ratio
    int Nbins = _h_jet_multi_inclusive->numBins();
    for (int i = 0; i < Nbins-1; ++i) {
      if (_h_jet_multi_inclusive->bin(i).area() > 0.0 && _h_jet_multi_inclusive->bin(i+1).area() > 0.0) {
        double ratio = _h_jet_multi_inclusive->bin(i+1).area()/_h_jet_multi_inclusive->bin(i).area();
        double relerr_i = _h_jet_multi_inclusive->bin(i).areaError()/_h_jet_multi_inclusive->bin(i).area();
        double relerr_j = _h_jet_multi_inclusive->bin(i+1).areaError()/_h_jet_multi_inclusive->bin(i+1).area();
        double err = ratio * (relerr_i + relerr_j);

	Point2D & pt = _h_jet_multi_ratio->point(i);
	pt.setY(ratio);
	pt.setYErr(err);
      }
    }

    scale(_h_jet_multi_exclusive, crossSection()/sumOfWeights());
    scale(_h_jet_multi_inclusive, crossSection()/sumOfWeights());
    scale(_h_jet_HT, crossSection()/sumOfWeights());
  }


}
