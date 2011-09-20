#include "Rivet/Analysis.hh"
#include "Rivet/Projections/FinalState.hh"
#include "Rivet/Projections/ChargedLeptons.hh"
#include "Rivet/Projections/WFinder.hh"
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

        FinalState fs = FinalState(-5, 5, 0*GeV);
        addProjection(ChargedLeptons(fs), "LFS"); 
        addProjection(FastJets(fs, FastJets::ANTIKT, 0.4), "Jets");

        // Separated Electron and Muon Wfinder projections
        addProjection(WFinder(-3.5, 3.5, 25.0*GeV, ELECTRON, 60.0*GeV,
              100.0*GeV, 20.0*GeV, 0.2), "WE");
        addProjection(WFinder(-3.5, 3.5, 25.0*GeV, MUON, 60.0*GeV,
              100.0*GeV, 25.0*GeV, 0.2), "WMU");

        _h_t_pT_W_cut = bookHistogram1D(2,1,1);
      }

      void analyze(const Event& event) {
        const double weight = event.weight();

        // Ensure that there is only one charged lepton in the event
        const ChargedLeptons& lfs = applyProjection<ChargedLeptons>(event, "LFS");

        if (lfs.chargedLeptons().size() != 1) {
          MSG_DEBUG("Event failed charged lepton multiplicity cut");
          vetoEvent;
        }

        // Find the leptonically decaying W. @todo: find a better way to do this
        // branching.

        const Particle& lepton = lfs.chargedLeptons().at(0);
        const WFinder& wfinder = (abs(lepton.pdgId()) == MUON) ? 
          applyProjection<WFinder>(event, "WMU") : 
          applyProjection<WFinder>(event, "WE") ;

        if (wfinder.bosons().size() < 1) {
          MSG_DEBUG("Event failed charged lepton cuts");
          vetoEvent;
        }

        // Apply the lepton rapiditiy cuts.
        const double maxEta = (abs(lepton.pdgId() == MUON)) ? 2.0 : 1.1;
        if (abs(lepton.momentum().eta()) >= maxEta) {
          MSG_DEBUG("Charged lepton failed rapidity cut");
          vetoEvent;
        }

        // Run the jet finder, 

        const FastJets& jetpro = applyProjection<FastJets>(event, "Jets");
        const Jets jets = jetpro.jetsByPt(20*GeV, MAXDOUBLE, -2.5, 2.5);

        foreach (const Jet& jet, jets) {
          MSG_DEBUG("Jet pT = " << jet.momentum().pT()/GeV << " GeV");
        }

        if (jets.size() < 4) {
          MSG_DEBUG("Event failed jet pT cut");
          vetoEvent;
        }

        if (jets[0].momentum().pT() <= 40*GeV) {
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

        if (bjets.size() != 2) {
          MSG_DEBUG("Event failed b-tagging cut");
          vetoEvent;
        }

        const FourMomentum had_W = ljets[0].momentum() + ljets[1].momentum();
        const FourMomentum lep_W = wfinder.bosons().front().momentum();

        if (inRange(lep_W.mass()/GeV, 70, 90) && inRange(had_W.mass()/GeV, 70, 90)) {
          MSG_INFO("hadronic W mass: " << had_W.mass()/GeV);
          MSG_INFO("leptonic W mass: " << lep_W.mass()/GeV);

          // We don't know if which b-tagged jet to combine each W with. We
          // choose the combinations which minimises the difference between the
          // masses of the reconstructed t,tbar pair.
          ttbar ttb1 = ttbar(lep_W + bjets[0].momentum(), had_W + bjets[1].momentum());
          ttbar ttb2 = ttbar(lep_W + bjets[1].momentum(), had_W + bjets[0].momentum());

          // Choose the t,tbar pair that minimises the mass difference
          ttbar ttb = (_massdiff(ttb1) < _massdiff(ttb2)) ? ttb1 : ttb2;

          _h_t_pT_W_cut->fill(ttb.first.pT(), weight);
          _h_t_pT_W_cut->fill(ttb.second.pT(), weight);
        }
        else vetoEvent;
      }

      void finalize() {
        scale(_h_t_pT_W_cut, crossSection()/sumOfWeights());
      }
      //@}

    private:

      typedef std::pair<FourMomentum, FourMomentum> ttbar;

      double _massdiff(ttbar ttb) {
        return abs(ttb.first.mass() - ttb.second.mass());
      }

      AIDA::IHistogram1D *_h_t_pT_W_cut;

  };

  // This global object acts as a hook for the plugin system
  AnalysisBuilder<D0_2010_S8521379> plugin_D0_2010_S8521379;
}
