// -*- C++ -*-
#ifndef RIVET_SVertex_HH
#define RIVET_SVertex_HH

#include "Rivet/Rivet.hh"
#include "Rivet/Projection.hh"
#include "Rivet/Projections/PVertex.hh"
#include "Rivet/Projections/ChargedFinalState.hh"
#include "Rivet/Event.hh"

namespace Rivet {


  /**
     @brief Determine secondary vertices.
     
     Makes use of PVertex projection.

     @todo Replace function with a functor to improve equality comparisons.

     Complex cuts on tracks and vertices to validate them have to be provided
     by an external function
     bool f(SVertex&, ParticleVector&, const HepMC::GenVertex&, FourMomentum);
     which can be embedded in the analysis code. An example can be found
     in the S6653332 analysis. A pointer to this function has to be given
     to the constructor of the SVertex projection. Its arguments are as follows:

     in: reference to instance of SVertex projection, ParticleVector of
         vertex to be analyzed, primary (Gen)Vertex
     out: FourMomentum = visible Momentum of vertex (selected tracks),
     return bool: cuts passed? 1 : 0

     In this way the SVertex projection can be kept as universal/flexible
     as possible.

     The constructor expects also a list of (pre-selected) jets.
     Associated tracks and vertices to a jet are checked for displacement.
     A list of tagged jets can be obtained via the getTaggedJets() function
  */
  class SVertex : public Projection {
  public:

    /// @name Standard constructors and destructors.
    //@{
    /// The default constructor. Must specify a PVertex
    /// projection object which is assumed to live through the run.
    SVertex(const ChargedFinalState& chfs,
            const vector<FourMomentum>& jetaxes, double deltaR,
            double detEta, double IPres, double DLS, double DLSres=0.0)
      : _jetaxes(jetaxes), _deltaR(deltaR),
        _detEta(detEta), _IPres(IPres), _DLS(DLS),
        _DLSres(DLSres)
    {
      setName("SVertex");
      addProjection(PVertex(), "PV");
      addProjection(chfs, "FS");
      if (_DLSres == 0.0) {
        _DLSres = _IPres;
      }
    }

    /// Clone on the heap.
    virtual const Projection* clone() const {
      return new SVertex(*this);
    }
    //@}


  public:
    /// Return vector of tagged jets (FourMomentum's)
    const vector<FourMomentum>& getTaggedJets() const {
      return _taggedjets;
    }

  protected:

    /// Apply the projection to the event.
    void project(const Event& e);

    /// Compare projections.
    int compare(const Projection& p) const;

  private:

    /// The jet axes of the jet algorithm projection
    const vector<FourMomentum>& _jetaxes;

    /// Max distance between vis. momentum of vertex and jet to be probed
    double _deltaR;

    /// Analysis dependent cuts to be specified in analysis function
    /// @todo Replace with inheritance-based cut method.
    //bool (*_applyVtxTrackCuts) (const ParticleVector&, const Vector3&, FourMomentum);
    bool _applyVtxTrackCuts(const ParticleVector&, const Vector3&, FourMomentum);

    /// Geometrical acceptance of tracker
    double _detEta;

    /// Impact parameter resolution, (including beam size)
    double _IPres;

    /// Decay length significance (cut value)
    double _DLS;

    /// Decay length significance uncertainty
    double _DLSres;

    /// Jets which have been tagged
    vector<FourMomentum> _taggedjets;
  };

}

#endif
