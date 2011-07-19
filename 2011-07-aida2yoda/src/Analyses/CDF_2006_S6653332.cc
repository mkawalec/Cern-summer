// -*- C++ -*-
#include "Rivet/Analysis.hh"
#include "Rivet/RivetAIDA.hh"
#include "Rivet/Tools/Logging.hh"
#include "Rivet/Tools/ParticleIdUtils.hh"
#include "Rivet/Projections/FinalState.hh"
#include "Rivet/Projections/VetoedFinalState.hh"
#include "Rivet/Projections/ChargedFinalState.hh"
#include "Rivet/Projections/InvMassFinalState.hh"
#include "Rivet/Projections/FastJets.hh"
#include "Rivet/Projections/ChargedLeptons.hh"

namespace Rivet {


  /* @brief CDF Run II analysis: jet \f$ p_T \f$ and \f$ \eta \f$
   *   distributions in Z + (b) jet production
   * @author Lars Sonnenschein
   *
   * This CDF analysis provides \f$ p_T \f$ and \f$ \eta \f$ distributions of
   * jets in Z + (b) jet production, before and after tagging.
   */
  class CDF_2006_S6653332 : public Analysis {
  public:
    
    /// Constructor
    CDF_2006_S6653332()
      : Analysis("CDF_2006_S6653332"),
        _Rjet(0.7), _JetPtCut(20.), _JetEtaCut(1.5), _Lep1PtCut(18.), _Lep2PtCut(10.), _LepEtaCut(1.1),
        _sumWeightsWithZ(0.0), _sumWeightsWithZJet(0.0)
    {
      setBeams(PROTON, ANTIPROTON);
      setNeedsCrossSection(true);
    }
    
    
    /// @name Analysis methods
    //@{
    
    void init() {
      const FinalState fs(-3.6, 3.6);
      addProjection(fs, "FS");
   
      // Create a final state with any e+e- or mu+mu- pair with
      // invariant mass 76 -> 106 GeV and ET > 20 (Z decay products)
      vector<pair<PdgId,PdgId> > vids;
      vids.push_back(make_pair(ELECTRON, POSITRON));
      vids.push_back(make_pair(MUON, ANTIMUON));
      FinalState fs2(-3.6, 3.6);
      InvMassFinalState invfs(fs2, vids, 66*GeV, 116*GeV);
      addProjection(invfs, "INVFS");
   
      // Make a final state without the Z decay products for jet clustering
      VetoedFinalState vfs(fs);
      vfs.addVetoOnThisFinalState(invfs);
      addProjection(vfs, "VFS");
      addProjection(FastJets(vfs, FastJets::CDFMIDPOINT, 0.7), "Jets");

      // Book histograms
      _sigmaBJet = bookHistogram1D(1, 1, 1);
      _ratioBJetToZ = bookHistogram1D(2, 1, 1);
      _ratioBJetToJet = bookHistogram1D(3, 1, 1);
    }


