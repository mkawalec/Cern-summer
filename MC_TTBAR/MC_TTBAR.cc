#include "Rivet/Analysis.hh"
#include "Rivet/Projections/FinalState.hh"
#include "Rivet/Projections/ChargedFinalState.hh"
#include "Rivet/Projections/ChargedLeptons.hh"
#include "Rivet/Projections/FastJets.hh"
#include "Rivet/AnalysisLoader.hh"
#include "Rivet/RivetAIDA.hh"
#include <iostream>

namespace Rivet {
  
  class MC_TTBAR : public Analysis {
    
  public:
    
    /// Default constructor
    MC_TTBAR()
      : Analysis("MC_TTBAR")
    {   }

    /// @name Analysis methods
    //@{

    void init() {
      // Actually, why fastjest have different rapidity ranges than CFSs?
      addProjection(ChargedFinalState(-3.5, 3.5, 0.5*GeV), "CFS");
      addProjection(ChargedLeptons(ChargedFinalState(-3.5, 3.5, 30*GeV)), "LFS");
      addProjection(FastJets(FinalState(-2.5, 2.5, 0*GeV), FastJets::KT, 0.5), "JETS");

      _h_t_mass = bookHistogram1D("t_mass", 150, 130, 430);
      _h_t_pT = bookHistogram1D("t_pT", 150, 130, 430);
      _h_t_rap = bookHistogram1D("t_rap", 150, 130, 430);
    }
    
    void analyze(const Event& event) {
      double weight = event.weight();
      
      //Applying projections:
      const FinalState& cfs = applyProjection<FinalState>(event, "CFS");
      const ChargedLeptons& lfs = applyProjection<ChargedLeptons>(event, "LFS");
      
      //Outputting some additional info:
      getLog() << Log::DEBUG << "Total charged multiplicity    = " 
               << cfs.size()  << endl;
      getLog() << Log::DEBUG << "Charged lepton multiplicity   = " 
               << lfs.chargedLeptons().size()  << endl;

      //Aren't we artificially throwing out events that could give us t/tbar just because of the noise?
      if (lfs.chargedLeptons().size() != 1) {
        getLog() << Log::DEBUG << "Event failed lepton cut" << endl;
        vetoEvent;
      }

      foreach (Particle lepton, lfs.chargedLeptons()) {
        getLog() << Log::DEBUG << "lepton pT = " << lepton.momentum().pT() << endl;
      }

      //Applying fastjets projection and filtering out all those that have pT lower than 35,
      //as we don't really need those for any of the computations.
      const FastJets& jetpro = applyProjection<FastJets>(event, "JETS");
      const Jets jets = jetpro.jetsByPt(35);
      getLog() << Log::DEBUG << "Energetic jets multiplicity = " << jets.size() << endl;

      if (jets.size() < 4) {
        getLog() << Log::DEBUG << "Event failed jet cut" << endl;
        vetoEvent;
      }

      // Put all b-quarks in a vector
      ParticleVector bquarks;
      for (GenEvent::particle_const_iterator p = event.genEvent().particles_begin(); 
           p != event.genEvent().particles_end(); ++p) {
        if ( fabs((*p)->pdg_id()) == BQUARK ) {
          bquarks.push_back(Particle(**p));
        }
      }

      Jets bjets, ljets;

      foreach (Jet jet, jets) {
        //Next line added to avoid recomputing eta and phi again and again
        double eta = jet.eta(); double phi = jet.phi();
	foreach (Particle bquark, bquarks) {
          if (deltaR(eta, phi, bquark.momentum().pseudorapidity(), bquark.momentum().azimuthalAngle()) < 0.5) {
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
      FourMomentum t1 = W + bjets[0].momentum();
      FourMomentum t2 = W + bjets[1].momentum();
      getLog() << Log::INFO << "W found with mass " << W.mass() << endl;

      if (W.mass() > 70 && W.mass() < 90) {
        getLog() << Log::INFO << "W found with mass " << W.mass() << endl;

        _h_t_mass->fill(t1.mass(), weight);
        _h_t_mass->fill(t2.mass(), weight);
        _h_t_rap->fill(t1.rapidity(), weight);
        _h_t_rap->fill(t2.rapidity(), weight);
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
  };

  // This global object acts as a hook for the plugin system
  AnalysisBuilder<MC_TTBAR> plugin_MC_TTBAR;

}