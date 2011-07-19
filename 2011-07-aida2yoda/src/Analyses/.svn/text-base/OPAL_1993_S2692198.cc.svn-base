// -*- C++ -*-
#include "Rivet/Analysis.hh"
#include "Rivet/RivetAIDA.hh"
#include "Rivet/Tools/ParticleIdUtils.hh"
#include "Rivet/Projections/Beam.hh"
#include "Rivet/Projections/FinalState.hh"
#include "Rivet/Projections/ChargedFinalState.hh"
#include "Rivet/Projections/FastJets.hh"
#include "fastjet/JadePlugin.hh"

namespace Rivet {


  /// @brief OPAL photon production 
  /// @author Peter Richardson
  class OPAL_1993_S2692198 : public Analysis {
  public:

    /// Constructor
    OPAL_1993_S2692198() : Analysis("OPAL_1993_S2692198")
    {
      setBeams(ELECTRON, POSITRON);

    }


    /// @name Analysis methods
    //@{

    void analyze(const Event& e) {
      // First, veto on leptonic events by requiring at least 4 charged FS particles
//       const ChargedFinalState& cfs = applyProjection<ChargedFinalState>(e, "CFS");
//       const size_t numParticles = cfs.particles().size();

//       if (numParticles < 4) {
//         getLog() << Log::DEBUG << "Failed ncharged cut" << endl;
//         vetoEvent;
//       }
//       getLog() << Log::DEBUG << "Passed ncharged cut" << endl;

      // Get event weight for histo filling
      const double weight = e.weight();

      // extract the photons
      ParticleVector photons;
      ParticleVector nonPhotons;
      FourMomentum ptotal;
      const FinalState& fs = applyProjection<FinalState>(e, "FS");
      foreach (const Particle& p, fs.particles()) {
	ptotal+= p.momentum();
	if(p.pdgId()==PHOTON) {
	  photons.push_back(p);
	}
	else {
	  nonPhotons.push_back(p);
	}
      }
      // no photon return but still count for normalisation
      if(photons.empty()) return;
      // definition of the Durham algorithm
      fastjet::JetDefinition durham_def(fastjet::ee_kt_algorithm,fastjet::E_scheme,
					fastjet::Best);
      // definition of the JADE algorithm
      fastjet::JadePlugin jade;
      fastjet::JetDefinition jade_def = fastjet::JetDefinition(&jade);
      // now for the weird jet algorithm
      double evis = ptotal.mass();
      vector<fastjet::PseudoJet> input_particles;
      // pseudo jets from the non photons
      foreach (const Particle& p,  nonPhotons) {
	input_particles.push_back(fastjet::PseudoJet(p.momentum().px(),
						     p.momentum().py(),
						     p.momentum().pz(),
						     p.momentum().E()));
      }
      // pseudo jets from all bar the first photon
      for(unsigned int ix=1;ix<photons.size();++ix) {
	input_particles.push_back(fastjet::PseudoJet(photons[ix].momentum().px(),
						     photons[ix].momentum().py(),
						     photons[ix].momentum().pz(),
						     photons[ix].momentum().E()));
      }
      // now loop over the photons
      for(unsigned int ix=0;ix<photons.size();++ix) {
	FourMomentum pgamma = photons[ix].momentum();
	// run the jet clustering DURHAM
	fastjet::ClusterSequence clust_seq(input_particles, durham_def);
	// cluster the jets
	for (int j = 0; j < _nPhotonDurham->size(); ++j) {
	  bool accept(true);
	  double ycut = _nPhotonDurham->point(j)->coordinate(0)->value();
	  double dcut = sqr(evis)*ycut;
	  vector<fastjet::PseudoJet> exclusive_jets = 
	    sorted_by_E(clust_seq.exclusive_jets(dcut));
	  for(unsigned int iy=0;iy<exclusive_jets.size();++iy) {
	    FourMomentum pjet(momentum(exclusive_jets[iy]));
	    double cost = pjet.vector3().unit().dot(pgamma.vector3().unit());
	    double ygamma = 2.*min(sqr(pjet.E()/evis),
				   sqr(pgamma.E()/evis))*(1.-cost);
	    if(ygamma<ycut) {
	      accept = false;
	      break;
	    }
	  }
	  if(!accept) continue;
	  _nPhotonDurham->point(j)->coordinate(1)->
	    setValue(_nPhotonDurham->point(j)->coordinate(1)->value()+weight);
	  int njet = min(4,int(exclusive_jets.size())) - 1;
	  if(j<_nPhotonJetDurham[njet]->size()) {
	    _nPhotonJetDurham[njet]->point(j)->coordinate(1)->
	      setValue(_nPhotonJetDurham[njet]->point(j)->coordinate(1)->value()+weight);
	  }
	}
	// run the jet clustering JADE
	fastjet::ClusterSequence clust_seq2(input_particles, jade_def);
	for (int j = 0; j < _nPhotonJade->size(); ++j) {
	  bool accept(true);
	  double ycut = _nPhotonJade->point(j)->coordinate(0)->value();
	  double dcut = sqr(evis)*ycut;
	  vector<fastjet::PseudoJet> exclusive_jets = 
	    sorted_by_E(clust_seq2.exclusive_jets(dcut));
	  for(unsigned int iy=0;iy<exclusive_jets.size();++iy) {
	    FourMomentum pjet(momentum(exclusive_jets[iy]));
	    double cost = pjet.vector3().unit().dot(pgamma.vector3().unit());
	    double ygamma = 2.*pjet.E()*pgamma.E()/sqr(evis)*(1.-cost);
	    if(ygamma<ycut) {
	      accept = false;
	      break;
	    }
	  }
	  if(!accept) continue;
	  _nPhotonJade->point(j)->coordinate(1)->
	    setValue(_nPhotonJade->point(j)->coordinate(1)->value()+weight);
	  int njet = min(4,int(exclusive_jets.size())) - 1;
	  if(j<_nPhotonJetJade[njet]->size()) {
	    _nPhotonJetJade[njet]->point(j)->coordinate(1)->
	      setValue(_nPhotonJetJade[njet]->point(j)->coordinate(1)->value()+weight);
	  }
	}
	// add this photon back in for the next interation of the loop
	if(ix+1!=photons.size())
	  input_particles[nonPhotons.size()+ix] = 
	    fastjet::PseudoJet(photons[ix].momentum().px(),photons[ix].momentum().py(),
			       photons[ix].momentum().pz(),photons[ix].momentum().E());
      }
    }


