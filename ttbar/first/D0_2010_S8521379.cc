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
      addProjection(ChargedLeptons(FinalState(-2.0, 2.0, 20*GeV)), "LFS");
      addProjection(FastJets(FinalState(-4.2, 4.2, 0*GeV), FastJets::ANTIKT, 0.4), "Jets");

      _h_t_mass_W_cut = bookHistogram1D("t_mass_W_cut", 26, 100, 400);
      _h_t_pT_W_cut = bookHistogram1D("t_pT_W_cut", 8, 0, 400);
    }


    void analyze(const Event& event) {
      const double weight = event.weight();

      const ChargedLeptons& lfs = applyProjection<ChargedLeptons>(event, "LFS");
      MSG_DEBUG("Charged lepton multiplicity = " << lfs.chargedLeptons().size());

      foreach (Particle lepton, lfs.chargedLeptons()) {
        MSG_DEBUG("Lepton pT = " << lepton.momentum().pT());
      }

      // Would be very nice to find a way to make this bit work!
      if (lfs.chargedLeptons().size() != 1) {
        MSG_DEBUG("Event failed lepton multiplicity cut");
        vetoEvent;
      }

      const Jets jets = jetpro.jetsByPt(20*GeV);
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
      FourMomentum W()
      foreach (const Jet& jet, jets) {
        if (jet.containsBottom()) {
          bjets.push_back(jet);
        } else {
	  W += jet.momentum()
          ljets.push_back(jet);
        }
      }
      const FourMomentum W = W;

      MSG_DEBUG("Number of b-jets = " << bjets.size());
      if (bjets.size() < 1) {
        MSG_DEBUG("Event failed b-tagging cut");
        vetoEvent;
      }

      // Really need to think about this... How are they reconstructing with variable number of b quarks?
      if (inRange(W.pseudorapidity()/GeV, -1.1, 1.1)) {
        MSG_DEBUG("W found with mass " << W.mass()/GeV << " GeV");
	foreach (const Jet& jet, jets) {
        const FourMomentum t1 = W + bjets[0].momentum();
        const FourMomentum t2 = W + bjets[1].momentum();
        _h_t_mass_W_cut->fill(t1.mass(), weight);
        _h_t_mass_W_cut->fill(t2.mass(), weight);
	_h_t_pT_W_cut->fill(t1.pT(), weight);
	_h_t_pT_W_cut->fill(t2.pT(), weight);
      }
      else {
        vetoEvent;
      }

      /// @todo Add reconstruction of the other top from the leptonically decaying W, using WFinder
    }

    void finalize() {
      // No histos, so nothing to do!
      scale(_h_t_pT_W_cut, crossSection()/sumOfWeights());
      scale(_h_t_mass_W_cut, crossSection()/sumOfWeights());
    }

    //@}

  private:

    AIDA::IHistogram1D *_h_t_mass_W_cut;
    AIDA::IHistogram1D *_h_t_pT_W_cut;

  };


  // This global object acts as a hook for the plugin system
  AnalysisBuilder<D0_2010_S8521379> plugin_D0_2010_S8521379;

}
