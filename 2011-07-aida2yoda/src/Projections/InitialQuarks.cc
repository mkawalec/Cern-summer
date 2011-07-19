// -*- C++ -*-
#include "Rivet/Projections/InitialQuarks.hh"
#include "Rivet/Tools/Logging.hh"
#include "Rivet/Cmp.hh"


#define IS_PARTON_PDGID(id) ( abs(id) <= 100 && abs(id) != 22 && (abs(id) < 11 || abs(id) > 18) )


namespace Rivet {


  int InitialQuarks::compare(const Projection& p) const {
    return EQUIVALENT;
  }


  void InitialQuarks::project(const Event& e) {
    _theParticles.clear();

    foreach (const GenParticle* p, Rivet::particles(e.genEvent())) {
      const GenVertex* pv = p->production_vertex();
      const GenVertex* dv = p->end_vertex();
      const PdgId pid = abs(p->pdg_id());
      bool passed = (inRange(pid, 1, 5));
      if (passed) {
        if (pv != 0) {
          foreach (const GenParticle* pp, particles_in(pv)) {
            // Only accept if parent is electron or Z0
            const PdgId pid = abs(pp->pdg_id());
            passed = (pid == ELECTRON || abs(pp->pdg_id()) == ZBOSON);
          }
        } else {
          passed = false;
        }
      }

      if (getLog().isActive(Log::TRACE)) {
        const int st = p->status();
        const double pT = p->momentum().perp();
        const double eta = p->momentum().eta();
        getLog() << Log::TRACE << std::boolalpha
                 << "ID = " << p->pdg_id() << ", status = " << st << ", pT = " << pT
                 << ", eta = " << eta << ": result = " << passed << endl;
        if (pv != 0) {
          foreach (const GenParticle* pp, particles_in(pv)) {
            getLog() << Log::TRACE << std::boolalpha
                     << "     parent ID = " << pp->pdg_id() << endl;
          }
        }
        if (dv != 0) {
          foreach (const GenParticle* pp, particles_out(dv)) {
            getLog() << Log::TRACE << std::boolalpha
                     << "     child ID  = " << pp->pdg_id() << endl;
          }
        }
      }
      if (passed) _theParticles.push_back(Particle(*p));
    }
    getLog() << Log::DEBUG << "Number of initial quarks = "
             << _theParticles.size() << endl;
    if (! _theParticles.empty())
      for (size_t i=0 ; i < _theParticles.size() ; i++)
        getLog() << Log::DEBUG << "Initial quark[" << i << "] = "
                 << _theParticles[i].pdgId() << std::endl;
  }


}
