#include "Rivet/Jet.hh"
#include "Rivet/Tools/Logging.hh"
#include "Rivet/Tools/ParticleIdUtils.hh"
#include "Rivet/ParticleName.hh"
#include "Rivet/RivetBoost.hh"

namespace Rivet {


  Jet::Jet()
    : ParticleBase()
  {
    clear();
  }


  Jet& Jet::setParticles(const vector<FourMomentum>& particles) {
    _particles = particles;
    _resetCaches();
    return *this;
  }


  Jet& Jet::addParticle(const FourMomentum& particle) {
    _particles.push_back(particle);
    _resetCaches();
    return *this;
  }


  Jet& Jet::addParticle(const Particle& particle) {
    _fullParticles.push_back(particle);
    _particles.push_back(particle.momentum());
    _resetCaches();
    return *this;
  }
 

  bool Jet::containsParticle(const Particle& particle) const {
    const int barcode = particle.genParticle().barcode();
    foreach (const Particle& p, particles()) {
      if (p.genParticle().barcode() == barcode) return true;
    }
    return false;
  }


  bool Jet::containsParticleId(PdgId pid) const {
    foreach (const Particle& p, particles()) {
      if (p.pdgId() == pid) return true;
    }
    return false;
  }


  bool Jet::containsParticleId(const vector<PdgId>& pids) const {
    foreach (const Particle& p, particles()) {
      foreach (PdgId pid, pids) {
        if (p.pdgId() == pid) return true;
      }
    }
    return false;
  }


  /// @todo Jet::containsMatch(Matcher m) { ... if m(pid) return true; ... }


  double Jet::totalEnergy() const {
    return momentum().E();
  }


  double Jet::neutralEnergy() const {
    double e_neutral = 0.0;
    foreach (const Particle& p, particles()) {
      const PdgId pid = p.pdgId();
      if (PID::threeCharge(pid) == 0) {
        e_neutral += p.momentum().E();
      }
    }
    return e_neutral;
  }


  double Jet::hadronicEnergy() const {
    double e_hadr = 0.0;
    foreach (const Particle& p, particles()) {
      const PdgId pid = p.pdgId();
      if (PID::isHadron(pid)) {
        e_hadr += p.momentum().E();
      }
    }
    return e_hadr;
  }


  bool Jet::containsCharm() const {
    foreach (const Particle& p, particles()) {
      const PdgId pid = p.pdgId();
      if (abs(pid) == CQUARK) return true;
      if (PID::isHadron(pid) && PID::hasCharm(pid)) return true;
      HepMC::GenVertex* gv = p.genParticle().production_vertex();
      if (gv) {
        foreach (const GenParticle* pi, Rivet::particles(gv, HepMC::ancestors)) {
          const PdgId pid2 = pi->pdg_id();
          if (PID::isHadron(pid2) && PID::hasCharm(pid2)) return true;
        }
      }
    }
    return false;
  }


  bool Jet::containsBottom() const {
    foreach (const Particle& p, particles()) {
      const PdgId pid = p.pdgId();
      if (abs(pid) == BQUARK) return true;
      if (PID::isHadron(pid) && PID::hasBottom(pid)) return true;
      HepMC::GenVertex* gv = p.genParticle().production_vertex();
      if (gv) {
        foreach (const GenParticle* pi, Rivet::particles(gv, HepMC::ancestors)) {
          const PdgId pid2 = pi->pdg_id();
          if (PID::isHadron(pid2) && PID::hasBottom(pid2)) return true;
        }
      }
    }
    return false;
  }


  Jet& Jet::clear() {
    _particles.clear();
    _fullParticles.clear();
    _resetCaches();
    return *this;
  }


  double Jet::ptWeightedEta() const {
    _calcPtAvgs();
    assert(_okPtWeightedEta);
    return _ptWeightedEta;
  }


  double Jet::ptWeightedPhi() const {
    _calcPtAvgs();
    assert(_okPtWeightedPhi);
    return _ptWeightedPhi;
  }


  double Jet::eta() const {
    return momentum().eta();

  }


  double Jet::phi() const {
    return momentum().phi();
  }


  const FourMomentum& Jet::momentum() const {
    _calcMomVector();
    return _momentum;
  }

 
  // FourMomentum& Jet::momentum() {
  //   _calcMomVector();
  //   return _momentum;
  // }

 
  double Jet::ptSum() const {
    return momentum().pT();
  }


  double Jet::EtSum() const {
    return momentum().Et();
  }


  void Jet::_resetCaches() const {
    _okPtWeightedPhi = false;
    _okPtWeightedEta = false;
    _okMomentum = false;
  }


  void Jet::_calcMomVector() const {
    if (!_okMomentum) {
      _momentum = accumulate(begin(), end(), FourMomentum());
      _okMomentum = true;
    }
  }


  void Jet::_calcPtAvgs() const {
    if (!_okPtWeightedEta || !_okPtWeightedPhi) {
      double ptwetasum(0.0), ptwdphisum(0.0), ptsum(0.0);
      double phi0 = phi();
      foreach (const FourMomentum& p, momenta()) {
        double pt = p.pT();
        ptsum += pt;
        ptwetasum += pt * p.pseudorapidity();
        ptwdphisum += pt * mapAngleMPiToPi(phi0 - p.azimuthalAngle());
      }
      _ptWeightedEta = ptwetasum/ptsum;
      _okPtWeightedEta = true;
      _ptWeightedPhi = mapAngleMPiToPi(phi0 + ptwdphisum/ptsum);
      _okPtWeightedPhi = true;
    }
  }


}
