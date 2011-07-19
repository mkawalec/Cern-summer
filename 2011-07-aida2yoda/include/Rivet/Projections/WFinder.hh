// -*- C++ -*-
#ifndef RIVET_WFinder_HH
#define RIVET_WFinder_HH

#include "Rivet/Tools/Logging.hh"
#include "Rivet/Rivet.hh"
#include "Rivet/Particle.hh"
#include "Rivet/Event.hh"
#include "Rivet/Projection.hh"
#include "Rivet/Projections/ChargedFinalState.hh"

namespace Rivet {


  /// @brief Convenience finder of leptonically decaying Ws
  ///
  /// Chain together different projections as convenience for finding W's
  /// from two leptons in the final state, including photon clustering.
  class WFinder : public FinalState {
  public:

    /// @name Constructors
    //@{

    // /// Constructor taking a FinalState and type of the charged lepton, mass window,
    // /// and maximum dR of photons around the charged lepton to take into account for W
    // /// reconstruction.
    // WFinder(const ChargedFinalState& fs_l,
    //         PdgId pid,
    //         double m2_min, double m2_max,
    //         double missingET,
    //         double dRmax, bool clusterPhotons, bool excludePhotonsFromRFS);


    /// Constructor taking single eta/pT bounds and type of the charged lepton, mass
    /// window, and maximum dR of photons around the charged lepton to take into account
    /// for W reconstruction.
    WFinder(double etaMin, double etaMax,
            double pTmin,
            PdgId pid,
            double m2_min, double m2_max,
            double missingET,
            double dRmax, bool clusterPhotons=true, bool excludePhotonsFromRFS=false);


    /// Constructor taking multiple eta/pT bounds and type of the charged lepton, mass
    /// window, and maximum dR of photons around the charged lepton to take into account
    /// for W reconstruction.
    WFinder(const std::vector<std::pair<double, double> >& etaRanges,
            double pTmin,
            PdgId pid,
            double m2_min, const double m2_max,
            double missingET,
            double dRmax, bool clusterPhotons=true, bool excludePhotonsFromRFS=false);


    /// Clone on the heap.
    virtual const Projection* clone() const {
      return new WFinder(*this);
    }
    //@}


    /// Access to the remaining particles, after the W and clustered photons
    /// have been removed from the full final state
    /// (e.g. for running a jet finder on it)
    const FinalState& remainingFinalState() const;

    /// Access to the W constituent clustered lepton
    /// (e.g. for more fine-grained cuts on the clustered lepton)
    Particle constituentLepton() const;
    Particle constituentNeutrino() const;

    const FinalState& originalLeptonFinalState() const;

  protected:

    /// Apply the projection on the supplied event.
    void project(const Event& e);

    /// Compare projections.
    int compare(const Projection& p) const;


  public:

    /// Clear the projection
    void clear();


  private:

    /// Common implementation of constructor operation, taking FS params.
    void _init(const std::vector<std::pair<double, double> >& etaRanges,
               double pTmin,  PdgId pid,
               double m2_min, double m2_max,
               double missingET,
               double dRmax, bool clusterPhotons, bool excludePhotonsFromRFS);


  private:

    // Mass range
    double _m2_min, _m2_max;

    // Missing ET cut
    double _etMiss;

  };


}


#endif
