// -*- C++ -*-
#ifndef RIVET_LeptonClusters_HH
#define RIVET_LeptonClusters_HH

#include "Rivet/Tools/Logging.hh"
#include "Rivet/Rivet.hh"
#include "Rivet/Particle.hh"
#include "Rivet/Event.hh"
#include "Rivet/Projection.hh"
#include "Rivet/Projections/FinalState.hh"
#include "Rivet/Projections/IdentifiedFinalState.hh"

namespace Rivet {

  /// @brief Cluster photons from fs to all charged particles (typically
  /// leptons) from signal and store the original charged particles and photons
  /// as particles() while the newly created clustered lepton objects are
  /// accessible as clusteredLeptons()
  class LeptonClustersConstituents : public FinalState {
  public:

    /// @name Constructors
    //@{
    LeptonClustersConstituents(const FinalState& fs, const FinalState& signal,
                               double dRmax, bool cluster, bool track)
      : _dRmax(dRmax), _cluster(cluster), _track(track)
    {
      setName("LeptonClustersConstituents");
      IdentifiedFinalState photonfs(fs);
      photonfs.acceptId(PHOTON);
      addProjection(photonfs, "Photons");
      addProjection(signal, "Signal");
    }


    /// Clone on the heap.
    virtual const Projection* clone() const {
      return new LeptonClustersConstituents(*this);
    }
    //@}


  public:

    const ParticleVector& clusteredLeptons() const { return _clusteredLeptons; }

  protected:

    /// Apply the projection on the supplied event.
    void project(const Event& e);

    /// Compare projections.
    int compare(const Projection& p) const;


  private:

    /// maximum cone radius to find photons in
    double _dRmax;
    /// whether to actually add the photon momenta to clusteredLeptons
    bool _cluster;
    /// whether to add the photons to the particles() vector
    bool _track;
    ParticleVector _clusteredLeptons;

  };



  /// @brief Use LeptonClustersConstituents projection to cluster all photons to
  /// leptons. This projection here makes the clustered objects available
  /// in a FinalState manner, i.e. as particles(). The given pT and eta cuts are
  /// applied to those objects. The underlying (original) leptons and photons
  /// are available by means of the constituentsFinalState() method.
  class LeptonClusters : public FinalState {

  public:

    LeptonClusters(const FinalState& fs, const FinalState& signal, double dRmax,
                   bool cluster, bool track,
                   const std::vector<std::pair<double, double> >& etaRanges,
                   double pTmin) :
      FinalState(etaRanges, pTmin)
    {
      setName("LeptonClusters");
      LeptonClustersConstituents constituents(fs, signal, dRmax, cluster, track);
      addProjection(constituents, "Constituents");
    }

    virtual const Projection* clone() const {
      return new LeptonClusters(*this);
    }

    const FinalState& constituentsFinalState() const;

  protected:

    /// Apply the projection on the supplied event.
    void project(const Event& e);

    /// Compare projections.
    int compare(const Projection& p) const;
  };


}


#endif
