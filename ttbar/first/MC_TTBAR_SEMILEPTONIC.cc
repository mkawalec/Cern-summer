#include "Rivet/Analysis.hh"
#include "Rivet/Projections/FinalState.hh"
#include "Rivet/Projections/WFinder.hh"
#include "Rivet/Projections/ChargedLeptons.hh"
#include "Rivet/Projections/MissingMomentum.hh"
#include "Rivet/Projections/FastJets.hh"
#include "Rivet/AnalysisLoader.hh"
#include "Rivet/RivetAIDA.hh"

namespace Rivet {


  class MC_TTBAR_SEMILEPTONIC : public Analysis {
  public:

    /// Minimal constructor
    MC_TTBAR_SEMILEPTONIC() : Analysis("MC_TTBAR_SEMILEPTONIC")
    {
      _sumwPassedLepJetMET = 0;
      _sumwPassedJetID = 0;
      _sumwPassedWMass = 0;
      _sumwPassedLepW = 0;
    }


    /// @name Analysis methods
    //@{

    /// Set up projections and book histograms
    void init() {

      // A FinalState is used to select particles within |eta| < 4.2 and with pT
      // > 30 GeV, out of which the ChargedLeptons projection picks only the
      // electrons and muons, to be accessed later as "LFS".
      addProjection(ChargedLeptons(FinalState(-4.2, 4.2, 30*GeV)), "LFS");
      // A second FinalState is used to select all particles in |eta| < 4.2,
      // with no pT cut. This is used to construct jets and measure missing
      // transverse energy.
      FinalState fs(-4.2, 4.2, 0*GeV);

      addProjection(FastJets(fs, FastJets::ANTIKT, 0.6), "Jets");
      addProjection(MissingMomentum(fs), "MissingET");
      addProjection(WFinder(-3.5, 3.5, 25.0*GeV, ELECTRON, 60.0*GeV,
            100.0*GeV, 20.0*GeV, 0.2), "W_e");
      addProjection(WFinder(-3.5, 3.5, 25.0*GeV, MUON, 60.0*GeV,
            100.0*GeV, 20.0*GeV, 0.2), "W_mu");

      // Booking of histograms
      _h_jet_1_pT = bookHistogram1D("jet_1_pT", 50, 0, 500);
      _h_jet_2_pT = bookHistogram1D("jet_2_pT", 50, 0, 400);
      _h_jet_3_pT = bookHistogram1D("jet_3_pT", 50, 0, 300);
      _h_jet_4_pT = bookHistogram1D("jet_4_pT", 50, 0, 200);
      _h_jet_HT   = bookHistogram1D("jet_HT", logspace(0.01, 2000, 50));
      //
      _h_bjet_1_pT = bookHistogram1D("jetb_1_pT", 50, 0, 400);
      _h_bjet_2_pT = bookHistogram1D("jetb_2_pT", 50, 0, 300);
      //
      _h_ljet_1_pT = bookHistogram1D("jetl_1_pT", 50, 0, 400);
      _h_ljet_2_pT = bookHistogram1D("jetl_2_pT", 50, 0, 300);
      //
      _h_hadronic_W_mass = bookHistogram1D("hadronic_W_mass", 75, 30, 180);
      _h_leptonic_W_mass = bookHistogram1D("leptonic_W_mass", 75, 30, 180);
      _h_t_mass = bookHistogram1D("t_mass", 150, 130, 430);
      _h_t_mass_W_cut = bookHistogram1D("t_mass_W_cut", 150, 130, 430);
      _h_t_pT_W_cut = bookHistogram1D("t_pT_W_cut", 150, 130, 430);
    }


