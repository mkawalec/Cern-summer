// -*- C++ -*- 
#include "Rivet/Analysis.hh"
#include "Rivet/Tools/BinnedHistogram.hh"
#include "Rivet/RivetAIDA.hh"
#include "Rivet/Tools/Logging.hh"
#include "Rivet/Projections/FinalState.hh"
#include "Rivet/Projections/ChargedFinalState.hh"
#include "Rivet/Projections/VisibleFinalState.hh"
#include "Rivet/Projections/IdentifiedFinalState.hh"
#include "Rivet/Projections/FastJets.hh"

namespace Rivet {


  class ATLAS_2011_CONF_2011_090 : public Analysis {
  public:

    /// @name Constructors etc.
    //@{

    /// Constructor

    ATLAS_2011_CONF_2011_090()
      : Analysis("ATLAS_2011_CONF_2011_090")

    {
      /// Set whether your finalize method needs the generator cross section
      setNeedsCrossSection(false);
    }

    //@}


  public:

    /// @name Analysis methods
    //@{

    /// Book histograms and initialize projections before the run
    void init() {

      // projection to find the electrons
      std::vector<std::pair<double, double> > eta_e;
      eta_e.push_back(make_pair(-2.47,2.47));
      IdentifiedFinalState elecs(eta_e, 20.0*GeV);
      elecs.acceptIdPair(ELECTRON);
      addProjection(elecs, "elecs");


      // veto region electrons (from 2010 arXiv:1102.2357v2)
      std::vector<std::pair<double, double> > eta_v_e;
      eta_v_e.push_back(make_pair(-1.52,-1.37));
      eta_v_e.push_back(make_pair( 1.37, 1.52));
      IdentifiedFinalState veto_elecs(eta_v_e, 10.0*GeV);
      veto_elecs.acceptIdPair(ELECTRON);
      addProjection(veto_elecs, "veto_elecs");


      // projection to find the muons
      std::vector<std::pair<double, double> > eta_m;
      eta_m.push_back(make_pair(-2.4,2.4));
      IdentifiedFinalState muons(eta_m, 10.0*GeV);
      muons.acceptIdPair(MUON);
      addProjection(muons, "muons");


      // Jet finder
      VetoedFinalState vfs;
      vfs.addVetoPairDetail(MUON,10*GeV,7000*GeV);
      vfs.addVetoPairDetail(ELECTRON,20*GeV,7000*GeV);
      addProjection(FastJets(vfs, FastJets::ANTIKT, 0.4),
                   "AntiKtJets04");


      // all tracks (to do deltaR with leptons)
      addProjection(ChargedFinalState(-3.0,3.0,0.5*GeV),"cfs");


      // for pTmiss
      addProjection(VisibleFinalState(-4.9,4.9),"vfs");


      /// Book histograms
      _count_mu_channel = bookHistogram1D("count_muon_channel", 1, 0., 1.);
      _count_e_channel = bookHistogram1D("count_electron_channel", 1, 0., 1.); 
      _hist_eTmiss_e = bookHistogram1D("Et_miss_e", 50, 0., 500.);
      _hist_eTmiss_mu = bookHistogram1D("Et_miss_mu", 50, 0., 500.);
      _hist_m_eff_e = bookHistogram1D("m_eff_e", 30, 0., 1500.);
      _hist_m_eff_mu = bookHistogram1D("m_eff_mu", 30, 0., 1500.);
      _hist_m_eff_e_final = bookHistogram1D("m_eff_e_final", 30, 0., 1500.);
      _hist_m_eff_mu_final = bookHistogram1D("m_eff_mu_final", 30, 0., 1500.);



    }



