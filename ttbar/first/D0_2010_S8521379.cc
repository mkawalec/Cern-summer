#include "Rivet/Analysis.hh"
#include "Rivet/Projections/FinalState.hh"
#include "Rivet/Projections/ChargedLeptons.hh"
#include "Rivet/Projections/MissingMomentum.hh"
#include "Rivet/Projections/WFinder.hh"
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

        FinalState fs = FinalState(-5, 5, 0*GeV);

        addProjection(ChargedLeptons(fs), "LFS"); 
      	addProjection(WFinder(-3.5, 3.5, 25.0*GeV, ELECTRON, 60.0*GeV, 100.0*GeV, 20.0*GeV, 0.2), "WE");
      	addProjection(WFinder(-3.5, 3.5, 25.0*GeV, MUON, 60.0*GeV, 100.0*GeV, 25.0*GeV, 0.2), "WMU");
        addProjection(MissingMomentum(FinalState(fs)), "MM");
        addProjection(FastJets(fs, FastJets::ANTIKT, 0.4), "Jets");

        _h_t_pT_W_cut = bookHistogram1D(2,1,1);
      }

      void analyze(const Event& event) {
        const double weight = event.weight();

        const ChargedLeptons& lfs = applyProjection<ChargedLeptons>(event, "LFS");
        const MissingMomentum& missmom = applyProjection<MissingMomentum>(event, "MM");
        const FastJets& jetpro = applyProjection<FastJets>(event, "Jets");


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

        const Particle& lepton = lfs.chargedLeptons().at(0);
        const FourMomentum misslmom = missmom.visibleMomentum();

        const WFinder& wfinder = (abs(lepton.pdgId()) == MUON) ? 
          applyProjection<WFinder>(event, "WMU") : 
          applyProjection<WFinder>(event, "WE") ;

        if (wfinder.bosons().size() != 1) {
          vetoEvent;
        }

        FourMomentum Wlep(wfinder.bosons().front().momentum());

        if (abs(lepton.pdgId()) == MUON) {
          if (abs(lepton.momentum().eta()) >= 2.0) {
            MSG_DEBUG("Muon failed rapidity cut");
            vetoEvent;
          }
        }
        else if (abs(lepton.pdgId()) == ELECTRON) {
          if (abs(lepton.momentum().eta()) >= 1.1) {
            MSG_DEBUG("Electron failed rapidity cut");
            vetoEvent;
          }
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

        if (ljets.size() != 2) {
          MSG_DEBUG("Event failed l-tagging cut");
          vetoEvent;
        }


        const FourMomentum Whad = ljets[0].momentum() + ljets[1].momentum();

        if (inRange(Whad.mass()/GeV, 70, 90) && inRange(Wlep.mass()/GeV, 70, 90)) {
          MSG_INFO("hadronic W mass: " << Whad.mass()/GeV);
          MSG_INFO("leptonic W mass: " << Wlep.mass()/GeV);
          const FourMomentum t1 = Whad + bjets[0].momentum();
          const FourMomentum t2 = Wlep + bjets[1].momentum();
          const FourMomentum t1bar = Wlep + bjets[1].momentum();
          const FourMomentum t2bar = Wlep + bjets[0].momentum();

          // Consider combinatorics of t,tbar configurations
          const double c11 = fabs(t1.mass() - t1bar.mass());
          const double c12 = fabs(t1.mass() - t2bar.mass());
          const double c21 = fabs(t2.mass() - t1bar.mass());
          const double c22 = fabs(t2.mass() - t2bar.mass());

          // Choose configuration with minimum difference of t, tbar masses
          FourMomentum top = t1;
          FourMomentum tbar = t1bar;
          double cmin = c11;

          if (c12 < cmin) {
            top = t1;
            tbar = t2bar;
            cmin = c12;
          }

          if (c21 < cmin) {
            top = t2;
            tbar = t1bar;
            cmin = c21;
          }

          if (c22 < cmin) {
            top = t2;
            tbar = t2bar;
            cmin = c22;
          }

          // Fill t, tbar
          _h_t_pT_W_cut->fill(top.pT(), weight);
          _h_t_pT_W_cut->fill(tbar.pT(), weight);

        }
        else vetoEvent;
      }

      void finalize() {
        scale(_h_t_pT_W_cut,1000 * crossSection()/sumOfWeights());
      }
      //@}

    private:

      AIDA::IHistogram1D *_h_t_pT_W_cut;

  };


  // This global object acts as a hook for the plugin system
  AnalysisBuilder<D0_2010_S8521379> plugin_D0_2010_S8521379;

}
