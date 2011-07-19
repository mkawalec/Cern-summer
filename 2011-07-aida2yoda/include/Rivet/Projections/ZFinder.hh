// -*- C++ -*-
#ifndef RIVET_ZFinder_HH
#define RIVET_ZFinder_HH

#include "Rivet/Tools/Logging.hh"
#include "Rivet/Rivet.hh"
#include "Rivet/Particle.hh"
#include "Rivet/Event.hh"
#include "Rivet/Projection.hh"
#include "Rivet/Projections/FinalState.hh"

namespace Rivet {


  /// @brief Convenience finder of leptonically decaying Zs
  ///
  /// Chain together different projections as convenience for finding Z's
  /// from two leptons in the final state, including photon clustering.
  class ZFinder : public FinalState {

  public:

    /// @name Constructors
    //@{

    /// Constructor taking single eta/pT bounds and type of the leptons, mass
    /// window, and maximum dR of photons around leptons to take into account
    /// for Z reconstruction.
    /// It has to be specified separately whether such photons are
    /// supposed to be clustered to the lepton objects and whether they should
    /// be excluded from the remaining FS.
    ZFinder(double etaMin, double etaMax,
            double pTmin,
            PdgId pid,
            double m2_min, double m2_max,
            double dRmax, bool clusterPhotons, bool excludePhotonsFromRFS);


    /// Constructor taking multiple eta/pT bounds and type of the leptons, mass
    /// window, and maximum dR of photons around leptons to take into account
    /// for Z reconstruction.
    /// It has to be specified separately whether such photons are
    /// supposed to be clustered to the lepton objects and whether they should
    /// be excluded from the remaining FS.
    ZFinder(const std::vector<std::pair<double, double> >& etaRanges,
            double pTmin,
            PdgId pid,
            double m2_min, const double m2_max,
            double dRmax, bool clusterPhotons, bool excludePhotonsFromRFS);


    /// Clone on the heap.
    virtual const Projection* clone() const {
      return new ZFinder(*this);
    }
    //@}


    /// Access to the remaining particles, after the Z and clustered photons
    /// have been removed from the full final state
    /// (e.g. for running a jet finder on it)
    const FinalState& remainingFinalState() const;

    /// Access to the Z constituent clustered leptons final state
    /// (e.g. for more fine-grained cuts on the clustered leptons)
    const FinalState& constituentsFinalState() const;

    const FinalState& originalConstituentsFinalState() const;

  protected:

    /// Apply the projection on the supplied event.
    void project(const Event& e);

    /// Compare projections.
    int compare(const Projection& p) const;


  private:
    /// Common implementation of constructor operation, taking FS params.
    void _init(const std::vector<std::pair<double, double> >& etaRanges,
               double pTmin,  PdgId pid,
               double m2_min, double m2_max,
               double dRmax, bool clusterPhotons, bool excludePhotonsFromJets);

  };


}


#endif
