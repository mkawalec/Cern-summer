// -*- C++ -*-
#include "Rivet/Analysis.hh"
#include "Rivet/Tools/Logging.hh"
#include "Rivet/Projections/FinalState.hh"
#include "Rivet/Projections/ZFinder.hh"
#include "Rivet/Projections/FastJets.hh"
#include "Rivet/RivetYODA.hh"

namespace Rivet {


  /// @brief D0 Z + jet + \f$ X \f$ cross-section / \f$ p_\perp \f$ distributions
  class D0_2009_S8202443 : public Analysis {
  public:

    /// @name Construction
    //@{
    /// Constructor
    D0_2009_S8202443() : Analysis("D0_2009_S8202443"),
        _sum_of_weights(0.0), _sum_of_weights_constrained(0.0)
    {
      setBeams(PROTON, ANTIPROTON);
    }

    //@}


    /// @name Analysis methods
    //@{

    /// Book histograms
    void init() {
      // Leptons in constrained tracking acceptance
      vector<pair<double, double> > etaRanges;
      etaRanges.push_back(make_pair(-2.5, -1.5));
      etaRanges.push_back(make_pair(-1.1, 1.1));
      etaRanges.push_back(make_pair(1.5, 2.5));
      ZFinder zfinder_constrained(etaRanges, 25.0*GeV, ELECTRON,
                                  65.0*GeV, 115.0*GeV, 0.2, true, true);
      addProjection(zfinder_constrained, "ZFinderConstrained");
      FastJets conefinder_constrained(zfinder_constrained.remainingFinalState(),
                                      FastJets::D0ILCONE, 0.5);
      addProjection(conefinder_constrained, "ConeFinderConstrained");

      // Unconstrained leptons
      ZFinder zfinder(-MAXRAPIDITY, MAXRAPIDITY, 0.0*GeV, ELECTRON,
                      65.0*GeV, 115.0*GeV, 0.2, true, true);
      addProjection(zfinder, "ZFinder");
      FastJets conefinder(zfinder.remainingFinalState(), FastJets::D0ILCONE, 0.5);
      addProjection(conefinder, "ConeFinder");

      _h_jet1_pT_constrained = bookHisto1D(1, 1, 1);
      _h_jet2_pT_constrained = bookHisto1D(3, 1, 1);
      _h_jet3_pT_constrained = bookHisto1D(5, 1, 1);
      _h_jet1_pT = bookHisto1D(2, 1, 1);
      _h_jet2_pT = bookHisto1D(4, 1, 1);
      _h_jet3_pT = bookHisto1D(6, 1, 1);
    }



    // Do the analysis
    void analyze(const Event& e) {
      double weight = e.weight();

      // unconstrained electrons first
      const ZFinder& zfinder = applyProjection<ZFinder>(e, "ZFinder");
      if (zfinder.particles().size()==1) {
        _sum_of_weights += weight;
        const JetAlg& jetpro = applyProjection<JetAlg>(e, "ConeFinder");
        const Jets& jets = jetpro.jetsByPt(20.0*GeV);
        Jets jets_cut;
        foreach (const Jet& j, jets) {
          if (fabs(j.momentum().pseudorapidity()) < 2.5) {
            jets_cut.push_back(j);
          }
        }

        if (jets_cut.size()>0) {
          _h_jet1_pT->fill(jets_cut[0].momentum().pT()/GeV, weight);
        }
        if (jets_cut.size()>1) {
          _h_jet2_pT->fill(jets_cut[1].momentum().pT()/GeV, weight);
        }
        if (jets_cut.size()>2) {
          _h_jet3_pT->fill(jets_cut[2].momentum().pT()/GeV, weight);
        }
      }
      else {
        getLog() << Log::DEBUG << "no unique lepton pair found." << endl;
      }


      // constrained electrons
      const ZFinder& zfinder_constrained = applyProjection<ZFinder>(e, "ZFinderConstrained");
      if (zfinder_constrained.particles().size()==1) {
        _sum_of_weights_constrained += weight;
        const JetAlg& jetpro = applyProjection<JetAlg>(e, "ConeFinderConstrained");
        const Jets& jets = jetpro.jetsByPt(20.0*GeV);
        Jets jets_cut;
        foreach (const Jet& j, jets) {
          if (fabs(j.momentum().pseudorapidity()) < 2.5) {
            jets_cut.push_back(j);
          }
        }

        if (jets_cut.size()>0) {
          _h_jet1_pT_constrained->fill(jets_cut[0].momentum().pT()/GeV, weight);
        }
        if (jets_cut.size()>1) {
          _h_jet2_pT_constrained->fill(jets_cut[1].momentum().pT()/GeV, weight);
        }
        if (jets_cut.size()>2) {
          _h_jet3_pT_constrained->fill(jets_cut[2].momentum().pT()/GeV, weight);
        }
      }
      else {
        getLog() << Log::DEBUG << "no unique lepton pair found." << endl;
        vetoEvent;
      }
    }



    // Finalize
    void finalize() {
      scale(_h_jet1_pT, 1.0/_sum_of_weights);
      scale(_h_jet2_pT, 1.0/_sum_of_weights);
      scale(_h_jet3_pT, 1.0/_sum_of_weights);
      scale(_h_jet1_pT_constrained, 1.0/_sum_of_weights_constrained);
      scale(_h_jet2_pT_constrained, 1.0/_sum_of_weights_constrained);
      scale(_h_jet3_pT_constrained, 1.0/_sum_of_weights_constrained);
    }

    //@}


  private:

    /// @name Histograms
    //@{
    Histo1DPtr _h_jet1_pT;
    Histo1DPtr _h_jet2_pT;
    Histo1DPtr _h_jet3_pT;
    Histo1DPtr _h_jet1_pT_constrained;
    Histo1DPtr _h_jet2_pT_constrained;
    Histo1DPtr _h_jet3_pT_constrained;
    //@}

    double _sum_of_weights, _sum_of_weights_constrained;

  };



  // This global object acts as a hook for the plugin system
  AnalysisBuilder<D0_2009_S8202443> plugin_D0_2009_S8202443;

}
