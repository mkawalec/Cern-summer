// -*- C++ -*-
#include "Rivet/Rivet.hh"
#include "Rivet/Projections/VetoedFinalState.hh"
#include "Rivet/Cmp.hh"
#include "Rivet/Tools/Utils.hh"
#include <algorithm>

namespace Rivet {


  int VetoedFinalState::compare(const Projection& p) const {
    const PCmp fscmp = mkNamedPCmp(p, "FS");
    if (fscmp != EQUIVALENT) return fscmp;
    if (_vetofsnames.size() != 0) return UNDEFINED;
    const VetoedFinalState& other = dynamic_cast<const VetoedFinalState&>(p);
    return \
      cmp(_vetoCodes, other._vetoCodes) ||
      cmp(_compositeVetoes, other._compositeVetoes) ||
      cmp(_parentVetoes, other._parentVetoes);
  }


  void VetoedFinalState::project(const Event& e) {
    const FinalState& fs = applyProjection<FinalState>(e, "FS");
    _theParticles.clear();
    _theParticles.reserve(fs.particles().size());
    foreach (const Particle& p, fs.particles()) {
      if (getLog().isActive(Log::DEBUG)) {
        vector<long> codes;
        for (VetoDetails::const_iterator code = _vetoCodes.begin(); code != _vetoCodes.end(); ++code) {
          codes.push_back(code->first);
        }
        const string codestr = "{ " + join(codes) + " }";
        getLog() << Log::TRACE << p.pdgId() << " vs. veto codes = "
                 << codestr << " (" << codes.size() << ")" << endl;
      }
      const long pdgid = p.pdgId();
      const double pt = p.momentum().pT();
      VetoDetails::iterator iter = _vetoCodes.find(pdgid);
      if (iter == _vetoCodes.end()) {
        getLog() << Log::TRACE << "Storing with PDG code = " << pdgid << ", pT = " << pt << endl;
        _theParticles.push_back(p);
      } else {
        // This particle code is listed as a possible veto... check pT.
        // Make sure that the pT range is sensible:
        BinaryCut ptrange = iter->second;
        assert(ptrange.first <= ptrange.second);
        stringstream rangess;
        if (ptrange.first < numeric_limits<double>::max()) rangess << ptrange.second;
        rangess << " - ";
        if (ptrange.second < numeric_limits<double>::max()) rangess << ptrange.second;
        getLog() << Log::TRACE << "ID = " << pdgid << ", pT range = " << rangess.str();
        stringstream debugline;
        debugline << "with PDG code = " << pdgid << " pT = " << p.momentum().pT();
        if (pt < ptrange.first || pt > ptrange.second) {
          getLog() << Log::TRACE << "Storing " << debugline.str() << endl;
          _theParticles.push_back(p);
        } else {
          getLog() << Log::TRACE << "Vetoing " << debugline.str() << endl;
        }
      }
    }

    set<ParticleVector::iterator> toErase;
    for (set<int>::iterator nIt = _nCompositeDecays.begin();
         nIt != _nCompositeDecays.end() && !_theParticles.empty(); ++nIt) {
      map<set<ParticleVector::iterator>, FourMomentum> oldMasses;
      map<set<ParticleVector::iterator>, FourMomentum> newMasses;
      set<ParticleVector::iterator> start;
      start.insert(_theParticles.begin());
      oldMasses.insert(pair<set<ParticleVector::iterator>, FourMomentum>
                       (start, _theParticles.begin()->momentum()));
   
      for (int nParts = 1; nParts != *nIt; ++nParts) {
        for (map<set<ParticleVector::iterator>, FourMomentum>::iterator mIt = oldMasses.begin();
             mIt != oldMasses.end(); ++mIt) {
          ParticleVector::iterator pStart = *(mIt->first.rbegin());
          for (ParticleVector::iterator pIt = pStart + 1; pIt != _theParticles.end(); ++pIt) {
            FourMomentum cMom = mIt->second + pIt->momentum();
            set<ParticleVector::iterator> pList(mIt->first);
            pList.insert(pIt);
            newMasses[pList] = cMom;
          }
        }
        oldMasses = newMasses;
        newMasses.clear();
      }
      for (map<set<ParticleVector::iterator>, FourMomentum>::iterator mIt = oldMasses.begin();
           mIt != oldMasses.end(); ++mIt) {
        double mass2 = mIt->second.mass2();
        if (mass2 >= 0.0) {
          double mass = sqrt(mass2);
          for (CompositeVeto::iterator cIt = _compositeVetoes.lower_bound(*nIt);
               cIt != _compositeVetoes.upper_bound(*nIt); ++cIt) {
            BinaryCut massRange = cIt->second;
            if (mass < massRange.second && mass > massRange.first) {
              for (set<ParticleVector::iterator>::iterator lIt = mIt->first.begin();
                   lIt != mIt->first.end(); ++lIt) {
                toErase.insert(*lIt);
              }
            }
          }
        }
      }
    }
 
    for (set<ParticleVector::iterator>::reverse_iterator p = toErase.rbegin(); p != toErase.rend(); ++p) {
      _theParticles.erase(*p);
    }

    /// @todo Improve!
    for (ParentVetos::const_iterator vIt = _parentVetoes.begin(); vIt != _parentVetoes.end(); ++vIt) {
      for (ParticleVector::iterator p = _theParticles.begin(); p != _theParticles.end(); ++p) {
        GenVertex* startVtx = ((*p).genParticle()).production_vertex();
        bool veto = false;
        if (startVtx!=0) {
          for (GenVertex::particle_iterator pIt = startVtx->particles_begin(HepMC::ancestors);
                   pIt != startVtx->particles_end(HepMC::ancestors) && !veto; ++pIt) {
            if (*vIt == (*pIt)->pdg_id()) {
              veto = true;
              p = _theParticles.erase(p);
              --p;
            }
          }
        }
      }
    }
    
    // Now veto on the FS
    foreach (const string& ifs, _vetofsnames) {
      const FinalState& vfs = applyProjection<FinalState>(e, ifs);
      const ParticleVector& vfsp = vfs.particles();
      for (ParticleVector::iterator icheck = _theParticles.begin(); icheck != _theParticles.end(); ++icheck) {
        if (!icheck->hasGenParticle()) continue;
        bool found = false;
        for (ParticleVector::const_iterator ipart = vfsp.begin(); ipart != vfsp.end(); ++ipart){
          if (!ipart->hasGenParticle()) continue;
          getLog() << Log::TRACE << "Comparing barcode " << icheck->genParticle().barcode() 
                   << " with veto particle " << ipart->genParticle().barcode() << endl;
          if (ipart->genParticle().barcode() == icheck->genParticle().barcode()){
            found = true;
            break;
          }
        }
        if (found) {
          _theParticles.erase(icheck);
          --icheck;
        }	
      }	
    }
  }


}
