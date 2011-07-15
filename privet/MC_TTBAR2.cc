#include "Rivet/Analysis.hh"
#include "Rivet/Projections/FinalState.hh"
#include "Rivet/Projections/UnstableFinalState.hh"
#include "Rivet/Projections/ChargedFinalState.hh"
#include "Rivet/Projections/ChargedLeptons.hh"
#include "Rivet/Projections/FastJets.hh"
#include "Rivet/AnalysisLoader.hh"
#include "Rivet/RivetAIDA.hh"
#include <iostream>

namespace Rivet {
  
  class MC_TTBAR2 : public Analysis {
    
  public:
    
    MC_TTBAR2()
      : Analysis("MC_TTBAR2")
    {   }

    void init() {
      // Actually, why fastjest have different rapidity ranges than CFSs?
      // No idea! I suspect original author knows more about particle physics
      // than we do!

      addProjection(
        ChargedLeptons(ChargedFinalState(-3.5, 3.5, 30*GeV)), "LFS"
        );

      addProjection(
        FastJets(FinalState(-2.5, 2.5, 0*GeV), FastJets::KT, 0.5), "JETS"
        );

      // Book histograms
      _h_t_mass = bookHistogram1D("t_mass", 50, 130, 430);
      _h_t_pT = bookHistogram1D("t_pT", 50, 0, 250);
      _h_t_rap = bookHistogram1D("t_rap", 50, 0, 2.5);
      _h_W_mass = bookHistogram1D("W_mass", 50, 30, 180);
      _h_W_pT = bookHistogram1D("W_pT", 50, 0, 250);
      _h_W_rap = bookHistogram1D("W_rap", 50, 0, 2.5);
    }
    
    void analyze(const Event& event) {
      double weight = event.weight();
      
      // Applying initial projection
      const ChargedLeptons& lfs = applyProjection<ChargedLeptons>(event, "LFS");
      
      // Aren't we artificially throwing out events that could give us
      // t/tbar just because of the noise?
      if (lfs.chargedLeptons().size() != 1) {
        getLog() << Log::DEBUG << "Event failed lepton cut" << endl;
        vetoEvent;
      }

      foreach (Particle lepton, lfs.chargedLeptons()) {
        getLog() << Log::DEBUG <<
          "lepton pT = " << lepton.momentum().pT() << endl;
      }

      // Applying fastjets projection and filtering out all those that have pT
      // lower than 35, as we don't really need those for any of the
      // computations.
      

      const FastJets& jetpro = applyProjection<FastJets>(event, "JETS");
      const Jets jets = jetpro.jetsByPt(35);
      getLog() << Log::DEBUG <<
        "Energetic jets multiplicity = " << jets.size() << endl;

      if (jets.size() < 4) {
        getLog() << Log::DEBUG << "Event failed jet cut" << endl;
        vetoEvent;
      }

      // Put all b-quarks in a vector
      // Ugly. Can we foreach this?
      ParticleVector bquarks;
      foreach(const GenParticle* p, Rivet::particles(event.genEvent())) {
        if ( fabs(p->pdg_id()) == BQUARK ) {
          bquarks.push_back(*p);
        }
      }

      Jets bjets, ljets;

      foreach (Jet jet, jets) {
        const double eta = jet.eta();
        const double phi = jet.phi();

	    foreach (Particle &bquark, bquarks) {
          
          if (deltaR(eta, phi, bquark.momentum().pseudorapidity(),
                  bquark.momentum().azimuthalAngle()) < 0.5) {
            bjets.push_back(jet);
          }
          else {
            ljets.push_back(jet);
          }
        }
      }

      if (bjets.size() !=2) {
        getLog() << Log::DEBUG << "Event failed b-tagging cut" << endl;
        vetoEvent;
      }

      FourMomentum W  = ljets[0].momentum() + ljets[1].momentum();
      // Can abs output int insetead of double and cause the problem with rapidity?
      _h_W_mass->fill(W.mass(), weight);
      _h_W_rap-> fill(abs(W.rapidity()), weight);
      _h_W_pT->  fill(W.pT(), weight);
      getLog() << Log::INFO << "W found with mass " << W.mass() << endl;

      // Mass cut
      if (W.mass() > 70 && W.mass() < 90) {

        FourMomentum t1 = W + bjets[0].momentum();
        FourMomentum t2 = W + bjets[1].momentum();

        getLog() << Log::INFO << "t, tbar found with massses " <<
                    t1.mass() << ", " << t2.mass() << endl;
        getLog() << Log::INFO << "and the respective rapidities are: " <<
                    t1.rapidity() << ", " << t2.rapidity() << endl;
        _h_t_mass->fill(t1.mass(), weight);
        _h_t_mass->fill(t2.mass(), weight);
        _h_t_rap->fill(abs(t1.rapidity()), weight);
        _h_t_rap->fill(abs(t2.rapidity()), weight);
        _h_t_pT->fill(t1.pT(), weight);
        _h_t_pT->fill(t2.pT(), weight);
      }

    }
    
    void finalize() {
      // No normalisation to be done for now, so proceeding
    }
    //@}

  private:
    AIDA::IHistogram1D *_h_t_mass, *_h_t_pT, *_h_t_rap;
    AIDA::IHistogram1D *_h_W_mass, *_h_W_pT, *_h_W_rap;
  };

  // This global object acts as a hook for the plugin system
  AnalysisBuilder<MC_TTBAR2> plugin_MC_TTBAR2;

}
