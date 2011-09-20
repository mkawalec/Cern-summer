#include "Rivet/Analysis.hh"
#include "Rivet/Projections/FinalState.hh"
#include "Rivet/Projections/ChargedLeptons.hh"
#include "Rivet/Projections/MissingMomentum.hh"
#include "Rivet/Projections/FastJets.hh"
#include "Rivet/AnalysisLoader.hh"
#include "Rivet/RivetAIDA.hh"

namespace Rivet {


  class MC_TTBAR : public Analysis {
  public:

    /// Minimal constructor
    MC_TTBAR() : Analysis("MC_TTBAR")
    {
      _sumwPassedLepJetMET = 0;
      _sumwPassedJetID = 0;
      _sumwPassedWMass = 0;
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
      _h_W_mass = bookHistogram1D("W_mass", 75, 30, 180);
      _h_t_mass = bookHistogram1D("t_mass", 150, 130, 430);
      _h_t_mass_W_cut = bookHistogram1D("t_mass_W_cut", 150, 130, 430);
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
      if (lfs.chargedLeptons().empty()) {
        MSG_DEBUG("Event failed lepton multiplicity cut");
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
      FourMomentum W(10*sqrtS(), 0, 0, 0);
      for (size_t i = 0; i < ljets.size()-1; ++i) {
        for (size_t j = i + 1; j < ljets.size(); ++j) {
          const FourMomentum Wcand = ljets[i].momentum() + ljets[j].momentum();
          MSG_TRACE(i << "," << j << ": candidate W mass = " << Wcand.mass()/GeV
                    << " GeV, vs. incumbent candidate with " << W.mass()/GeV << " GeV");
          if (fabs(Wcand.mass() - 80.4*GeV) < fabs(W.mass() - 80.4*GeV)) {
            W = Wcand;
          }
        }
      }
      MSG_DEBUG("Candidate W mass = " << W.mass() << " GeV");

      // There are two b-jets with which this can be combined to make the
      // hadronically decaying top, one of which is correct and the other is
      // not... but we have no way to identify which is which, so we construct
      // both possible top momenta and fill the histograms with both.
      const FourMomentum t1 = W + bjets[0].momentum();
      const FourMomentum t2 = W + bjets[1].momentum();
      _h_W_mass->fill(W.mass(), weight);
      _h_t_mass->fill(t1.mass(), weight);
      _h_t_mass->fill(t2.mass(), weight);

      // Placing a cut on the well-known W mass helps to reduce backgrounds
      if (inRange(W.mass()/GeV, 75, 85)) {
        MSG_DEBUG("W found with mass " << W.mass()/GeV << " GeV");
        _sumwPassedWMass += weight;
        _h_t_mass_W_cut->fill(t1.mass(), weight);
        _h_t_mass_W_cut->fill(t2.mass(), weight);
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
      scale(_h_W_mass, 1/_sumwPassedJetID);
      scale(_h_t_mass, 1/_sumwPassedJetID);
      scale(_h_t_mass_W_cut, 1/_sumwPassedWMass);
    }

    //@}


  private:

    // Passed-cuts counters
    double _sumwPassedLepJetMET, _sumwPassedJetID, _sumwPassedWMass;

    // @name Histogram data members
    //@{

    AIDA::IHistogram1D *_h_jet_1_pT, *_h_jet_2_pT, *_h_jet_3_pT, *_h_jet_4_pT;
    AIDA::IHistogram1D *_h_jet_HT;
    AIDA::IHistogram1D *_h_bjet_1_pT, *_h_bjet_2_pT;
    AIDA::IHistogram1D *_h_ljet_1_pT, *_h_ljet_2_pT;
    AIDA::IHistogram1D *_h_W_mass;
    AIDA::IHistogram1D *_h_t_mass, *_h_t_mass_W_cut;

    //@}

  };



  // The hook for the plugin system
  DECLARE_RIVET_PLUGIN(MC_TTBAR);

}
