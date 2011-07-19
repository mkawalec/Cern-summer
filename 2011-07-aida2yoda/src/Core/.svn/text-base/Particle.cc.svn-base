#include "Rivet/Particle.hh"
#include "Rivet/RivetBoost.hh"

namespace Rivet {


  bool Particle::hasAncestor(PdgId pdg_id) const {
    GenVertex* prodVtx = genParticle().production_vertex();
    if (prodVtx == 0) return false;
    foreach (const GenParticle* ancestor, particles(prodVtx, HepMC::ancestors)) {
      if (ancestor->pdg_id() == pdg_id) return true;
    }
    return false;
  }


}
