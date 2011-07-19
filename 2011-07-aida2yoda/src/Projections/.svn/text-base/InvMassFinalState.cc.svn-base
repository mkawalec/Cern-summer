// -*- C++ -*-
#include "Rivet/Projections/InvMassFinalState.hh"
#include "Rivet/Tools/Logging.hh"
#include "Rivet/Cmp.hh"

namespace Rivet {


  InvMassFinalState::InvMassFinalState(const FinalState& fsp,
                                       const pair<PdgId, PdgId>& idpair, // pair of decay products
                                       double minmass, // min inv mass
                                       double maxmass, // max inv mass
                                       double masstarget)
    : _minmass(minmass), _maxmass(maxmass), _masstarget(masstarget)
  {
    setName("InvMassFinalState");
    addProjection(fsp, "FS");
    _decayids.push_back(idpair);
  }


  InvMassFinalState::InvMassFinalState(const FinalState& fsp,
                                       const vector<pair<PdgId, PdgId> >& idpairs,  // vector of pairs of decay products
                                       double minmass, // min inv mass
                                       double maxmass, // max inv mass
                                       double masstarget)
    : _decayids(idpairs), _minmass(minmass), _maxmass(maxmass), _masstarget(masstarget)
  {
    setName("InvMassFinalState");
    addProjection(fsp, "FS");
  }


  int InvMassFinalState::compare(const Projection& p) const {
    // First compare the final states we are running on
    int fscmp = mkNamedPCmp(p, "FS");
    if (fscmp != EQUIVALENT) return fscmp;

    // Then compare the two as final states
    const InvMassFinalState& other = dynamic_cast<const InvMassFinalState&>(p);
    fscmp = FinalState::compare(other);
    if (fscmp != EQUIVALENT) return fscmp;

    // Then compare the mass limits
    int massllimcmp = cmp(_minmass, other._minmass);
    if (massllimcmp != EQUIVALENT) return massllimcmp;
    int masshlimcmp = cmp(_maxmass, other._maxmass);
    if (masshlimcmp != EQUIVALENT) return masshlimcmp;

    // Compare the decay species
    int decaycmp = cmp(_decayids, other._decayids);
    if (decaycmp != EQUIVALENT) return decaycmp;

    // Finally compare them as final states
    return FinalState::compare(other);
  }



  void InvMassFinalState::project(const Event& e) {
    _theParticles.clear();
    _particlePairs.clear();
    const FinalState& fs = applyProjection<FinalState>(e, "FS");

    // Containers for the particles of type specified in the pair
    vector<const Particle*> type1;
    vector<const Particle*> type2;
    // Get all the particles of the type specified in the pair from the particle list
    foreach (const Particle& ipart, fs.particles()) {
      // Loop around possible particle pairs (typedef needed to keep BOOST_FOREACH happy)
      foreach (const PdgIdPair& ipair, _decayids) {
        if (ipart.pdgId() == ipair.first) {
          if (accept(ipart)) {
            type1 += &ipart;
          }
        } else if (ipart.pdgId() == ipair.second) {
          if (accept(ipart)) {
            type2 += &ipart;
          }
        }
      }
    }
    if(type1.empty() || type2.empty()) return;

    // Temporary container of selected particles iterators
    // Useful to compare iterators and avoid double occurrences of the same
    // particle in case it matches with more than another particle
    vector<const Particle*> tmp;

    // Now calculate the inv mass
    pair<double, pair<Particle, Particle> > closestPair;
    closestPair.first = 1e30;
    foreach (const Particle* i1, type1) {
      foreach (const Particle* i2, type2) {
	// check this is actually a pair 
	// (if more than one pair in vector particles can be unrelated)
	bool found = false;
	foreach (const PdgIdPair& ipair, _decayids) {
	  if (i1->pdgId() == ipair.first &&
	      i2->pdgId() == ipair.second) {
	    found=true;
	    break;
	  }
	}
	if(!found) continue;

        FourMomentum v4 = i1->momentum() + i2->momentum();
        if (v4.mass2() < 0) {
          getLog() << Log::DEBUG << "Constructed negative inv mass2: skipping!" << endl;
          continue;
        }
        if (v4.mass() > _minmass && v4.mass() < _maxmass) {
          getLog() << Log::DEBUG << "Selecting particles with IDs "
                   << i1->pdgId() << " & " << i2->pdgId()
                   << " and mass = " << v4.mass()/GeV << " GeV" << endl;
          // Store accepted particles, avoiding duplicates
          if (find(tmp.begin(), tmp.end(), i1) == tmp.end()) {
            tmp.push_back(i1);
            _theParticles += *i1;
          }
          if (find(tmp.begin(), tmp.end(), i2) == tmp.end()) {
            tmp.push_back(i2);
            _theParticles += *i2;
          }
          // Store accepted particle pairs
          _particlePairs += make_pair(*i1, *i2);
          if (_masstarget>0.0) {
            double diff=fabs(v4.mass()-_masstarget);
            if (diff<closestPair.first) {
              closestPair.first=diff;
              closestPair.second=make_pair(*i1, *i2);
            }
          }
        }
      }
    }
    if (_masstarget>0.0&&closestPair.first<1e30) {
      _theParticles.clear();
      _particlePairs.clear();
      _theParticles += closestPair.second.first;
      _theParticles += closestPair.second.second;
      _particlePairs += closestPair.second;
    }

    getLog() << Log::DEBUG << "Selected " << _theParticles.size() << " particles "
             << "(" << _particlePairs.size() << " pairs)" << endl;
    if (getLog().isActive(Log::TRACE)) {
      foreach (const Particle& p, _theParticles) {
        getLog() << Log::TRACE << "ID: " << p.pdgId()
                 << ", barcode: " << p.genParticle().barcode() << endl;
      }
    }
  }


  /// Constituent pairs
  const std::vector<std::pair<Particle, Particle> >& InvMassFinalState::particlePairs() const {
    return _particlePairs;
  }


}