    /// Perform the per-event analysis
    void analyze(const Event& event) {

      const double weight = event.weight();      
      

      ParticleVector veto_e 
	= applyProjection<IdentifiedFinalState>(event, "veto_elecs").particles();
      if ( ! veto_e.empty() ) {
       	MSG_DEBUG("electrons in veto region");
       	vetoEvent;
      }

      Jets cand_jets;
      foreach ( const Jet& jet, 
       	  applyProjection<FastJets>(event, "AntiKtJets04").jetsByPt(20.0*GeV) ) {
        if ( fabs( jet.momentum().eta() ) < 2.8 ) {
          cand_jets.push_back(jet);
        }
      } 

      ParticleVector candtemp_e = 
	applyProjection<IdentifiedFinalState>(event, "elecs").particlesByPt();      
      ParticleVector candtemp_mu = 
	applyProjection<IdentifiedFinalState>(event,"muons").particlesByPt();
      ParticleVector chg_tracks = 
	applyProjection<ChargedFinalState>(event, "cfs").particles();
      ParticleVector cand_mu;
      ParticleVector cand_e;


      // pTcone around muon track 
      foreach ( const Particle & mu, candtemp_mu ) {
	double pTinCone = -mu.momentum().pT();
	foreach ( const Particle & track, chg_tracks ) {
	  if ( deltaR(mu.momentum(),track.momentum()) < 0.2 )
	    pTinCone += track.momentum().pT();
	}
	if ( pTinCone < 1.8*GeV ) 
	  cand_mu.push_back(mu);
      }


      // pTcone around electron
      foreach ( const Particle e, candtemp_e ) {
	double pTinCone = -e.momentum().pT();
	foreach ( const Particle & track, chg_tracks ) {
	  if ( deltaR(e.momentum(),track.momentum()) < 0.2 )  
	    pTinCone += track.momentum().pT();
	}
	if ( pTinCone < 0.10 * e.momentum().pT() )
	  cand_e.push_back(e);
      }



      // discard jets that overlap with electrons
      Jets cand_jets_2;
      foreach ( const Jet& jet, cand_jets ) {
	  bool away_from_e = true;
	  foreach ( const Particle & e, cand_e ) {
	    if ( deltaR(e.momentum(),jet.momentum()) <= 0.2 ) {
	      away_from_e = false;
	      break;
	    }
	  }
	  if ( away_from_e ) 
	    cand_jets_2.push_back( jet );
      }
      
      // only consider leptons far from jet
      ParticleVector recon_e, recon_mu;  
      foreach ( const Particle & e, cand_e ) {
        bool e_near_jet = false;
	foreach ( const Jet& jet, cand_jets_2 ) {  
          if ( deltaR(e.momentum(),jet.momentum()) < 0.4 && 
	       deltaR(e.momentum(),jet.momentum()) > 0.2 ) 
	    e_near_jet = true;
	}
        if ( e_near_jet == false )
          recon_e.push_back( e );  
       }

      foreach ( const Particle & mu, cand_mu ) {
         bool mu_near_jet = false;
         foreach ( const Jet& jet, cand_jets_2 ) {	
           if ( deltaR(mu.momentum(),jet.momentum()) < 0.4 ) 
	     mu_near_jet = true;	   
	 }
	 if ( mu_near_jet == false ) 
	  recon_mu.push_back( mu );
       } 

      // pTmiss
      ParticleVector vfs_particles 
	= applyProjection<VisibleFinalState>(event, "vfs").particles();
      FourMomentum pTmiss;
      foreach ( const Particle & p, vfs_particles ) {
	pTmiss -= p.momentum();
      }
      double eTmiss = pTmiss.pT();


      // final jet filter
      Jets recon_jets;
      foreach ( const Jet& jet, cand_jets_2 ) {
	  recon_jets.push_back( jet );
      }



	
      // ==================== observables ====================


      // Njets

      int Njets = 0;
      double pTmiss_phi = pTmiss.phi();
      foreach ( const Jet& jet, recon_jets ) {
	if ( fabs(jet.momentum().eta()) < 2.8 ) 
	  Njets+=1;
      }     
      if ( Njets < 3 ) {
	MSG_DEBUG("Only " << Njets << " jets w/ eta<2.8 left");
	vetoEvent;
      }

      if ( recon_jets[0].momentum().pT() <= 60.0 * GeV ) {
	MSG_DEBUG("No hard leading jet in " << recon_jets.size() << " jets");
	vetoEvent;
      }
      for ( int i = 1; i < 3; ++i ) {
	if ( recon_jets[i].momentum().pT() <= 25*GeV ) {
	  vetoEvent;
	}
      }      

      for ( int i = 0; i < 3; ++i ) {
	double dPhi = deltaPhi( pTmiss_phi, recon_jets[i].momentum().phi() );
	if ( dPhi <= 0.2 ) {
	  MSG_DEBUG("dPhi too small");
	  vetoEvent;
	  break;
	}
      }


      ParticleVector lepton;
      if ( recon_mu.empty() && recon_e.empty() ) {
	MSG_DEBUG("No leptons");
	vetoEvent;
      }
      else {
	foreach ( const Particle & mu, recon_mu ) 
	    lepton.push_back(mu);
        foreach ( const Particle & e, recon_e ) 
	    lepton.push_back(e);
      }

      std::sort(lepton.begin(), lepton.end(), cmpParticleByPt);

      double e_id = 11;
      double mu_id = 13;

      // one hard leading lepton cut
      if ( fabs(lepton[0].pdgId()) == e_id && 
           lepton[0].momentum().pT() <= 25*GeV ) {
	vetoEvent;
      }
      else if ( fabs(lepton[0].pdgId()) == mu_id && 
                lepton[0].momentum().pT() <= 20*GeV ) {
	vetoEvent;
      }
      
      // exactly one hard leading lepton cut
      if ( fabs(lepton[1].pdgId()) == e_id && 
           lepton[1].momentum().pT() > 20*GeV ) {
	  vetoEvent;
      }
      else if ( fabs(lepton[1].pdgId()) == mu_id && 
                lepton[1].momentum().pT() > 10*GeV ) {
	  vetoEvent;
      }
     
     

    // ==================== FILL ====================


      FourMomentum pT_l = lepton[0].momentum();
     

      double dPhi = deltaPhi( pT_l.phi(), pTmiss_phi);
      double mT = sqrt( 2 * pT_l.pT() * eTmiss * (1 - cos(dPhi)) );


      // effective mass
      double m_eff = eTmiss + pT_l.pT() 
	+ recon_jets[0].momentum().pT() 
	+ recon_jets[1].momentum().pT()
	+ recon_jets[2].momentum().pT();

     
      // Electron channel signal region
      
      if ( fabs( lepton[0].pdgId() ) == e_id ) {

        _hist_eTmiss_e->fill(eTmiss, weight);
        _hist_m_eff_e->fill(m_eff, weight);

        if ( mT > 100*GeV && eTmiss > 125*GeV ) { 
	  _hist_m_eff_e_final->fill(m_eff, weight);
	  if ( m_eff > 500*GeV && eTmiss > 0.25*m_eff ) {
            _count_e_channel->fill(0.5,weight);	
	  }
        }
      }

      // Muon channel signal region

      else if ( fabs( lepton[0].pdgId() ) == mu_id ) {      

        _hist_eTmiss_mu->fill(eTmiss, weight);
        _hist_m_eff_mu->fill(m_eff, weight);

        if ( mT > 100*GeV && eTmiss > 125*GeV ) {
          _hist_m_eff_mu_final->fill(m_eff, weight);
 	  if ( m_eff > 500*GeV && eTmiss > 0.25*m_eff ) {
            _count_mu_channel->fill(0.5,weight);
          }
        }
     
      }   


    }

