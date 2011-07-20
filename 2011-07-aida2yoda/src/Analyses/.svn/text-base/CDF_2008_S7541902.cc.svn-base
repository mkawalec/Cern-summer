// -*- C++ -*-
#include "Rivet/Analysis.hh"
#include "Rivet/RivetYODA.hh"
#include "Rivet/Tools/Logging.hh"
#include "Rivet/Tools/ParticleIdUtils.hh"
#include "Rivet/Projections/FinalState.hh"
#include "Rivet/Projections/VetoedFinalState.hh"
#include "Rivet/Projections/InvMassFinalState.hh"
#include "Rivet/Projections/FastJets.hh"
#include <algorithm>

namespace Rivet {


  /// @brief CDF jet pT and multiplicity distributions in W + jets events
  ///
  /// This CDF analysis provides jet pT distributions for 4 jet multiplicity bins
  /// as well as the jet multiplicity distribution in W + jets events.
  /// e-Print: arXiv:0711.4044 [hep-ex]
  class CDF_2008_S7541902 : public Analysis {
  public:

    /// Constructor
    CDF_2008_S7541902()
      : Analysis("CDF_2008_S7541902"),
        _electronETCut(20.0*GeV), _electronETACut(1.1),
        _eTmissCut(30.0*GeV), _mTCut(20.0*GeV),
        _jetEtCutA(20.0*GeV),  _jetEtCutB(25.0*GeV), _jetETA(2.0),
        _xpoint(1960.)
    {
      setBeams(PROTON, ANTIPROTON);
      setNeedsCrossSection(true);
    }


    /// @name Analysis methods
    //@{
 
    void init() {
      // Set up projections
      // Basic FS
      FinalState fs(-3.6, 3.6);
      addProjection(fs, "FS");
   
      // Create a final state with any e-nu pair with invariant mass 65 -> 95 GeV and ET > 20 (W decay products)
      vector<pair<PdgId,PdgId> > vids;
      vids += make_pair(ELECTRON, NU_EBAR);
      vids += make_pair(POSITRON, NU_E);
      FinalState fs2(-3.6, 3.6, 20*GeV);
      InvMassFinalState invfs(fs2, vids, 65*GeV, 95*GeV);
      addProjection(invfs, "INVFS");
   
      // Make a final state without the W decay products for jet clustering
      VetoedFinalState vfs(fs);
      vfs.addVetoOnThisFinalState(invfs);
      addProjection(vfs, "VFS");
      addProjection(FastJets(vfs, FastJets::CDFJETCLU, 0.4), "Jets");

      // Book histograms
      for (int i = 0 ; i < 4 ; ++i) {
        _histJetEt[i] = bookHisto1D(i+1, 1, 1);
        _histJetMultRatio[i] = bookScatter2D(5 , 1, i+1);
        _histJetMult[i]   = bookHisto1D(i+6, 1, 1);
      }
      _histJetMultNorm = bookHisto1D("norm", 1, _xpoint, _xpoint+1.);
    }
 

    /// Do the analysis
    void analyze(const Event& event) {
      // Get the W decay products (electron and neutrino)
      const InvMassFinalState& invMassFinalState = applyProjection<InvMassFinalState>(event, "INVFS");
      const ParticleVector&  wDecayProducts = invMassFinalState.particles();
   
      FourMomentum electronP, neutrinoP;
      bool gotElectron(false), gotNeutrino(false);
      foreach (const Particle& p, wDecayProducts) {
        FourMomentum p4 = p.momentum();
        if (p4.Et() > _electronETCut && fabs(p4.eta()) < _electronETACut && abs(p.pdgId()) == ELECTRON) {
          electronP = p4;
          gotElectron = true;
        }
        else if (p4.Et() > _eTmissCut && abs(p.pdgId()) == NU_E) {
          neutrinoP = p4;
          gotNeutrino = true;
        }
      }
   
      // Veto event if the electron or MET cuts fail
      if (!gotElectron || !gotNeutrino) vetoEvent;
   
      // Veto event if the MTR cut fails
      double mT2 = 2.0 * ( electronP.pT()*neutrinoP.pT() - electronP.px()*neutrinoP.px() - electronP.py()*neutrinoP.py() );
      if (sqrt(mT2) < _mTCut ) vetoEvent;
   
      // Get the jets
      const JetAlg& jetProj = applyProjection<FastJets>(event, "Jets");
      Jets theJets = jetProj.jetsByEt(_jetEtCutA);
      size_t njetsA(0), njetsB(0);
      foreach (const Jet& j, theJets) {
        const FourMomentum pj = j.momentum();
        if (fabs(pj.rapidity()) < _jetETA) {
          // Fill differential histograms for top 4 jets with Et > 20
          if (njetsA < 4 && pj.Et() > _jetEtCutA) {
            ++njetsA;
            _histJetEt[njetsA-1]->fill(pj.Et(), event.weight());
          }
          // Count number of jets with Et > 25 (for multiplicity histograms)
          if (pj.Et() > _jetEtCutB) ++njetsB;
        }
      }
   
      // Jet multiplicity
      _histJetMultNorm->fill(_xpoint, event.weight());
      for (size_t i = 1; i <= njetsB; ++i) {
        _histJetMult[i-1]->fill(_xpoint, event.weight());
        if (i == 4) break;
      }
    }
 
 

