// -*- C++ -*-
#include "Rivet/Rivet.hh"
#include "Rivet/Tools/Logging.hh"
#include "Rivet/Projections/Beam.hh"

namespace Rivet {


  ParticlePair beams(const Event& e) {
    Beam beamproj;
    beamproj.project(e);
    return beamproj.beams();
  }

  PdgIdPair beamIds(const Event& e) {
    Beam beamproj;
    beamproj.project(e);
    return beamproj.beamIds();
  }

  PdgIdPair beamIds(const ParticlePair& beams) {
    return make_pair(beams.first.pdgId(), beams.second.pdgId());
  }

  double sqrtS(const Event& e) {
    Beam beamproj;
    beamproj.project(e);
    return beamproj.sqrtS();
  }

  double sqrtS(const ParticlePair& beams) {
    return sqrtS(beams.first.momentum(), beams.second.momentum());
  }

  double sqrtS(const FourMomentum& pa, const FourMomentum& pb) {
    const double mom1 = pa.pz();
    const double e1 = pa.E();
    const double mom2 = pb.pz();
    const double e2 = pb.E();
    double sqrts = sqrt( sqr(e1+e2) - sqr(mom1+mom2) );
    return sqrts;
  }



  /////////////////////////////////////////////



  void Beam::project(const Event& e) {
    assert(e.genEvent().particles_size() >= 2);
    if (e.genEvent().valid_beam_particles()) {
      pair<HepMC::GenParticle*, HepMC::GenParticle*> beams = e.genEvent().beam_particles();
      assert(beams.first && beams.second);
      _theBeams.first = *(beams.first);
      _theBeams.second = *(beams.second);
    } else {
      _theBeams.first = *(e.genEvent().barcode_to_particle(1));
      _theBeams.second = *(e.genEvent().barcode_to_particle(2));
    }
    //getLog() << Log::DEBUG << "Beam particle IDs = " << beamIds() << endl;
  }


  double Beam::sqrtS() const {
    double sqrts = Rivet::sqrtS(beams());
    //getLog() << Log::DEBUG << "sqrt(s) = " << sqrts/GeV << " GeV" << endl;
    return sqrts;
  }



}