    //@}

    
    void finalize() {


	scale( _hist_eTmiss_e, 10. * 165. * crossSection()/sumOfWeights() );
	scale( _hist_eTmiss_mu, 10. * 165. * crossSection()/sumOfWeights() );
	scale( _hist_m_eff_e, 50. * 165. * crossSection()/sumOfWeights() );
	scale( _hist_m_eff_mu, 50. * 165. * crossSection()/sumOfWeights() );
	scale( _hist_m_eff_e_final, 50. * 165. * crossSection()/sumOfWeights() );
	scale( _hist_m_eff_mu_final, 50. * 165. * crossSection()/sumOfWeights() );


    }

  private:

    /// @name Histograms
    //@{
    AIDA::IHistogram1D* _count_e_channel;
    AIDA::IHistogram1D* _count_mu_channel;

    AIDA::IHistogram1D* _hist_eTmiss_e;
    AIDA::IHistogram1D* _hist_eTmiss_mu;

    AIDA::IHistogram1D* _hist_m_eff_e;
    AIDA::IHistogram1D* _hist_m_eff_mu;
    AIDA::IHistogram1D* _hist_m_eff_e_final;
    AIDA::IHistogram1D* _hist_m_eff_mu_final;


    //@}

    
  };



  // This global object acts as a hook for the plugin system
  AnalysisBuilder<ATLAS_2011_CONF_2011_090> plugin_ATLAS_2011_CONF_2011_090;


}
