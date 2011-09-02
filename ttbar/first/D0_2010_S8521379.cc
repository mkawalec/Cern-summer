#include "Rivet/Analysis.hh"
#include "Rivet/Projections/FinalState.hh"
#include "Rivet/Projections/ChargedLeptons.hh"
#include "Rivet/Projections/MissingMomentum.hh"
#include "Rivet/Projections/HadronicFinalState.hh"
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

      addProjection(MissingMomentum(FinalState(-1.1, 1.1, 30*GeV)), "MM");

      addProjection(FastJets(FinalState(-5, 5, 0*GeV), FastJets::ANTIKT, 0.4), "Jets");

      _h_t_pT_W_cut = bookHistogram1D(2,1,1);
      _multiplicity = bookHistogram1D("multi", 10, 0, 10);
    }


    void analyze(const Event& event) {
      const double weight = event.weight();

      const ChargedLeptons& lfs = applyProjection<ChargedLeptons>(event, "LFS");

      const MissingMomentum& missmom = applyProjection<MissingMomentum>(event, "MM");

      const FastJets& jetpro = applyProjection<FastJets>(event, "Jets");

      MSG_DEBUG("Charged lepton multiplicity = " << lfs.chargedLeptons().size());

      // Not really needed, and should speed stuff up
      /*foreach (Particle lepton, lfs.chargedLeptons()) {
        MSG_DEBUG("Lepton pT = " << lepton.momentum().pT());
      }*/

      if (lfs.chargedLeptons().size() != 1) {
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
      _multiplicity->fill(ljets.size(), 1);

      if (bjets.size() != 2) {
        MSG_DEBUG("Event failed b-tagging cut");
        vetoEvent;
      }

      if (ljets.size() != 2) {
        MSG_DEBUG("Event failed l-tagging cut");
        vetoEvent;
      }

      const FourMomentum Whad = ljets[0].momentum() + ljets[1].momentum();
      const FourMomentum Wlep = missmom.visibleMomentum() + lfs.chargedLeptons().at(0).momentum();

      if (inRange(Whad.mass()/GeV, 70, 90) && inRange(Wlep.mass()/GeV, 70, 90)) {
      	MSG_INFO("hadronic W mass: " << Whad.mass()/GeV);
      	MSG_INFO("leptonic W mass: " << Wlep.mass()/GeV);
        const FourMomentum t1 = Whad + bjets[0].momentum();
        const FourMomentum t2 = Wlep + bjets[1].momentum();
        const FourMomentum t1bar = Wlep + bjets[1].momentum();
        const FourMomentum t2bar = Wlep + bjets[0].momentum();
      }
      else vetoEvent;
    }

    void finalize() {
      normalize(_h_t_pT_W_cut, 1/crossSection());
      //scale(_h_t_pT_W_cut,crossSection()/sumOfWeights());
      //scale(_h_t_pT_W_cut,crossSection());
    }
    //@}

  private:

    AIDA::IHistogram1D *_h_t_pT_W_cut;
    AIDA::IHistogram1D *_multiplicity;

  };


  // This global object acts as a hook for the plugin system
  AnalysisBuilder<D0_2010_S8521379> plugin_D0_2010_S8521379;

}