    void init() {
      // Projections
      addProjection(FinalState(), "FS");
//       addProjection(ChargedFinalState(), "CFS");

      // Book data sets
      _nPhotonJade       = bookDataPointSet(1, 1, 1);
      _nPhotonDurham     = bookDataPointSet(2, 1, 1);
      for(unsigned int ix=0;ix<4;++ix) {
	_nPhotonJetJade  [ix] = bookDataPointSet(3 , 1, 1+ix);
	_nPhotonJetDurham[ix] = bookDataPointSet(4 , 1, 1+ix);
      }
    }


    /// Finalize
    void finalize() {
      const double fact = 1000./sumOfWeights();
      normaliseDataPointSet(_nPhotonJade      ,fact);
      normaliseDataPointSet(_nPhotonDurham    ,fact);
      for(unsigned int ix=0;ix<4;++ix) {
	normaliseDataPointSet(_nPhotonJetJade  [ix],fact);
	normaliseDataPointSet(_nPhotonJetDurham[ix],fact);
      }
    }

    // normalise a data point set, default function does both x and y AHHH
    void normaliseDataPointSet(AIDA::IDataPointSet * points, const double & fact) {
      for (int i = 0; i < points->size(); ++i) {
	points->point(i)->coordinate(1)->
	  setValue(points->point(i)->coordinate(1)->value()*fact);
      }
    }
    //@}

  private:

    AIDA::IDataPointSet *_nPhotonJade;
    AIDA::IDataPointSet *_nPhotonDurham;
    AIDA::IDataPointSet *_nPhotonJetJade  [4];
    AIDA::IDataPointSet *_nPhotonJetDurham[4];

  };



  // This global object acts as a hook for the plugin system
  AnalysisBuilder<OPAL_1993_S2692198> plugin_OPAL_1993_S2692198;

}