    /// Finalize
    void finalize() {
      const double xsec = crossSection()/sumOfWeights();
      // Get the x-axis for the ratio plots
      /// @todo YODA Replace with autobooking etc. once YODA in place
      // std::vector<double> xval; xval.push_back(_xpoint);
      // std::vector<double> xerr; xerr.push_back(.5);
      // // Fill the first ratio histogram using the special normalisation histogram for the total cross section
      // double ratio1to0 = 0.;
      // if (_histJetMultNorm->bin(0).area() > 0.) ratio1to0 = _histJetMult[0]->bin(0).area()/_histJetMultNorm->bin(0).area();
      // // Get the fractional error on the ratio histogram
      // double frac_err1to0 = 0.;
      // if (_histJetMult[0]->bin(0).area() > 0.)  frac_err1to0 = _histJetMult[0]->bin(0).areaError()/_histJetMult[0]->bin(0).area();
      // if (_histJetMultNorm->bin(0).area() > 0.) {
      //   frac_err1to0 *= frac_err1to0;
      //   frac_err1to0 += pow(_histJetMultNorm->bin(0).areaError()/_histJetMultNorm->bin(0).area(),2.);
      //   frac_err1to0 = sqrt(frac_err1to0);
      // }
   
      // /// @todo Replace with autobooking etc. once YODA in place
      // vector<double> yval[4]; yval[0].push_back(ratio1to0);
      // vector<double> yerr[4]; yerr[0].push_back(ratio1to0*frac_err1to0);
      // _histJetMultRatio[0]->setCoordinate(0,xval,xerr);
      // _histJetMultRatio[0]->setCoordinate(1,yval[0],yerr[0]);
      // for (int i = 0; i < 4; ++i) {
      //   if (i < 3) {
      //     float ratio = 0.0;
      //     if (_histJetMult[i]->bin(0).area() > 0.0) ratio = _histJetMult[i+1]->bin(0).area()/_histJetMult[i]->bin(0).area();
      //     float frac_err = 0.0;
      //     if (_histJetMult[i]->bin(0).area() > 0.0) frac_err = _histJetMult[i]->binError(0)/_histJetMult[i]->bin(0).area();
      //     if (_histJetMult[i+1]->bin(0).area() > 0.0) {
      //       frac_err *= frac_err;
      //       frac_err += pow(_histJetMult[i+1]->binError(0)/_histJetMult[i+1]->bin(0).area(),2.);
      //       frac_err = sqrt(frac_err);
      //     }
      //     yval[i+1].push_back(ratio);
      //     yerr[i+1].push_back(ratio*frac_err);
      //     _histJetMultRatio[i+1]->setCoordinate(0,xval,xerr);
      //     _histJetMultRatio[i+1]->setCoordinate(1,yval[i+1],yerr[i+1]);
      //   }
      //   _histJetEt[i]->scale(xsec);
      //   _histJetMult[i]->scale(xsec);
      // }
      // _histJetMultNorm->scale(xsec);
    }

    //@}


  private:

    /// @name Cuts
    //@{
    /// Cut on the electron ET:
    double _electronETCut;
    /// Cut on the electron ETA:
    double _electronETACut;
    /// Cut on the missing ET
    double _eTmissCut;
    /// Cut on the transverse mass squared
    double _mTCut;
    /// Cut on the jet ET for differential cross sections
    double _jetEtCutA;
    /// Cut on the jet ET for jet multiplicity
    double _jetEtCutB;
    /// Cut on the jet ETA
    double _jetETA;
    //@}

    double _xpoint;

    /// @name Histograms
    //@{
    Histo1DPtr _histJetEt[4];
    Histo1DPtr _histJetMultNorm;
    Scatter2DPtr _histJetMultRatio[4];
    Histo1DPtr _histJetMult[4];
    //@}

  };


  // This global object acts as a hook for the plugin system
  AnalysisBuilder<CDF_2008_S7541902> plugin_CDF_2008_S7541902;

}