    void analyze(const Event& event) {
      const double weight = event.weight();

      // Use the "LFS" projection to require at least one hard charged
      // lepton. This is an experimental signature for the leptonically decaying
      // W. This helps to reduce pure QCD backgrounds.
      const ChargedLeptons& lfs = applyProjection<ChargedLeptons>(event, "LFS");
      MSG_DEBUG("Charged lepton multiplicity = " << lfs.chargedLeptons().size());
      foreach (const Particle& lepton, lfs.chargedLeptons()) {
        MSG_DEBUG("Lepton pT = " << lepton.momentum().pT());
      }
      if (lfs.chargedLeptons().size() < 1) {
        MSG_DEBUG("Event failed charged lepton multiplicity cut");
        vetoEvent;
      }


      // Use a missing ET cut to bias toward events with a hard neutrino from
      // the leptonically decaying W. This helps to reduce pure QCD backgrounds.
      const MissingMomentum& met = applyProjection<MissingMomentum>(event, "MissingET");
      MSG_DEBUG("Vector ET = " << met.vectorEt().mod() << " GeV");
      if (met.vectorEt().mod() < 30*GeV) {
        MSG_DEBUG("Event failed missing ET cut");
        vetoEvent;
      }

      const PdgId lepId = abs(lfs.chargedLeptons().front().pdgId());

      // Reconstruct the leptonically decaying W from charged lepton and 
      const WFinder& wfinder = applyProjection<WFinder>
                        (event, (lepId == MUON) ? "W_mu" : "W_e" );

      if(wfinder.bosons().size() != 1) {
        MSG_DEBUG("No leptonic W found");
        vetoEvent;
      }

      const FourMomentum leptonic_W = wfinder.bosons().front().momentum();

      _h_leptonic_W_mass->fill(leptonic_W.mass(), weight);
      _sumwPassedLepW += weight;

      // Use the "Jets" projection to check that there are at least 4 jets of
      // any pT. Getting the jets sorted by pT ensures that the first jet is the
      // hardest, and so on. We apply no pT cut here only because we want to
      // plot all jet pTs to help optimise our jet pT cut.
      const FastJets& jetpro = applyProjection<FastJets>(event, "Jets");
      const Jets alljets = jetpro.jetsByPt();
      if (alljets.size() < 4) {
        MSG_DEBUG("Event failed jet multiplicity cut");
        vetoEvent;
      }

      // Update passed-cuts counter and fill all-jets histograms
      _sumwPassedLepJetMET += weight;
      _h_jet_1_pT->fill(alljets[0].momentum().pT()/GeV, weight);
      _h_jet_2_pT->fill(alljets[1].momentum().pT()/GeV, weight);
      _h_jet_3_pT->fill(alljets[2].momentum().pT()/GeV, weight);
      _h_jet_4_pT->fill(alljets[3].momentum().pT()/GeV, weight);

      // Insist that the hardest 4 jets pass pT hardness cuts. If we don't find
      // at least 4 such jets, we abandon this event.
      const Jets jets = jetpro.jetsByPt(30*GeV);
      double ht = 0.0;
      foreach (const Jet& j, jets) { ht += j.momentum().pT(); }
      _h_jet_HT->fill(ht/GeV, weight);
      if (jets.size() < 4 ||
          jets[0].momentum().pT() < 60*GeV ||
          jets[1].momentum().pT() < 50*GeV ||
          jets[3].momentum().pT() < 30*GeV) {
        MSG_DEBUG("Event failed jet cuts");
        vetoEvent;
      }

      // Sort the jets into b-jets and light jets. We expect one hard b-jet from
      // each top decay, so our 4 hardest jets should include two b-jets. The
      // Jet::containsBottom() method is equivalent to perfect experimental
      // b-tagging, in a generator-independent way.
      Jets bjets, ljets;
      foreach (const Jet& jet, jets) {
        // // Don't count jets that overlap with the hard leptons
        bool isolated = true;
        foreach (const Particle& lepton, lfs.chargedLeptons()) {
          if (deltaR(jet.momentum(), lepton.momentum()) < 0.3) {
            isolated = false;
            break;
          }
        }
        if (!isolated) {
          MSG_DEBUG("Jet failed lepton isolation cut");
          break;
        }
        if (jet.containsBottom()) {
          bjets.push_back(jet);
        } else {
          ljets.push_back(jet);
        }
      }
      MSG_DEBUG("Number of b-jets = " << bjets.size());
      if (bjets.size() != 2) {
        MSG_DEBUG("Event failed post-lepton-isolation b-tagging cut");
        vetoEvent;
      }
      if (ljets.size() < 2) {
        MSG_DEBUG("Event failed since not enough light jets remaining after lepton-isolation");
        vetoEvent;
      }

      // Plot the pTs of the identified jets.
      _sumwPassedJetID += weight;
      _h_bjet_1_pT->fill(bjets[0].momentum().pT(), weight);
      _h_bjet_2_pT->fill(bjets[1].momentum().pT(), weight);
      _h_ljet_1_pT->fill(ljets[0].momentum().pT(), weight);
      _h_ljet_2_pT->fill(ljets[1].momentum().pT(), weight);

      // Construct the hadronically decaying W momentum 4-vector from pairs of
      // non-b-tagged jets. The pair which best matches the W mass is used. We start
      // with an always terrible 4-vector estimate which should always be "beaten" by
      // a real jet pair.
      FourMomentum hadronic_W(10*sqrtS(), 0, 0, 0);
      for (size_t i = 0; i < ljets.size()-1; ++i) {
        for (size_t j = i + 1; j < ljets.size(); ++j) {
          const FourMomentum Wcand = ljets[i].momentum() + ljets[j].momentum();
          MSG_TRACE(i << "," << j << ": candidate W mass = " << Wcand.mass()/GeV
                    << " GeV, vs. incumbent candidate with " << hadronic_W.mass()/GeV << " GeV");
          if (fabs(Wcand.mass() - 80.4*GeV) < fabs(hadronic_W.mass() - 80.4*GeV)) {
            hadronic_W = Wcand;
          }
        }
      }
      MSG_DEBUG("Candidate hadronic W mass = " << hadronic_W.mass() << " GeV");
      _h_hadronic_W_mass->fill(hadronic_W.mass(), weight);

      
      // We don't know if which b-tagged jet to combine each W with. We
      // choose the combinations which minimises the difference between the
      // masses of the reconstructed t,tbar pair.
      Ttbar ttb1 = Ttbar(leptonic_W + bjets[0].momentum(),
                         hadronic_W + bjets[1].momentum());
      Ttbar ttb2 = Ttbar(leptonic_W + bjets[1].momentum(),
                         hadronic_W + bjets[0].momentum());
      Ttbar ttbar = (_massdiff(ttb1) < _massdiff(ttb2)) ? ttb1 : ttb2;

      _h_t_mass->fill(ttbar.first.mass(), weight);
      _h_t_mass->fill(ttbar.second.mass(), weight);

      // Placing a cut on the well-known W mass helps to reduce backgrounds
      if (inRange(hadronic_W.mass()/GeV, 75, 85) && inRange(leptonic_W.mass()/GeV, 75, 85)) {
        MSG_DEBUG("Hadronic W found with mass " << hadronic_W.mass()/GeV << " GeV");
        MSG_DEBUG("Leptonic W found with mass " << leptonic_W.mass()/GeV << " GeV");
        _sumwPassedWMass += weight;
        _h_t_mass_W_cut->fill(ttbar.first.mass(), weight);
        _h_t_mass_W_cut->fill(ttbar.second.mass(), weight);
      }

    }

