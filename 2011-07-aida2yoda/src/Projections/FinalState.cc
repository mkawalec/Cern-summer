// -*- C++ -*-
#include "Rivet/Projections/FinalState.hh"
#include "Rivet/Tools/Logging.hh"
#include "Rivet/Cmp.hh"

namespace Rivet {


  FinalState::FinalState(double mineta, double maxeta, double minpt)
    : _ptmin(minpt)
  {
    setName("FinalState");
    const bool openpt = isZero(minpt);
    const bool openeta = (mineta <= -MAXRAPIDITY && maxeta >= MAXRAPIDITY);
    getLog() << Log::TRACE << "Check for open FS conditions:" << std::boolalpha
             << " eta=" << openeta
             << ", pt=" << openpt << endl;
    if (!openeta || !openpt) {
      addProjection(FinalState(), "OpenFS");
      if (!openeta) {
        _etaRanges.push_back(make_pair(mineta, maxeta));
      }
    }
  }


  FinalState::FinalState(const vector<pair<double, double> >& etaRanges, double minpt)
    : _etaRanges(etaRanges), _ptmin(minpt)
  {
    setName("FinalState");
    const bool openpt = isZero(minpt);
    /// @todo Properly check whether any of these eta ranges (or their combination) are actually open
    const bool openeta = etaRanges.empty();
    getLog() << Log::TRACE << "Check for open FS conditions:" << std::boolalpha
             << " eta=" << openeta
             << ", pt=" << openpt << endl;
    if (!openeta || !openpt) {
      addProjection(FinalState(), "OpenFS");
    }
  }



  int FinalState::compare(const Projection& p) const {
    const FinalState& other = dynamic_cast<const FinalState&>(p);

    //cout << "FS::compare: " << 1 << " " << this << " " << &p << endl;
    std::vector<std::pair<double, double> > eta1(_etaRanges);
    std::vector<std::pair<double, double> > eta2(other._etaRanges);
    std::sort(eta1.begin(), eta1.end());
    std::sort(eta2.begin(), eta2.end());

    //cout << "FS::compare: " << 2 << " " << this << " " << &p << endl;
    if (eta1 < eta2) return ORDERED;
    else if (eta2 < eta1) return UNORDERED;

    //cout << "FS::compare: " << 3 << " " << this << " " << &p << endl;
    return cmp(_ptmin, other._ptmin);
  }



  void FinalState::project(const Event& e) {
    _theParticles.clear();

    // Handle "open FS" special case
    if (_etaRanges.empty() && _ptmin == 0) {
      //getLog() << Log::TRACE << "Open FS processing: should only see this once per event ("
      //         << e.genEvent().event_number() << ")" << endl;
      foreach (const GenParticle* p, Rivet::particles(e.genEvent())) {
        if (p->status() == 1) {
          //cout << "FS GV = " << p->production_vertex() << endl;
          _theParticles.push_back(Particle(*p));
        }
      }
      return;
    }

    // If this is not itself the "open" FS, base the calculations on the open FS' results
    /// @todo In general, we'd like to calculate a restrictive FS based on the most restricted superset FS.
    const ParticleVector allstable = applyProjection<FinalState>(e, "OpenFS").particles();
    foreach (const Particle& p, allstable) {
      const bool passed = accept(p);
//       if (getLog().isActive(Log::TRACE)) {
//         getLog() << Log::TRACE
//                  << "Choosing: ID = " << p.pdgId()
//                  << ", pT = " << p.momentum().pT()
//                  << ", eta = " << p.momentum().eta()
//                  << ": result = " << std::boolalpha << passed << endl;
//       }
      if (passed) _theParticles.push_back(p);
    }
    //getLog() << Log::DEBUG << "Number of final-state particles = "
    //         << _theParticles.size() << endl;
  }


  /// Decide if a particle is to be accepted or not.
  bool FinalState::accept(const Particle& p) const {
    // Not having s.c. == 1 should never happen!
    assert(!p.hasGenParticle() || p.genParticle().status() == 1);

    // Check pT cut
    if (_ptmin > 0.0) {
      const double pT = p.momentum().pT();
      if (pT < _ptmin) return false;
    }

    // Check eta cuts
    if (!_etaRanges.empty()) {
      bool eta_pass = false;
      const double eta = p.momentum().eta();
      typedef pair<double,double> EtaPair;
      foreach (const EtaPair& etacuts, _etaRanges) {
        if (eta > etacuts.first && eta < etacuts.second) {
          eta_pass = true;
          break;
        }
      }
      if (!eta_pass) return false;
    }
 
    return true;
  }


}