    /// Do the analysis
    void analyze(const Event& event) {
      // Check we have an l+l- pair that passes the kinematic cuts
      // Get the Z decay products (mu+mu- or e+e- pair)
      const InvMassFinalState& invMassFinalState = applyProjection<InvMassFinalState>(event, "INVFS");
      const ParticleVector&  ZDecayProducts =  invMassFinalState.particles();
   
      // Make sure we have at least 2 Z decay products (mumu or ee)
      if (ZDecayProducts.size() < 2) vetoEvent;
      //
      double Lep1Pt = ZDecayProducts[0].momentum().perp();
      double Lep2Pt = ZDecayProducts[1].momentum().perp();
      double Lep1Eta = fabs(ZDecayProducts[0].momentum().rapidity());
      double Lep2Eta = fabs(ZDecayProducts[1].momentum().rapidity());

      if (Lep1Eta > _LepEtaCut && Lep2Eta > _LepEtaCut) vetoEvent;

      if (abs(ZDecayProducts[0].pdgId())==13 && (Lep1Eta > 1.0 && Lep2Eta > 1.)) {
        vetoEvent;
      }
      if (Lep1Pt < _Lep1PtCut && Lep2Pt < _Lep1PtCut) vetoEvent;
      
      //
      
      _sumWeightsWithZ += event.weight();
      // @todo: write out a warning if there are more than two decay products
      FourMomentum Zmom = ZDecayProducts[0].momentum() +  ZDecayProducts[1].momentum();
   
      // Put all b-quarks in a vector
      /// @todo Use jet contents rather than accessing quarks directly
      ParticleVector bquarks;
      /// @todo Use nicer looping
      for (GenEvent::particle_const_iterator p = event.genEvent().particles_begin();
           p != event.genEvent().particles_end(); ++p) {
        if ( fabs((*p)->pdg_id()) == BQUARK ) {
          bquarks.push_back(Particle(**p));
        }
      }
   
      // Get jets
      const FastJets& jetpro = applyProjection<FastJets>(event, "Jets");
      getLog() << Log::DEBUG << "Jet multiplicity before any pT cut = " << jetpro.size() << endl;
   
      const PseudoJets& jets = jetpro.pseudoJetsByPt();
      getLog() << Log::DEBUG << "jetlist size = " << jets.size() << endl;
   
      int numBJet = 0;
      int numJet  = 0;
      // for each b-jet plot the ET and the eta of the jet, normalise to the total cross section at the end
      // for each event plot N jet and pT(Z), normalise to the total cross section at the end
      for (PseudoJets::const_iterator jt = jets.begin(); jt != jets.end(); ++jt) {
        // select jets that pass the kinematic cuts
        if (jt->perp() > _JetPtCut && fabs(jt->rapidity()) <= _JetEtaCut) {
          ++numJet;
          // Does the jet contain a b-quark?
          /// @todo Use jet contents rather than accessing quarks directly
       
          bool bjet = false;
          foreach (const Particle& bquark,  bquarks) {
            if (deltaR(jt->rapidity(), jt->phi(), bquark.momentum().rapidity(),bquark.momentum().azimuthalAngle()) <= _Rjet) {
              bjet = true;
              break;
            }
          } // end loop around b-jets
          if (bjet) {
            numBJet++;
          }
        }
      } // end loop around jets
   
      if (numJet > 0)    _sumWeightsWithZJet += event.weight();
      if (numBJet > 0) {
        _sigmaBJet->fill(1960.0,event.weight());
        _ratioBJetToZ->fill(1960.0,event.weight());
        _ratioBJetToJet->fill(1960.0,event.weight());
      }
   
    }
 

    /// Finalize
    void finalize() {
      getLog() << Log::DEBUG << "Total sum of weights = " << sumOfWeights() << endl;
      getLog() << Log::DEBUG << "Sum of weights for Z production in mass range = " << _sumWeightsWithZ << endl;
      getLog() << Log::DEBUG << "Sum of weights for Z+jet production in mass range = " << _sumWeightsWithZJet << endl;
   
      _sigmaBJet->scale(crossSection()/sumOfWeights());
      _ratioBJetToZ->scale(1.0/_sumWeightsWithZ);
      _ratioBJetToJet->scale(1.0/_sumWeightsWithZJet);
    }
 
        //@}


  private:

    /// @name Cuts and counters
    //@{

    double _Rjet;
    double _JetPtCut;
    double _JetEtaCut;
    double _Lep1PtCut;
    double _Lep2PtCut;
    double _LepEtaCut;
    
    double _sumWeightsWithZ;
    double _sumWeightsWithZJet;

    //@}

    /// @name Histograms
    //@{
    AIDA::IHistogram1D* _sigmaBJet;
    AIDA::IHistogram1D* _ratioBJetToZ;
    AIDA::IHistogram1D* _ratioBJetToJet;
    //@}
 
  };


  // This global object acts as a hook for the plugin system
  AnalysisBuilder<CDF_2006_S6653332> plugin_CDF_2006_S6653332;

}