    void finalize() {
      scale(_h_jet_1_pT, 1/_sumwPassedLepJetMET);
      scale(_h_jet_2_pT, 1/_sumwPassedLepJetMET);
      scale(_h_jet_3_pT, 1/_sumwPassedLepJetMET);
      scale(_h_jet_4_pT, 1/_sumwPassedLepJetMET);
      scale(_h_jet_HT, 1/_sumwPassedLepJetMET);
      scale(_h_bjet_1_pT, 1/_sumwPassedJetID);
      scale(_h_bjet_2_pT, 1/_sumwPassedJetID);
      scale(_h_ljet_1_pT, 1/_sumwPassedJetID);
      scale(_h_ljet_2_pT, 1/_sumwPassedJetID);
      scale(_h_hadronic_W_mass, 1/_sumwPassedJetID);
      scale(_h_leptonic_W_mass, 1/_sumwPassedLepW);
      scale(_h_t_mass, 1/_sumwPassedJetID);
      scale(_h_t_mass_W_cut, 1/_sumwPassedJetID);
      scale(_h_t_pT_W_cut, 1/_sumwPassedJetID);
    }

    //@}


  private:

    // For operating on mass differences of top combinations
    typedef std::pair<FourMomentum, FourMomentum> Ttbar;

    inline double _massdiff(Ttbar& ttb) {
      return abs(ttb.first.mass() - ttb.second.mass());
    }
    // Passed-cuts counters
    double _sumwPassedLepJetMET, _sumwPassedJetID, _sumwPassedWMass, _sumwPassedLepW;

    // @name Histogram data members
    //@{

    AIDA::IHistogram1D *_h_jet_1_pT, *_h_jet_2_pT, *_h_jet_3_pT, *_h_jet_4_pT;
    AIDA::IHistogram1D *_h_jet_HT;
    AIDA::IHistogram1D *_h_bjet_1_pT, *_h_bjet_2_pT;
    AIDA::IHistogram1D *_h_ljet_1_pT, *_h_ljet_2_pT;
    AIDA::IHistogram1D *_h_leptonic_W_mass, *_h_hadronic_W_mass;
    AIDA::IHistogram1D *_h_t_mass, *_h_t_mass_W_cut;
    AIDA::IHistogram1D *_h_t_pT_W_cut;

    //@}

  };



  // The hook for the plugin system
  DECLARE_RIVET_PLUGIN(MC_TTBAR_SEMILEPTONIC);

}
