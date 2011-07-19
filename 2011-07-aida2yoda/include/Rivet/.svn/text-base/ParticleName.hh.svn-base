#ifndef RIVET_PARTICLENAME_HH
#define RIVET_PARTICLENAME_HH

#include "Rivet/Particle.fhh"
#include "Rivet/Exceptions.hh"


namespace Rivet {


  /// @name Static const convenience particle ID names
  //@{
  static const PdgId ELECTRON = 11;
  static const PdgId POSITRON = -11;
  static const PdgId PROTON = 2212;
  static const PdgId ANTIPROTON = -2212;
  static const PdgId PHOTON = 22;
  static const PdgId NEUTRON = 2112;
  static const PdgId ANTINEUTRON = -2112;
  static const PdgId MUON = 13;
  static const PdgId ANTIMUON = -13;
  static const PdgId NU_E = 12;
  static const PdgId NU_EBAR = -12;
  static const PdgId NU_MU = 14;
  static const PdgId NU_MUBAR = -14;
  static const PdgId NU_TAU = 16;
  static const PdgId NU_TAUBAR = -16;
  static const PdgId PIPLUS = 211;
  static const PdgId PIMINUS = -211;
  static const PdgId K0L = 130;
  static const PdgId K0S = 310;
  static const PdgId KPLUS = 321;
  static const PdgId KMINUS = -321;
  static const PdgId LAMBDA = 3122;
  static const PdgId LAMBDABAR = -3122;
  static const PdgId XIMINUS = 3312;
  static const PdgId XIPLUS = -3312;
  static const PdgId OMEGAMINUS = 3334;
  static const PdgId OMEGAPLUS = -3334;
  static const PdgId TAU = 15;
  static const PdgId ANTITAU = -15;
  static const PdgId EMINUS = 11;
  static const PdgId EPLUS = -11;
  static const PdgId P = 2212;
  static const PdgId PBAR = -2212;
  static const PdgId GLUON = 21;
  static const PdgId GAMMA = 22;
  static const PdgId WPLUSBOSON = 24;
  static const PdgId WMINUSBOSON = -24;
  static const PdgId ZBOSON = 23;
  static const PdgId HIGGS = 25;
  static const PdgId DQUARK = 1;
  static const PdgId UQUARK = 2;
  static const PdgId SQUARK = 3;
  static const PdgId CQUARK = 4;
  static const PdgId BQUARK = 5;
  static const PdgId TQUARK = 6;
  static const PdgId ANY = 10000;
  // static const PdgId PHOTOELECTRON;
  // static const PdgId PHOTOPOSITRON;
  // static const PdgId PHOTOMUON;
  // static const PdgId PHOTOANTIMUON;
  // static const PdgId PHOTOTAU;
  // static const PdgId PHOTOANTITAU;
  //@}


  class ParticleNames {
  public:

    static const std::string& particleName(PdgId pid) {
      if (!_instance) _instance = new ParticleNames();
      return _instance->_particleName(pid);
    }

    static PdgId particleId(const std::string& pname) {
      if (!_instance) _instance = new ParticleNames();
      return _instance->_particleId(pname);
    }


  public:

    const std::string& _particleName(PdgId pid);


    PdgId _particleId(const std::string& pname);


  private:

    ParticleNames() {
      _add_pid_name(ELECTRON, "ELECTRON");
      _add_pid_name(POSITRON, "POSITRON");
      _add_pid_name(PROTON, "PROTON");
      _add_pid_name(ANTIPROTON, "ANTIPROTON");
      _add_pid_name(PHOTON, "PHOTON");
      _add_pid_name(NEUTRON, "NEUTRON");
      _add_pid_name(ANTINEUTRON, "ANTINEUTRON");
      _add_pid_name(MUON, "MUON");
      _add_pid_name(ANTIMUON, "ANTIMUON");
      _add_pid_name(NU_E, "NU_E");
      _add_pid_name(NU_EBAR, "NU_EBAR");
      _add_pid_name(NU_MU, "NU_MU");
      _add_pid_name(NU_MUBAR, "NU_MUBAR");
      _add_pid_name(NU_TAU, "NU_TAU");
      _add_pid_name(NU_TAUBAR, "NU_TAUBAR");
      _add_pid_name(PIPLUS, "PIPLUS");
      _add_pid_name(PIMINUS, "PIMINUS");
      _add_pid_name(TAU, "TAU");
      _add_pid_name(WPLUSBOSON, "WPLUSBOSON");
      _add_pid_name(WMINUSBOSON, "WMINUSBOSON");
      _add_pid_name(ZBOSON, "ZBOSON");
      _add_pid_name(HIGGS, "HIGGS");
      _add_pid_name(ANTITAU, "ANTITAU");
      // _add_pid_name(PHOTOELECTRON, "PHOTOELECTRON");
      // _add_pid_name(PHOTOPOSITRON, "PHOTOPOSITRON");
      // _add_pid_name(PHOTOMUON, "PHOTOMUON");
      // _add_pid_name(PHOTOANTIMUON, "PHOTOANTIMUON");
      // _add_pid_name(PHOTOTAU, "PHOTOTAU");
      // _add_pid_name(PHOTOANTITAU, "PHOTOANTITAU");
      _add_pid_name(ANY, "*");
    }

    void _add_pid_name(PdgId pid, const std::string& pname) {
      _ids_names[pid] = pname;
      _names_ids[pname] = pid;
    }


    static ParticleNames* _instance;

    std::map<PdgId, std::string> _ids_names;

    std::map<std::string, PdgId> _names_ids;

  };


  /// Print a PdgId as a named string.
  inline const std::string& toParticleName(PdgId p) {
    return ParticleNames::particleName(p);
  }


  /// Print a PdgId as a named string.
  inline PdgId toParticleId(const std::string& pname) {
    return ParticleNames::particleId(pname);
  }


  /// Convenience maker of particle ID pairs from PdgIds.
  inline std::pair<PdgId,PdgId> make_pdgid_pair(PdgId a, PdgId b) {
    return make_pair(a, b);
  }


  /// Convenience maker of particle ID pairs from particle names.
  inline std::pair<PdgId,PdgId> make_pdgid_pair(const std::string& a, const std::string& b) {
    const PdgId pa = toParticleId(a);
    const PdgId pb = toParticleId(b);
    return make_pair(pa, pb);
  }


  /// Print a PdgIdPair as a string.
  inline std::string toBeamsString(const PdgIdPair& pair) {
    string out = "[" +
      toParticleName(pair.first) + ", " +
      toParticleName(pair.second) + "]";
    return out;
  }


}

#endif
