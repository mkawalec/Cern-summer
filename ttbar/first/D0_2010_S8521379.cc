#include "Rivet/Analysis.hh"
#include "Rivet/Projections/FinalState.hh"
#include "Rivet/Projections/ChargedLeptons.hh"
#include "Rivet/Projections/FastJets.hh"
#include "Rivet/AnalysisLoader.hh"
#include "Rivet/RivetAIDA.hh"


namespace Rivet {

  class D0_2010_S8521379 : public Analysis {

  public:

    D0_2010_S8521379()
      : Analysis("D0_2010_S8521379")
    {   
      setNeedsCrossSection(true);
    } 

    /// @name Analysis methods
    //@{

    void init() {
      addProjection(ChargedLeptons(FinalState(-1.1, 1.1, 30*GeV)), "LFS");
      addProjection(FastJets(FinalState(-5, 5, 0*GeV), FastJets::ANTIKT, 0.4), "Jets");

      _h_t_pT_W_cut = bookHistogram1D(2,1,1);
    }


    void analyze(const Event& event) {
      const double weight = event.weight();

      const ChargedLeptons& lfs = applyProjection<ChargedLeptons>(event, "LFS");

      const FastJets& jetpro = applyProjection<FastJets>(event, "Jets");

      MSG_DEBUG("Charged lepton multiplicity = " << lfs.chargedLeptons().size());

      // Not really needed, and should speed stuff up
      /*foreach (Particle lepton, lfs.chargedLeptons()) {
        MSG_DEBUG("Lepton pT = " << lepton.momentum().pT());
      }*/

      // Would be very nice to find a way to make this bit work!
      if (lfs.chargedLeptons().empty()) {
        MSG_DEBUG("Event failed lepton multiplicity cut");
        vetoEvent;
      }

      const Jets jets = jetpro.jetsByPt(20*GeV, MAXDOUBLE, -2.5, 2.5);
      foreach (const Jet& jet, jets) {
        MSG_DEBUG("Jet pT = " << jet.momentum().pT()/GeV << " GeV");
      }

      if (jets.size() < 4) {
        MSG_DEBUG("Event failed jet pT cut");
        vetoEvent;
      }

      if (jets[0].momentum().pT() <= 40) {
        MSG_DEBUG("Event failed leading jet pT cut");
	      vetoEvent;
      }

      Jets bjets, ljets;
      foreach (const Jet& jet, jets) {
        if (jet.containsBottom()) {
          bjets.push_back(jet);
        } else {
          ljets.push_back(jet);
        }
      }

      MSG_DEBUG("Number of b-jets = " << bjets.size());
      if (bjets.size() < 1) {
        MSG_DEBUG("Event failed b-tagging cut");
        vetoEvent;
      }

      MSG_DEBUG("Number of l-jets = " << ljets.size());
      if (ljets.size() != 2) {
        MSG_DEBUG("Event failed l-tagging cut");
        vetoEvent;
      }

      const FourMomentum W  = ljets[0].momentum() + ljets[1].momentum();

      if (W.Et() > 20*GeV) {
        MSG_DEBUG("W found with mass " << W.mass()/GeV << " GeV");
        const FourMomentum t = W + bjets[0].momentum();
        std::cout << "Found W! t_pT = "<< t.pT() << ", weight= "<< weight  << endl;
	      _h_t_pT_W_cut->fill(t.pT(), weight);
      }
      else {
        vetoEvent;
      }

      /// @todo Add reconstruction of the other top from the leptonically decaying W, using WFinder
    }

    void finalize() {
      scale(_h_t_pT_W_cut,crossSection()/sumOfWeights());
    }

    //@}

  private:

    AIDA::IHistogram1D *_h_t_pT_W_cut;

  };


  // This global object acts as a hook for the plugin system
  AnalysisBuilder<D0_2010_S8521379> plugin_D0_2010_S8521379;

}
